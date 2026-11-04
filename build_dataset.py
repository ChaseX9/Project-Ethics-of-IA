"""Construit un dataset de parties rapides chess.com stratifié par tranche d'Elo et pays.

Usage :
    python -u build_dataset.py                 # lance ou reprend la collecte
    python -u build_dataset.py --max-hours 6   # s'arrête proprement après 6 h (relancer pour reprendre)

Reprise : data/checkpoint/players.jsonl contient une ligne par joueur traité, avec ses
parties retenues et ses adversaires. Une ligne est écrite d'un seul coup : un arrêt brutal
perd au plus le joueur en cours. Les joueurs de départ et la fenêtre de 12 mois sont figés
au premier lancement, et la file est reconstruite à la reprise à partir du journal.

Échantillonnage "boule de neige" : /pub/country/{CODE}/players est tronqué à 10 000 joueurs
par ordre alphabétique, donc on n'en tire que quelques joueurs de départ (plus les
leaderboards), puis on visite les adversaires rencontrés. Ceux-ci sont rangés par tranche
d'après leur Elo dans la partie, et les tranches sont visitées à tour de rôle : sans cela, la
file serait dominée par les bas Elo, les plus nombreux.
"""

import argparse
import csv
import ctypes
import json
import math
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

BASE_URL = "https://api.chess.com/pub"
CONTACT_ENV_VAR = "CHESSCOM_CONTACT"

DATA_DIR = Path("data")
CHECKPOINT_DIR = DATA_DIR / "checkpoint"
PLAYERS_LOG = CHECKPOINT_DIR / "players.jsonl"
META_FILE = CHECKPOINT_DIR / "meta.json"
SEEDS_FILE = CHECKPOINT_DIR / "seeds.json"

# Tranches semi-ouvertes [min, max[ : un Elo de 400 appartient à "400-700".
BINS = [
    ("100-400", 100, 400),
    ("400-700", 400, 700),
    ("700-1000", 700, 1000),
    ("1000-1300", 1000, 1300),
    ("1300-1600", 1300, 1600),
    ("1600-1900", 1600, 1900),
    ("1900+", 1900, math.inf),
]
QUOTAS = {"FR": 240, "IN": 90, "US": 90, "BR": 90, "DE": 90}
COUNTRIES = list(QUOTAS)

MIN_PLIES = 40
MAX_GAMES_PER_PLAYER = 5
WINDOW_DAYS = 365

SEEDS_PER_COUNTRY = 10
LEADERBOARDS = ("live_rapid", "live_blitz", "live_bullet")
# Sans plafond, les leaderboards (traités en premier) remplissent seuls la case US 1900+ avec des Elo >= 2400.
LEADERBOARD_MAX_SHARE = 0.25

COLUMNS = [
    "game_url", "date", "username", "country", "source", "elo", "opponent_elo", "color", "result",
    "termination", "eco", "opening_name", "nb_moves", "time_control", "accuracy", "moves", "pgn",
]

DRAW_RESULTS = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}
TERMINATIONS = {
    "checkmated": "mat",
    "resigned": "abandon",
    "timeout": "temps",
    "abandoned": "deconnexion",
    "agreed": "nulle_accord",
    "repetition": "nulle_repetition",
    "stalemate": "pat",
    "insufficient": "materiel_insuffisant",
    "50move": "regle_50_coups",
    "timevsinsufficient": "temps_vs_materiel_insuffisant",
}

MAX_RETRIES = 6
MAX_CONSECUTIVE_FAILURES = 20


class ApiError(Exception):
    """L'API n'a pas donné de réponse exploitable après tous les essais."""


