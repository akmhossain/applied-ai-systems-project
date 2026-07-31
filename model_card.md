# 🎧 Model Card: MixMaster

## 1. Model Name  

MixMaster

---

## 2. Intended Use  

MixMaster is built for users who have their own collection of songs (any CSV with a title-like column, no fixed schema required) and want recommendations based on a free-text mood description instead of picking values from a fixed set of genres/moods. A user uploads their playlist and describes what they want to listen to in plain language (e.g. "chill acoustic songs for studying"); MixMaster retrieves the top matches from that uploaded file. The model is NOT for discovering songs outside the uploaded file — it can only retrieve and rank songs the user has already provided, and it is not designed for precise, exact-value filtering (e.g. "songs at exactly 120 bpm"), since matching is semantic and approximate rather than rule-based.

---

## 3. How the Model Works  

MixMaster is a retrieval-augmented (RAG) system, not a fixed-weight formula. Each uploaded song's non-title fields (genre, mood, artist, energy, etc.) are combined into a single text blob and converted into a numerical embedding using a local `sentence-transformers` model (`all-MiniLM-L6-v2`) — no API calls or internet connection required after the model's first download. The user's mood query is embedded the same way, and songs are ranked by cosine similarity between the query embedding and each song's embedding. Separately, a per-field embedding comparison generates each result's explanation by identifying which individual field (genre, mood, artist, etc.) most closely matches the query for that specific song. Before retrieval runs, a lightweight guardrail (`is_gibberish`) checks the query for nonsense input — too-short text, keyboard mashing, or an abnormally low vowel ratio — and declines to answer rather than returning arbitrary results.

---

## 4. Strengths  

MixMaster performs well on natural-language mood queries, since it matches on meaning rather than requiring exact keyword overlap — a query like "songs for a rainy day" can surface relevant songs even if none of their fields literally contain those words. Because the pipeline makes no assumptions about column names beyond a title-like field, it adapts automatically to different uploaded playlists (verified against both `data/songs.csv` and `data/songs2.csv`) without any code changes. Explanations are generated per song rather than being a single generic message, so a user can see specifically which field (genre, mood, artist, etc.) drove each result. The gibberish guardrail also reliably catches many common non-answerable inputs — very short text and obvious keyboard mashing — before wasting a retrieval call on them.

---

## 5. Limitations and Bias 

**Limitations:** MixMaster struggles with complex or nuanced mood descriptions (e.g. "eecentric with a hint of sadness" returned low-confidence, inconsistent matches) and with short nonsense inputs that happen to contain a vowel (e.g. "soos" slipped past the `is_gibberish` guardrail). It also relies entirely on the quality of the uploaded file — vague or inconsistently-labeled fields degrade both retrieval and explanations — and can reproduce whatever bias already exists in a playlist's own genre/mood labels rather than correct for it.

**Potential misuse:** There is minimal misuse potential here. MixMaster runs entirely locally, uses a small general-purpose embedding model with no generative capabilities, and only retrieves/ranks songs the user themselves uploaded — there's no way for it to produce or spread new content, and no external API or data source for it to abuse.

---

## 6. Future Work  

In the future, I would like the model to handle the edge cases mentioned in the previous section. I would also like to make the model dynamic, adding an option for the user to rank the features they value the most and introduce a more robust LLM. In general, I want to work to improve prompt recognition and fulfill more complex user requests.

---

## 7. Personal Reflection

Throughout this project AI was helpful at planning and brainstorming workfolows for this project. It also helped with understanding new parts of code. However, AI was flawed when it came to identifying bugs or implementing guardrails.
