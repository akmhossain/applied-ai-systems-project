"""
MaestroMix - a chatbot that retrieves songs from a user-uploaded file
based on a free-text mood description.
"""

import streamlit as st

from rag import build_index, explain_match, is_gibberish, parse_uploaded_songs, retrieve

st.set_page_config(page_title="MaestroMix", page_icon="🎵")
st.title("🎵 MaestroMix")
st.caption("Upload your playlist, then describe what you want to listen to today. Consider title,artist,genre,mood,energy).")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "index" not in st.session_state:
    st.session_state.index = None

uploaded_file = st.file_uploader("Upload a CSV of songs", type="csv")

if uploaded_file is not None and st.session_state.get("uploaded_name") != uploaded_file.name:
    songs = parse_uploaded_songs(uploaded_file)
    if songs:
        with st.spinner("Uploading your songs..."):
            matrix = build_index(songs)
        st.session_state.index = {"songs": songs, "matrix": matrix}
        st.session_state.uploaded_name = uploaded_file.name
        st.session_state.messages = []
        st.success(f"Loaded {len(songs)} songs from {uploaded_file.name}.")
    else:
        st.error("That file doesn't have any rows to work with.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.index is None:
    st.chat_input("Upload a song file to start chatting", disabled=True)
else:
    query = st.chat_input("Describe your mood (e.g. \"upbeat happy songs for a road trip\")")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        if is_gibberish(query):
            reply = "🤔 I couldn't quite understand that — try describing your mood in a few plain words (e.g. \"chill acoustic songs for studying\")."
        else:
            index = st.session_state.index
            results = retrieve(query, index["matrix"], index["songs"], k=5)
            matches = [song for song, score in results if score > 0]

            if not matches:
                reply = "😕 I couldn't find any songs in your file matching that mood."
            else:
                extra_columns = [k for k in matches[0]["raw"].keys() if k != "title"][:3]
                header = ["🎵 Title"] + [f"✨ {column.title()}" for column in extra_columns] + ["💡 Why"]
                rows = [
                    [song["title"]]
                    + [str(song["raw"].get(column, "")) for column in extra_columns]
                    + [explain_match(query, song)]
                    for song in matches
                ]

                lines = [f"🎧 Here are the top {len(matches)} choices from your playlist:", "", "| " + " | ".join(header) + " |"]
                lines.append("| " + " | ".join(["---"] * len(header)) + " |")
                for row in rows:
                    lines.append("| " + " | ".join(row) + " |")
                reply = "\n".join(lines)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
