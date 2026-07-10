# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

In the real world, companies have two main ways of predicting what a user will want next: collaborative filtering and content-based filtering. Collaborative filetering involves making predictions primarily based on what other users like. On the other hand, content-based filtering only focuses on what the user prefers and the attributes of the content itself. By using user data like genre, mood, tempo, oe user history, the models are able to provide predictions on what the user will like next. Each feature also has a weight attached, based on how important that feature is in making the prediction. In my version of the AI reccomender, I want to prioritize genre, mood, energy, and tempo/bpm. I think these are the most deterministic aspects of a piece, and will provide clearer reccomendations to the user.

These are the attributes that Song and UserProfile will use:
Song - artist: str, genre: str, mood: str, energy: float, tempo_bpm: float
UserProfile - favorite_artists: list, avg_tempo: list, favorite_genre: str, favorite_mood: str, target_energy: float

In the How The System Works section, write a short paragraph explaining your understanding of how real-world recommendations work and what your version will prioritize.
List the specific features your Song and UserProfile objects will use in your simulation.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - It stores the id/title, artist, genre, mood, energy, and bpm of the song
- What information does your `UserProfile` store
  - It stores the favorite artists, target bpm, favorite genres, favorite mood, and target_energy
- How does your `Recommender` compute a score for each song
  - For each song the reccomender will compute a score in between 0.0 and 1.0. 1.0 means the song is a perfect match. Based on the user's preferences, the reccomender will compute a score. Each feature has a different weight, so some will be weighed more than others. Genre and mood will be weighed twice as much as the other features, which may lead my model to underestimate the other features like energy and tempo. Below is the formula I will implement: 
  score = (
    0.3  * (1 if song.genre  == user.preferred_genre  else 0) +
    0.3   * (1 if song.mood   == user.preferred_mood   else 0) +
    0.15 * (1 if song.artist == user.preferred_artist else 0) +
    0.15 * (1 - abs(song.energy - user.preferred_energy)) +
    0.1  * (1 - abs(norm_tempo(song.tempo_bpm) - norm_tempo(user.preferred_tempo)))
    )

- How do you choose which songs to recommend
  I will store the scores of all the songs in a list. Then, the list will be sorted in descending order. The top songs will be the ones that are recommended.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