def user_agent():
    """Lu ici plutôt qu'à l'import : stockfish_features.py importe ce module sans appeler l'API."""
    contact = os.environ.get(CONTACT_ENV_VAR, "").strip()
    if not contact:
        sys.exit(
            f"Variable d'environnement {CONTACT_ENV_VAR} non définie : chess.com demande un contact dans le User-Agent.\n"
            f'PowerShell : $env:{CONTACT_ENV_VAR} = "votre.email@example.com"\n'
            f'bash : export {CONTACT_ENV_VAR}="votre.email@example.com"'
        )
    return f"school-project-elo (contact: {contact})"


class Client:
    """Client HTTP strictement séquentiel, avec pause et backoff."""

    def __init__(self, pause):
        self.pause = pause
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent()
        self.n_requests = 0
        self.n_retries = 0

    def get(self, url):
        """Renvoie le JSON, ou None si la ressource n'existe pas (404/410)."""
        last_error = None
        for attempt in range(MAX_RETRIES):
            time.sleep(self.pause)
            self.n_requests += 1
            retry_after = None
            try:
                response = self.session.get(url, timeout=60)
                status = response.status_code
                if status == 200:
                    return response.json()
                if status in (404, 410):
                    return None
                if status != 429 and status < 500:
                    raise ApiError(f"HTTP {status} sur {url}")
                last_error = f"HTTP {status}"
                retry_after = response.headers.get("Retry-After")
            except (requests.RequestException, ValueError) as error:
                last_error = repr(error)

            self.n_retries += 1
            delay = 2 ** attempt + random.random()
            if retry_after and retry_after.isdigit():
                delay = max(delay, int(retry_after))
            print(f"  [retry {attempt + 1}/{MAX_RETRIES}] {last_error} - pause {delay:.0f}s", flush=True)
            time.sleep(delay)
        raise ApiError(f"{last_error} sur {url}")


def bin_label(rating):
    for label, low, high in BINS:
        if low <= rating < high:
            return label
    return None


def pgn_moves(pgn):
    """Renvoie uniquement les coups et les horloges : ni en-têtes (Elo, pseudos), ni résultat final."""
    movetext = pgn.split("\n\n", 1)[-1].strip()
    return re.sub(r"\s*(1-0|0-1|1/2-1/2|\*)$", "", movetext)


def count_plies(pgn):
    """Compte les demi-coups de la partie, annotations d'horloge exclues."""
    movetext = re.sub(r"\{[^}]*\}", " ", pgn_moves(pgn))
    return sum(1 for token in movetext.split() if not re.fullmatch(r"\d+\.+", token))


def pgn_tag(pgn, tag):
    match = re.search(rf'^\[{tag} "(.*)"\]$', pgn, re.MULTILINE)
    return match.group(1) if match else ""


def opening_from_url(url):
    slug = url.rstrip("/").rsplit("/", 1)[-1] if url else ""
    return slug.replace("-", " ")


def is_rated_rapid(game, cutoff):
    return (
        game.get("time_class") == "rapid"
        and game.get("rated") is True
        and game.get("rules") == "chess"
        and game.get("end_time", 0) >= cutoff
    )


def game_to_row(game, username, country, cutoff):
    """Applique les filtres. Renvoie la ligne du dataset, ou None si la partie est écartée."""
    if not is_rated_rapid(game, cutoff):
        return None
    pgn = game.get("pgn") or ""
    plies = count_plies(pgn)
    if plies < MIN_PLIES:
        return None

    if game["white"]["username"].lower() == username.lower():
        color, opponent_color = "white", "black"
    elif game["black"]["username"].lower() == username.lower():
        color, opponent_color = "black", "white"
    else:
        return None
    player, opponent = game[color], game[opponent_color]

    if player["result"] == "win":
        result, raw_termination = "win", opponent["result"]
    elif player["result"] in DRAW_RESULTS:
        result, raw_termination = "draw", player["result"]
    else:
        result, raw_termination = "loss", player["result"]

    accuracy = (game.get("accuracies") or {}).get(color, "")
    return {
        "game_url": game["url"],
        "date": datetime.fromtimestamp(game["end_time"], timezone.utc).strftime("%Y-%m-%d"),
        "username": player["username"],
        "country": country,
        "elo": player["rating"],
        "opponent_elo": opponent["rating"],
        "color": color,
        "result": result,
        "termination": TERMINATIONS.get(raw_termination, raw_termination),
        "eco": pgn_tag(pgn, "ECO"),
        "opening_name": opening_from_url(pgn_tag(pgn, "ECOUrl") or game.get("eco", "")),
        "nb_moves": math.ceil(plies / 2),
        "time_control": game.get("time_control", ""),
        "accuracy": accuracy,
        "moves": pgn_moves(pgn),
        "pgn": pgn,
    }


