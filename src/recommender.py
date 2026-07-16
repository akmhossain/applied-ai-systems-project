import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_artists: List[str]
    target_tempo_bpm: float
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def _norm_tempo(tempo_bpm: float, max_tempo: float = 200.0) -> float:
    """Scales a tempo in BPM to a 0-1 range so it's comparable to other normalized features."""
    return tempo_bpm / max_tempo

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Follows the weighted formula from the README's "How The System Works" section:
    genre (0.3), mood (0.3), artist (0.15), energy (0.15), tempo (0.1).
    """
    genre_match = 1 if song["genre"] == user_prefs.get("genre") else 0
    mood_match = 1 if song["mood"] == user_prefs.get("mood") else 0
    artist_match = 1 if song["artist"] == user_prefs.get("artist") else 0

    energy_target = user_prefs.get("energy")
    energy_score = 1 - abs(song["energy"] - energy_target) if energy_target is not None else 0

    tempo_target = user_prefs.get("tempo_bpm")
    tempo_score = (
        1 - abs(_norm_tempo(song["tempo_bpm"]) - _norm_tempo(tempo_target))
        if tempo_target is not None else 0
    )

    contributions = {
        "genre": 0.3 * genre_match,
        "mood": 0.3 * mood_match,
        "artist": 0.15 * artist_match,
        "energy": 0.15 * energy_score,
        "tempo": 0.1 * tempo_score,
    }

    score = sum(contributions.values())

    ranked = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
    reasons = []
    for feature, contribution in ranked:
        if contribution <= 0:
            continue
        if feature == "genre":
            reasons.append(f"Matches your favorite genre '{song['genre']}' (+{contribution:.2f})")
        elif feature == "mood":
            reasons.append(f"Matches your favorite mood '{song['mood']}' (+{contribution:.2f})")
        elif feature == "artist":
            reasons.append(f"By one of your favorite artists '{song['artist']}' (+{contribution:.2f})")
        elif feature == "energy":
            reasons.append(f"Energy ({song['energy']}) is close to your target (+{contribution:.2f})")
        elif feature == "tempo":
            reasons.append(f"Tempo ({song['tempo_bpm']} bpm) is close to your target (+{contribution:.2f})")

    if not reasons:
        reasons.append("No strong matches with your preferences")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        results.append((song, score, explanation))

    results.sort(key=lambda result: result[1], reverse=True)
    return results[:k]
