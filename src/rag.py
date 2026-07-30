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

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

FIELD_MATCH_THRESHOLD = 0.15

TITLE_COLUMN_PATTERN = re.compile(r"title|name|song", re.IGNORECASE)
IGNORED_EXPLANATION_COLUMNS = re.compile(r"^(id|index|idx|row)$", re.IGNORECASE)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


FEATURE_EMOJIS = {
    "genre": "🎼",
    "mood": "😊",
    "energy": "⚡",
    "tempo": "🥁",
    "bpm": "🥁",
    "valence": "🌈",
    "dance": "💃",
    "acoustic": "🎸",
    "artist": "🕺🏾",
    "year": "📅",
    "duration": "⏱️",
    "length": "⏱️",
}
DEFAULT_FEATURE_EMOJI = "✨"


def feature_emoji(column: str) -> str:
    """Best-effort emoji for a feature column name, falling back to a default."""
    lower = column.lower()
    for keyword, emoji in FEATURE_EMOJIS.items():
        if keyword in lower:
            return emoji
    return DEFAULT_FEATURE_EMOJI


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


VOWEL_RATIO_THRESHOLD = 0.25
VOWEL_RATIO_MIN_WORDS = 3
MIN_QUERY_LENGTH = 3


def is_gibberish(query: str) -> bool:
    """
    Heuristic check for nonsense input (keyboard mashing, random strings,
    too-short input) so the chatbot can decline to answer instead of
    guessing. Flags a query as gibberish if it has no alphabetic content,
    is too short to describe a mood meaningfully, if most of its words are
    long strings of consonants with no vowels, or (for phrases of 3+ words)
    if the overall vowel ratio is too low for real English text.
    """
    words = re.findall(r"[a-zA-Z]+", query)
    if not words:
        return True

    if len(query.strip()) < MIN_QUERY_LENGTH:
        return True

    def is_suspicious(word: str) -> bool:
        lower = word.lower()
        no_vowels = len(lower) >= 4 and not re.search(r"[aeiouy]", lower)
        repeated_char = re.search(r"(.)\1{3,}", lower) is not None
        return no_vowels or repeated_char

    suspicious = sum(1 for word in words if is_suspicious(word))
    if suspicious / len(words) > 0.5:
        return True

    if len(words) >= VOWEL_RATIO_MIN_WORDS:
        letters = "".join(words).lower()
        vowel_ratio = sum(1 for char in letters if char in "aeiouy") / len(letters)
        if vowel_ratio < VOWEL_RATIO_THRESHOLD:
            return True

    return False


def _field_embeddings(song: Dict) -> Dict[str, np.ndarray]:
    """Lazily embeds and caches each of a song's individual field values."""
    if "field_embeddings" not in song:
        fields = {
            column: str(value)
            for column, value in song["raw"].items()
            if column != "title"
            and not IGNORED_EXPLANATION_COLUMNS.match(column)
            and pd.notna(value)
        }
        if fields:
            model = _get_model()
            embeddings = model.encode(list(fields.values()))
            song["field_embeddings"] = dict(zip(fields.keys(), embeddings))
        else:
            song["field_embeddings"] = {}
    return song["field_embeddings"]


def explain_match(query: str, song: Dict) -> str:
    """
    Explains why a song matched by comparing the query's embedding against
    each of the song's individual field embeddings (genre, mood, etc.),
    citing whichever field(s) are most semantically similar for this
    specific song/query pair. This reflects the actual embedding-based
    retrieval signal, so explanations vary per song instead of repeating
    a generic fallback.
    """
    field_embeds = _field_embeddings(song)
    if not field_embeds:
        return "Similar overall vibe to your description"

    model = _get_model()
    query_embedding = model.encode([query])

    columns = list(field_embeds.keys())
    field_matrix = np.array([field_embeds[column] for column in columns])
    similarities = cosine_similarity(query_embedding, field_matrix).flatten()

    ranked = sorted(zip(columns, similarities), key=lambda pair: pair[1], reverse=True)
    top_fields = [column for column, score in ranked[:2] if score > FIELD_MATCH_THRESHOLD]

    if not top_fields:
        return "Similar overall vibe to your description"

    parts = [f"{column} ({song['raw'][column]})" for column in top_fields]
    return "Matched mainly on " + " and ".join(parts)
