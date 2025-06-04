import csv
from typing import Dict, List, Tuple

# Types for clarity
Record = Dict[str, Tuple[int, int]]  # team -> (wins, losses)
Schedule = List[Tuple[str, str]]     # list of (home_team, away_team)


def load_current_records(path: str) -> Record:
    """Load current wins/losses from CSV."""
    records: Record = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = row['Team']
            wins = int(row['Wins'])
            losses = int(row['Losses'])
            records[team] = (wins, losses)
    return records


def load_pecota(path: str) -> Dict[str, int]:
    """Load PECOTA projected wins from CSV."""
    proj: Dict[str, int] = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            proj[row['Team']] = int(row['PecotaWins'])
    return proj


def load_schedule(path: str) -> Schedule:
    """Load remaining schedule from CSV."""
    sched: Schedule = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sched.append((row['HomeTeam'], row['AwayTeam']))
    return sched


def project_results(current: Record, pecota: Dict[str, int], schedule: Schedule) -> Record:
    """Return final projected records."""
    # Convert to mutable structures
    wins_remaining: Dict[str, int] = {}
    records: Record = {}
    for team, (w, l) in current.items():
        final_expected = pecota.get(team, w)
        wins_remaining[team] = max(final_expected - w, 0)
        records[team] = [w, l]  # mutable list [wins, losses]

    for home, away in schedule:
        home_need = wins_remaining.get(home, 0)
        away_need = wins_remaining.get(away, 0)

        if home_need == 0 and away_need == 0:
            # If neither team needs more wins, assign arbitrarily
            winner = home
        elif home_need >= away_need:
            winner = home
        else:
            winner = away

        loser = away if winner == home else home

        records[winner][0] += 1
        records[loser][1] += 1

        if wins_remaining.get(winner, 0) > 0:
            wins_remaining[winner] -= 1

    # Convert back to tuples
    final_records: Record = {team: (w_l[0], w_l[1]) for team, w_l in records.items()}
    return final_records


def main():
    # Example usage with placeholder paths
    current = load_current_records('teams.csv')
    pecota = load_pecota('pecota.csv')
    schedule = load_schedule('schedule.csv')

    final_records = project_results(current, pecota, schedule)
    for team, (w, l) in final_records.items():
        print(f"{team}: {w}-{l}")


if __name__ == '__main__':
    main()