def write_with_retry(action):
    """OneDrive verrouille parfois brièvement les fichiers en cours de synchronisation."""
    for attempt in range(8):
        try:
            return action()
        except PermissionError:
            if attempt == 7:
                raise
            time.sleep(1 + attempt)


def load_or_create_meta(seed):
    if META_FILE.exists():
        return json.loads(META_FILE.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    meta = {
        "seed": seed,
        "created_at": now.isoformat(),
        "cutoff": int((now - timedelta(days=WINDOW_DAYS)).timestamp()),
    }
    write_with_retry(lambda: META_FILE.write_text(json.dumps(meta), encoding="utf-8"))
    return meta


def load_or_create_seeds(client, seed):
    """Tire les joueurs de départ : quelques-uns par pays, plus les leaderboards."""
    if SEEDS_FILE.exists():
        return json.loads(SEEDS_FILE.read_text(encoding="utf-8"))
    seeds = []
    for country in COUNTRIES:
        data = client.get(f"{BASE_URL}/country/{country}/players")
        if data is None:
            raise ApiError(f"Liste de joueurs introuvable pour {country}")
        players = sorted(player.lower() for player in set(data["players"]))
        sample = random.Random(f"{seed}-{country}").sample(players, SEEDS_PER_COUNTRY)
        seeds += [{"username": player, "source": "country_list"} for player in sample]
    leaderboards = client.get(f"{BASE_URL}/leaderboards")
    if leaderboards is None:
        raise ApiError("Leaderboards introuvables")
    for board in LEADERBOARDS:
        seeds += [{"username": e["username"].lower(), "source": "leaderboard"} for e in leaderboards[board]]
    write_with_retry(lambda: SEEDS_FILE.write_text(json.dumps(seeds), encoding="utf-8"))
    return seeds


def load_checkpoint(path=PLAYERS_LOG):
    """Relit le journal ; une dernière ligne tronquée par un arrêt brutal est ignorée et retirée."""
    records = []
    if not path.exists():
        return records
    raw = path.read_text(encoding="utf-8")
    valid_length = 0
    for line in raw.splitlines(keepends=True):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            print("Ligne de checkpoint tronquée ignorée.", flush=True)
            break
        if not line.endswith("\n"):
            records.pop()
            print("Ligne de checkpoint incomplète ignorée.", flush=True)
            break
        valid_length += len(line)
    if valid_length != len(raw):
        def truncate():
            with path.open("w", encoding="utf-8", newline="") as file:
                file.write(raw[:valid_length])
        write_with_retry(truncate)
    return records


def append_checkpoint(record, path=PLAYERS_LOG):
    # ASCII pur : les séparateurs Unicode resteraient sinon bruts et couperaient la ligne à la relecture.
    line = json.dumps(record) + "\n"

    def append():
        with path.open("a", encoding="utf-8", newline="") as file:
            file.write(line)

    write_with_retry(append)


def opponent_of(game, username, cutoff):
    """Renvoie (pseudo en minuscules, Elo) de l'adversaire d'une partie rapide classée, sinon None."""
    if not is_rated_rapid(game, cutoff):
        return None
    white, black = game["white"], game["black"]
    opponent = black if white["username"].lower() == username.lower() else white
    return opponent["username"].lower(), opponent["rating"]


def fetch_player(client, username, source, meta, counts, leaderboard_counts, seen_urls, rng):
    """Traite un joueur et renvoie son enregistrement de checkpoint. Les compteurs et `seen_urls` sont mis à jour."""
    record = {"username": username, "source": source, "games": []}
    from_leaderboard = source == "leaderboard"

    def leaderboard_cap_reached(cell):
        return from_leaderboard and leaderboard_counts[cell] >= LEADERBOARD_MAX_SHARE * QUOTAS[cell[1]]

    profile = client.get(f"{BASE_URL}/player/{username}")
    if profile is None:
        record["status"] = "no_profile"
        return record

    country = profile.get("country", "").rsplit("/", 1)[-1]
    record["country"] = country
    record["account_status"] = profile.get("status")
    # Comptes fermés, dont les bannis pour triche : leur Elo ne reflète pas forcément leur niveau.
    if (record["account_status"] or "").startswith("closed"):
        record["status"] = "closed_account"
        return record
    if country not in QUOTAS:
        record["status"] = "other_country"
        return record
    if country_is_full(counts, country):
        record["status"] = "country_full"
        return record

    stats = client.get(f"{BASE_URL}/player/{username}/stats")
    rapid = (stats or {}).get("chess_rapid")
    if not rapid or "last" not in rapid:
        record["status"] = "no_rapid"
        return record

    record["rapid"] = rapid["last"]["rating"]
    label = bin_label(record["rapid"])
    if label is None:
        record["status"] = "out_of_bins"
        return record
    if counts[label, country] >= QUOTAS[country]:
        record["status"] = "bin_full"
        return record
    if leaderboard_cap_reached((label, country)):
        record["status"] = "leaderboard_cap"
        return record
    if rapid["last"].get("date", 0) < meta["cutoff"]:
        record["status"] = "inactive"
        return record

    archives = client.get(f"{BASE_URL}/player/{username}/games/archives")
    cutoff_month = datetime.fromtimestamp(meta["cutoff"], timezone.utc).strftime("%Y/%m")
    urls = [url for url in (archives or {}).get("archives", []) if url[-7:] >= cutoff_month]

    candidates = []
    opponents = {}
    for url in urls:
        month = client.get(url)
        for game in (month or {}).get("games", []):
            try:
                opponent = opponent_of(game, username, meta["cutoff"])
                if opponent:
                    opponents[opponent[0]] = opponent[1]
                row = game_to_row(game, username, country, meta["cutoff"])
            except (KeyError, TypeError):
                continue
            if row and row["game_url"] not in seen_urls and bin_label(row["elo"]):
                candidates.append(row)
    # Les adversaires de l'élite resteraient dans l'élite et satureraient la file de la tranche 1900+.
    if not from_leaderboard:
        record["opponents"] = opponents

    # Tirage dans les 12 mois plutôt que les parties les plus récentes.
    rng.shuffle(candidates)
    for row in candidates:
        if len(record["games"]) == MAX_GAMES_PER_PLAYER:
            break
        cell = bin_label(row["elo"]), country
        if counts[cell] < QUOTAS[country] and not leaderboard_cap_reached(cell):
            record["games"].append(row)
            counts[cell] += 1
            leaderboard_counts[cell] += from_leaderboard
            seen_urls.add(row["game_url"])
    record["status"] = "kept" if record["games"] else "no_eligible_game"
    return record


class Frontier:
    """File des joueurs à visiter : les joueurs de départ, puis les adversaires par tranche."""

    def __init__(self, visited, rng):
        self.seen = set(visited)
        self.rng = rng
        self.seeds = deque()
        self.by_bin = {label: [] for label, _, _ in BINS}
        self.next_bin = 0

    def add_seed(self, username, source):
        if username not in self.seen:
            self.seen.add(username)
            self.seeds.append((username, source))

    def add_opponent(self, username, rating):
        label = bin_label(rating)
        if label and username not in self.seen:
            self.seen.add(username)
            self.by_bin[label].append(username)

    def pop(self, counts):
        """Renvoie (pseudo, source), ou None s'il ne reste personne dans une tranche ouverte."""
        if self.seeds:
            return self.seeds.popleft()
        for _ in BINS:
            label = BINS[self.next_bin][0]
            self.next_bin = (self.next_bin + 1) % len(BINS)
            bucket = self.by_bin[label]
            if bucket and any(counts[label, c] < QUOTAS[c] for c in COUNTRIES):
                index = self.rng.randrange(len(bucket))
                bucket[index], bucket[-1] = bucket[-1], bucket[index]
                return bucket.pop(), "opponent"
        return None

    def __len__(self):
        return len(self.seeds) + sum(len(bucket) for bucket in self.by_bin.values())


def country_is_full(counts, country):
    return all(counts[label, country] >= QUOTAS[country] for label, _, _ in BINS)


def print_table(counts):
    labels = [label for label, _, _ in BINS]
    header = f"{'tranche':<11}" + "".join(f"{c:>6}" for c in COUNTRIES) + f"{'total':>7}"
    print(header)
    for label in labels:
        values = [counts[label, c] for c in COUNTRIES]
        print(f"{label:<11}" + "".join(f"{v:>6}" for v in values) + f"{sum(values):>7}")
    totals = [sum(counts[label, c] for label in labels) for c in COUNTRIES]
    print(f"{'total':<11}" + "".join(f"{v:>6}" for v in totals) + f"{sum(totals):>7}", flush=True)


def collect(args):
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    client = Client(args.pause)
    meta = load_or_create_meta(args.seed)
    records = load_checkpoint()

    counts = Counter()
    leaderboard_counts = Counter()
    seen_urls = set()
    for record in records:
        for row in record["games"]:
            counts[bin_label(row["elo"]), row["country"]] += 1
            leaderboard_counts[bin_label(row["elo"]), row["country"]] += record["source"] == "leaderboard"
            seen_urls.add(row["game_url"])
    if records:
        print(f"Reprise : {len(records)} joueurs déjà traités.", flush=True)
        print_table(counts)

    rng = random.Random(f"{meta['seed']}-games-{len(records)}")
    frontier = Frontier((record["username"] for record in records), rng)
    for seed in load_or_create_seeds(client, meta["seed"]):
        frontier.add_seed(seed["username"], seed["source"])
    for record in records:
        for username, rating in record.get("opponents", {}).items():
            frontier.add_opponent(username, rating)
    print(f"File : {len(frontier)} joueurs à visiter", flush=True)

    start = time.time()
    deadline = start + args.max_hours * 3600 if args.max_hours else None
    consecutive_failures = 0
    n_failed = 0
    n_processed = 0

    while True:
        if all(country_is_full(counts, country) for country in COUNTRIES):
            stop_reason = "tous les quotas sont atteints"
            break
        next_player = frontier.pop(counts)
        if next_player is None:
            stop_reason = "file vide : plus d'adversaire à visiter dans les tranches ouvertes"
            break
        username, source = next_player
        try:
            record = fetch_player(client, username, source, meta, counts, leaderboard_counts, seen_urls, rng)
        except ApiError as error:
            # Le joueur n'est pas journalisé : il sera retenté à la prochaine reprise.
            print(f"  [échec] {username} : {error}", flush=True)
            n_failed += 1
            consecutive_failures += 1
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                stop_reason = f"{consecutive_failures} échecs consécutifs (API indisponible ?)"
                break
            continue
        consecutive_failures = 0
        append_checkpoint(record)
        records.append(record)
        n_processed += 1
        for opponent, rating in record.get("opponents", {}).items():
            frontier.add_opponent(opponent, rating)

        if n_processed % args.progress_every == 0:
            elapsed = time.time() - start
            print(
                f"\n--- {len(records)} joueurs traités, {len(frontier)} en file | {client.n_requests} requêtes, "
                f"{client.n_retries} retries, {n_failed} échecs | {elapsed / 60:.0f} min",
                flush=True,
            )
            print_table(counts)

        if deadline and time.time() > deadline:
            stop_reason = f"limite de {args.max_hours} h atteinte (relancer pour reprendre)"
            break

    print(f"\nFin de collecte : {stop_reason}. {n_failed} joueurs en échec sur ce lancement.", flush=True)
    return records


def write_csv(path, rows):
    def write():
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    write_with_retry(write)


def split_rows(rows, seed):
    """Découpe 80/10/10 par joueur, stratifié sur (tranche majoritaire, pays) du joueur."""
    games_by_player = defaultdict(list)
    for row in rows:
        games_by_player[row["username"].lower()].append(row)

    strata = defaultdict(list)
    for player, games in games_by_player.items():
        main_bin = Counter(bin_label(g["elo"]) for g in games).most_common(1)[0][0]
        strata[main_bin, games[0]["country"]].append(player)

    rng = random.Random(f"{seed}-split")
    splits = {"train": [], "val": [], "test": []}
    # Motif de 10 joueurs à 8/1/1, décalé au hasard dans chaque strate.
    pattern = ["train"] * 8 + ["val", "test"]
    for key in sorted(strata):
        players = sorted(strata[key])
        rng.shuffle(players)
        offset = rng.randrange(10)
        for index, player in enumerate(players):
            splits[pattern[(index + offset) % 10]].extend(games_by_player[player])
    return splits


def report(records, rows, splits):
    counts = Counter((bin_label(r["elo"]), r["country"]) for r in rows)
    print("\n========== RÉSUMÉ ==========")
    print(f"Parties : {len(rows)} (objectif {sum(QUOTAS.values()) * len(BINS)})")
    print_table(counts)

    missing = [
        (label, c, counts[label, c], QUOTAS[c])
        for label, _, _ in BINS for c in COUNTRIES if counts[label, c] < QUOTAS[c]
    ]
    print("\nCases non remplies :" if missing else "\nToutes les cases sont remplies.")
    for label, country, actual, quota in missing:
        print(f"  {label:<11}{country} : {actual}/{quota}")

    print("\nJoueurs traités par statut :", dict(Counter(r["status"] for r in records)))
    print("Joueurs traités par pays :", dict(Counter(r.get("country") for r in records).most_common(10)))
    kept = [r for r in records if r["games"]]
    print("Parties par origine du joueur :", dict(Counter(r["source"] for r in kept for _ in r["games"])))
    print("Statut de compte des joueurs retenus :", dict(Counter(r.get("account_status") for r in kept)))

    print("\nDécoupage par joueur :")
    total = max(len(rows), 1)
    for name, subset in splits.items():
        n_players = len({r["username"].lower() for r in subset})
        print(f"  {name:<6}{len(subset):>6} parties ({len(subset) / total:6.1%}), {n_players} joueurs")


def keep_system_awake():
    """Empêche la mise en veille automatique de Windows tant que ce processus tourne (fermer le capot l'emporte)."""
    if sys.platform == "win32":
        ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=42, help="graine, figée au premier lancement")
    parser.add_argument("--pause", type=float, default=0.3, help="pause en secondes avant chaque requête")
    parser.add_argument("--max-hours", type=float, default=None, help="durée maximale de ce lancement")
    parser.add_argument("--progress-every", type=int, default=100, help="affichage tous les N joueurs")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    keep_system_awake()
    records = collect(args)
    rows = [{**row, "source": record["source"]} for record in records for row in record["games"]]
    meta = json.loads(META_FILE.read_text(encoding="utf-8"))
    splits = split_rows(rows, meta["seed"])

    write_csv(DATA_DIR / "games.csv", rows)
    for name, subset in splits.items():
        write_csv(DATA_DIR / f"{name}.csv", subset)
    report(records, rows, splits)


if __name__ == "__main__":
    main()
