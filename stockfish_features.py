"""Calcule avec Stockfish, pour chaque partie et pour le joueur ciblé : gaffes, erreurs, imprécisions et ACPL.

Usage :
    python -u stockfish_features.py                 # lance ou reprend l'analyse
    python -u stockfish_features.py --max-hours 6   # s'arrête proprement après 6 h (relancer pour reprendre)
    python -u stockfish_features.py --limit 20      # n'analyse que 20 parties du tirage

Reprise : data/checkpoint/stockfish.jsonl contient une ligne par partie analysée, écrite d'un
seul coup : un arrêt brutal perd au plus les parties en cours. Les parties sont tirées dans un
ordre fixe et aléatoire, pour qu'une analyse partielle reste représentative de toutes les tranches.

Le journal garde l'évaluation de chaque position : changer les seuils ci-dessous ne demande pas
de relancer le moteur (il suffit de relancer le script, qui réécrit le CSV depuis le journal).

Définitions (celles de Lichess) : une évaluation est bornée à +/-1000 centipions, un mat comptant
pour la borne. La perte d'un coup est max(0, éval avant - éval après) du point de vue du joueur ;
l'ACPL est sa moyenne. Un coup est classé selon la baisse de ses chances de gain, plutôt qu'en
centipions : passer de +900 à +500 ne change pas l'issue et n'est pas une gaffe.
Toutes les positions sont évaluées, ouverture comprise.
"""

import argparse
import csv
import io
import math
import os
import queue
import random
import shutil
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import chess
import chess.engine
import chess.pgn

from build_dataset import CHECKPOINT_DIR, DATA_DIR, append_checkpoint, keep_system_awake, load_checkpoint, write_with_retry

CHECKPOINT_FILE = CHECKPOINT_DIR / "stockfish.jsonl"
GAMES_FILE = DATA_DIR / "games.csv"
OUTPUT_FILE = DATA_DIR / "stockfish_features.csv"

# Mesuré sur 20 parties par rapport à la profondeur 16 (écart moyen d'ACPL / durée pour 4200 parties, 6 moteurs) :
# profondeur 12 : 6,9 cp / 1,4 h ; 14 : 2,7 cp / 4,9 h (6,3 h réelles sur le calcul complet) ; 16 : référence / 16,5 h.
DEFAULT_DEPTH = 14
HASH_MB = 64
CP_CAP = 1000
WIN_CHANCE_SLOPE = 0.00368208
# Baisse des chances de gain, sur une échelle de -1 (perdu) à +1 (gagné).
BLUNDER_DROP = 0.3
MISTAKE_DROP = 0.2
INACCURACY_DROP = 0.1

COLUMNS = ["game_url", "username", "depth", "nb_analyzed_moves", "nb_blunders", "nb_mistakes", "nb_inaccuracies", "acpl"]

MAX_CONSECUTIVE_FAILURES = 20


def find_stockfish():
    """winget n'ajoute qu'un alias au PATH des nouveaux terminaux : on cherche aussi le paquet lui-même."""
    found = shutil.which("stockfish")
    if found:
        return found
    packages = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    matches = sorted(packages.glob("Stockfish.Stockfish_*/stockfish/stockfish*.exe"))
    if not matches:
        sys.exit("Stockfish introuvable : installez-le (winget install Stockfish.Stockfish) ou utilisez --stockfish.")
    return str(matches[0])


def open_engine(path):
    engine = chess.engine.SimpleEngine.popen_uci(path)
    # Un seul thread par moteur : à profondeur fixe, le résultat ne dépend alors pas de la charge.
    engine.configure({"Threads": 1, "Hash": HASH_MB})
    return engine


def position_eval(engine, board, depth, game_id):
    """Évaluation du point de vue des blancs, en centipions bornés."""
    outcome = board.outcome()
    if outcome:
        if outcome.winner is None:
            return 0
        return CP_CAP if outcome.winner == chess.WHITE else -CP_CAP
    # L'historique est transmis au moteur avec le plateau : il voit donc les répétitions.
    info = engine.analyse(board, chess.engine.Limit(depth=depth), game=game_id)
    score = info["score"].white().score(mate_score=CP_CAP * 100)
    return max(-CP_CAP, min(CP_CAP, score))


def analyse_game(engine, pgn, depth, game_id):
    """Renvoie les évaluations des positions, de la position initiale à la position finale."""
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None or game.errors:
        raise ValueError(f"PGN illisible : {game.errors if game else 'vide'}")
    board = game.board()
    evals = [position_eval(engine, board, depth, game_id)]
    for move in game.mainline_moves():
        board.push(move)
        evals.append(position_eval(engine, board, depth, game_id))
    return evals


def win_chance(cp):
    return 2 / (1 + math.exp(-WIN_CHANCE_SLOPE * cp)) - 1


def player_features(evals, color):
    """Résume les coups du joueur à partir des évaluations de la partie."""
    first_ply, sign = (0, 1) if color == "white" else (1, -1)
    losses = []
    counts = {"nb_blunders": 0, "nb_mistakes": 0, "nb_inaccuracies": 0}
    for ply in range(first_ply, len(evals) - 1, 2):
        before, after = sign * evals[ply], sign * evals[ply + 1]
        losses.append(max(0, before - after))
        drop = win_chance(before) - win_chance(after)
        if drop >= BLUNDER_DROP:
            counts["nb_blunders"] += 1
        elif drop >= MISTAKE_DROP:
            counts["nb_mistakes"] += 1
        elif drop >= INACCURACY_DROP:
            counts["nb_inaccuracies"] += 1
    return {"nb_analyzed_moves": len(losses), **counts, "acpl": round(sum(losses) / len(losses), 1) if losses else ""}


