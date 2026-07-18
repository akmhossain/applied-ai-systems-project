"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def _wrap_reasons(explanation: str, width: int = 50) -> str:
    """Turns a '; '-joined explanation string into one bullet per line, wrapped to width."""
    lines = []
    for reason in explanation.split("; "):
        lines.extend(textwrap.wrap(f"- {reason}", width=width) or [f"- {reason}"])
    return "\n".join(lines)


def print_recommendations_table(recommendations) -> None:
    """Prints recommendations as a table including rank, title, artist, score, and reasons."""
    rows = [
        [rank, song["title"], song["artist"], f"{score:.2f}", _wrap_reasons(explanation)]
        for rank, (song, score, explanation) in enumerate(recommendations, start=1)
    ]
    headers = ["#", "Title", "Artist", "Score", "Reasons"]

    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        return

    # Fallback ASCII table when tabulate isn't installed (per-column, per-line max width)
    col_widths = []
    for i, header in enumerate(headers):
        max_len = len(header)
        for row in rows:
            for line in str(row[i]).split("\n"):
                max_len = max(max_len, len(line))
        col_widths.append(max_len)

    def format_row(cells):
        cell_lines = [str(cell).split("\n") for cell in cells]
        height = max(len(lines) for lines in cell_lines)
        out_lines = []
        for h in range(height):
            parts = []
            for i, lines in enumerate(cell_lines):
                text = lines[h] if h < len(lines) else ""
                parts.append(text.ljust(col_widths[i]))
            out_lines.append(" | ".join(parts))
        return "\n".join(out_lines)

    separator = "-+-".join("-" * w for w in col_widths)
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))
        print(separator)


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Additional example profiles for testing
    user_prefs_2 = {"genre": "rock", "mood": "angry", "energy": 0.9}
    user_prefs_3 = {"genre": "jazz", "mood": "relaxed", "energy": 0.4, "tempo_bpm": 90.0}
    user_prefs_4 = {"genre": "chill lofi", "mood":"relaxed", "energy":0.3, "tempo_bpm":70.0}
    user_prefs_5 = {"genre": "breakup", "mood":"sad", "energy":0.2, "tempo_bpm":55.0}

    # Edge case profiles
    user_prefs_6 = {"genre": "pop", "mood": "sad", "energy": 0.9}  # conflicting: high energy + sad mood
    user_prefs_7 = {"genre": "pop", "mood": "happy", "energy": 1.5}  # energy above valid 0-1 range
    user_prefs_8 = {"genre": "rock", "mood": "angry", "energy": -0.5}  # negative energy
    user_prefs_9 = {}  # empty preferences
    user_prefs_10 = {"genre": "pop", "mood": "happy", "energy": 0.5, "tempo_bpm": 400.0}  # tempo far outside real song range
    user_prefs_11 = {"genre": "xyz-not-a-genre", "mood": "not-a-mood", "energy": 0.5}  # genre/mood not in dataset

    all_profiles = [
        user_prefs, user_prefs_2, user_prefs_3, user_prefs_4, user_prefs_5,
        user_prefs_6, user_prefs_7, user_prefs_8, user_prefs_9, user_prefs_10, user_prefs_11,
    ]

    for prefs in all_profiles:
        recommendations = recommend_songs(prefs, songs, k=5)

        print(f"\nTop Recommendations for {prefs}")
        print("=" * 40)
        print_recommendations_table(recommendations)


if __name__ == "__main__":
    main()
