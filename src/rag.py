"""
Retrieval pipeline for MaestroMix.

Lets a user upload a loosely-formatted CSV of songs and retrieve the
top matches for a free-text mood query using local semantic embeddings
(sentence-transformers) + cosine similarity. Runs fully offline/free,
so queries can match songs by meaning even when the exact words in
the query don't literally appear in the uploaded file.
"""

import re
from functools import lru_cache
from typing import Dict, List, Tuple

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

TITLE_COLUMN_PATTERN = re.compile(r"title|name|song", re.IGNORECASE)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def _find_title_column(columns: List[str]) -> str:
    for column in columns:
        if TITLE_COLUMN_PATTERN.search(column):
            return column
    return columns[0]


def parse_uploaded_songs(file) -> List[Dict]:
    """
    Reads an uploaded CSV into a list of songs. Only assumption: there's a
    title-like column. Every column's values are joined into one text blob
    per row, which becomes the document retrieval matches against.
    """
    df = pd.read_csv(file)
    if df.empty:
        return []

    title_column = _find_title_column(list(df.columns))

    songs = []
    for _, row in df.iterrows():
        raw = row.to_dict()
        text = " ".join(str(value) for value in raw.values() if pd.notna(value))
        songs.append({
            "title": str(raw.get(title_column, "Unknown")),
            "raw": raw,
            "text": text,
        })
    return songs


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    """Loads the embedding model once and reuses it across calls."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def build_index(songs: List[Dict]):
    """Embeds each song's text blob, returning a matrix of embeddings."""
    model = _get_model()
    return model.encode([song["text"] for song in songs])


def retrieve(query: str, matrix, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float]]:
    """Returns the top-k songs ranked by cosine similarity to the query."""
    model = _get_model()
    query_vector = model.encode([query])
    similarities = cosine_similarity(query_vector, matrix).flatten()

    ranked_indices = similarities.argsort()[::-1][:k]
    return [(songs[i], float(similarities[i])) for i in ranked_indices]


def is_gibberish(query: str) -> bool:
    """
    Heuristic check for nonsense input (keyboard mashing, random strings)
    so the chatbot can decline to answer instead of guessing. Flags a query
    as gibberish if it has no alphabetic content, or if most of its words
    are long strings of consonants with no vowels.
    """
    words = re.findall(r"[a-zA-Z]+", query)
    if not words:
        return True

    def is_suspicious(word: str) -> bool:
        lower = word.lower()
        no_vowels = len(lower) >= 4 and not re.search(r"[aeiouy]", lower)
        repeated_char = re.search(r"(.)\1{3,}", lower) is not None
        return no_vowels or repeated_char

    suspicious = sum(1 for word in words if is_suspicious(word))
    return suspicious / len(words) > 0.5


def explain_match(query: str, song: Dict) -> str:
    """
    Best-effort explanation of why a song matched. Since matching is based on
    semantic embeddings (not literal keywords), this looks for any of the
    song's own field values that literally overlap with words in the query;
    if nothing overlaps, the match was found by overall meaning rather than
    shared words.
    """
    query_words = {word for word in re.findall(r"\w+", query.lower()) if len(word) > 2}

    overlaps = []
    for column, value in song["raw"].items():
        if column == "title" or pd.isna(value):
            continue
        value_str = str(value).lower()
        if any(word in value_str for word in query_words):
            overlaps.append(f"{column}: {value}")

    if overlaps:
        return "Matches " + ", ".join(overlaps[:2])
    return "Similar overall vibe to your description"