def load_games():
    csv.field_size_limit(10 ** 9)
    with GAMES_FILE.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def write_features(path, games, records):
    """Réécrit le CSV depuis le journal, dans l'ordre de games.csv."""
    by_url = {record["game_url"]: record for record in records}
    rows = []
    for game in games:
        record = by_url.get(game["game_url"])
        if record:
            features = player_features(record["evals"], game["color"])
            rows.append({"game_url": game["game_url"], "username": game["username"], "depth": record["depth"], **features})

    def write():
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    write_with_retry(write)
    return rows


def analyse_all(args, todo, n_done):
    """Analyse les parties en parallèle ; seul ce thread écrit dans le journal."""
    engine_path = args.stockfish or find_stockfish()
    engines = queue.Queue()
    for _ in range(args.workers):
        engines.put(open_engine(engine_path))

    def task(game):
        engine = engines.get()
        try:
            return analyse_game(engine, game["pgn"], args.depth, game["game_url"])
        except (chess.engine.EngineError, chess.engine.EngineTerminatedError):
            # Moteur planté : on le remplace, et l'échec remonte au thread principal.
            engine.close()
            engine = open_engine(engine_path)
            raise
        finally:
            engines.put(engine)

    start = time.time()
    deadline = start + args.max_hours * 3600 if args.max_hours else None
    remaining = iter(todo)
    pending = {}
    n_processed = n_failed = consecutive_failures = 0
    stop_reason = None
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        try:
            while True:
                while stop_reason is None and len(pending) < args.workers:
                    game = next(remaining, None)
                    if game is None:
                        break
                    pending[pool.submit(task, game)] = game
                if not pending:
                    stop_reason = stop_reason or "toutes les parties demandées sont traitées"
                    break
                finished, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in finished:
                    game = pending.pop(future)
                    try:
                        evals = future.result()
                    except (ValueError, KeyError, chess.engine.EngineError, chess.engine.EngineTerminatedError) as error:
                        # La partie n'est pas journalisée : elle sera retentée à la prochaine reprise.
                        print(f"  [échec] {game['game_url']} : {error!r}", flush=True)
                        n_failed += 1
                        consecutive_failures += 1
                        if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                            stop_reason = f"{consecutive_failures} échecs consécutifs"
                        continue
                    consecutive_failures = 0
                    append_checkpoint({"game_url": game["game_url"], "depth": args.depth, "evals": evals}, args.checkpoint)
                    n_processed += 1
                    if n_processed % args.progress_every == 0:
                        elapsed = time.time() - start
                        left = (len(todo) - n_processed - n_failed) * elapsed / n_processed
                        print(
                            f"--- {n_done + n_processed} parties analysées, {n_failed} échecs | {elapsed / 60:.1f} min, "
                            f"reste environ {left / 3600:.1f} h",
                            flush=True,
                        )
                if deadline and time.time() > deadline and stop_reason is None:
                    stop_reason = f"limite de {args.max_hours} h atteinte (relancer pour reprendre)"
        except KeyboardInterrupt:
            for future in pending:
                future.cancel()
            stop_reason = "interruption (relancer pour reprendre)"

    while not engines.empty():
        engines.get().quit()
    print(f"Fin d'analyse : {stop_reason}. {n_processed} parties en {(time.time() - start) / 60:.1f} min, {n_failed} échecs.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--depth", type=int, default=DEFAULT_DEPTH, help="profondeur d'analyse (figée par le journal)")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2), help="moteurs en parallèle")
    parser.add_argument("--limit", type=int, default=None, help="ne considère que les N premières parties du tirage")
    parser.add_argument("--max-hours", type=float, default=None, help="durée maximale de ce lancement")
    parser.add_argument("--progress-every", type=int, default=50, help="affichage toutes les N parties")
    parser.add_argument("--seed", type=int, default=42, help="graine du tirage des parties")
    parser.add_argument("--stockfish", default=None, help="chemin de l'exécutable Stockfish")
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT_FILE, help="journal de reprise")
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE, help="CSV de sortie")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    keep_system_awake()
    args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    records = load_checkpoint(args.checkpoint)
    depths = {record["depth"] for record in records}
    if depths - {args.depth}:
        sys.exit(f"Le journal {args.checkpoint} a été calculé en profondeur {sorted(depths)}, pas {args.depth}.")

    games = load_games()
    selection = random.Random(f"{args.seed}-stockfish").sample(games, len(games))[:args.limit]
    done = {record["game_url"] for record in records}
    todo = [game for game in selection if game["game_url"] not in done]
    print(f"{len(selection)} parties demandées, {len(selection) - len(todo)} déjà analysées, {len(todo)} à faire "
          f"(profondeur {args.depth}, {args.workers} moteurs).", flush=True)

    if todo:
        analyse_all(args, todo, len(selection) - len(todo))
    records = load_checkpoint(args.checkpoint)
    rows = write_features(args.output, games, records)
    print(f"{args.output} : {len(rows)} parties.", flush=True)
    # Le journal relu fait foi : sous OneDrive, des lignes écrites sans erreur ont déjà disparu.
    done = {record["game_url"] for record in records}
    missing = sum(game["game_url"] not in done for game in selection)
    if missing:
        print(f"ATTENTION : {missing} parties absentes du journal, relancer le script pour les analyser.", flush=True)


if __name__ == "__main__":
    main()
