"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


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
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}")
            print("   Reasons:")
            for reason in explanation.split("; "):
                print(f"     - {reason}")


if __name__ == "__main__":
    main()
