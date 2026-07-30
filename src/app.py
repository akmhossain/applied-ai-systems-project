"""
MaestroMix - a chatbot that retrieves songs from a user-uploaded file
based on a free-text mood description.
"""

import streamlit as st

from rag import (
    IGNORED_EXPLANATION_COLUMNS,
    build_index,
    explain_match,
    feature_emoji,
    is_gibberish,
    parse_uploaded_songs,
    retrieve,
)

MAX_DISPLAYED_FEATURES = 6

st.set_page_config(page_title="MaestroMix", page_icon="🎵")

st.markdown('<div id="top"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <a href="#top" title="Back to top" style="
        position: fixed; bottom: 24px; right: 24px; z-index: 1000;
        background-color: transparent; color: inherit; text-decoration: none;
        border: 1px solid rgba(128,128,128,0.4); padding: 8px 14px;
        border-radius: 20px; display: flex; align-items: center;
        gap: 6px; font-size: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    ">⬆️ Back to Top</a>
    """,
    unsafe_allow_html=True,
)

st.title("🎵 MaestroMix")
st.caption("Upload your playlist, then describe what you want to listen to today. Consider title,artist,genre,mood,energy).")

if "index" not in st.session_state:
    st.session_state.index = None
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None
if "next_chat_id" not in st.session_state:
    st.session_state.next_chat_id = 1


def create_chat():
    chat_id = st.session_state.next_chat_id
    st.session_state.next_chat_id += 1
    st.session_state.chats[chat_id] = {"name": "New Chat", "messages": []}
    st.session_state.active_chat_id = chat_id


if not st.session_state.chats:
    create_chat()

with st.sidebar:
    st.header("💬 Chat Log")
    if st.button("➕ New Chat", use_container_width=True):
        create_chat()

    chat_ids = list(reversed(st.session_state.chats.keys()))
    labels = {chat_id: st.session_state.chats[chat_id]["name"] for chat_id in chat_ids}
    active_id = st.radio(
        "Your chats",
        options=chat_ids,
        format_func=lambda chat_id: labels[chat_id],
        index=chat_ids.index(st.session_state.active_chat_id),
        label_visibility="collapsed",
    )
    st.session_state.active_chat_id = active_id

active_chat = st.session_state.chats[st.session_state.active_chat_id]

uploaded_file = st.file_uploader("Upload a CSV of songs", type="csv")

if uploaded_file is not None and st.session_state.get("uploaded_name") != uploaded_file.name:
    songs = parse_uploaded_songs(uploaded_file)
    if songs:
        with st.spinner("Uploading your songs..."):
            matrix = build_index(songs)
        st.session_state.index = {"songs": songs, "matrix": matrix}
        st.session_state.uploaded_name = uploaded_file.name
        active_chat["name"] = uploaded_file.name
        st.success(f"Loaded {len(songs)} songs from {uploaded_file.name}.")

        feature_columns = [
            column
            for column in songs[0]["raw"].keys()
            if column != "title" and not IGNORED_EXPLANATION_COLUMNS.match(column)
        ][:MAX_DISPLAYED_FEATURES]
        if feature_columns:
            feature_list = "\n".join(
                f"- {feature_emoji(column)} {column.title()}" for column in feature_columns
            )
            st.info("Features that will be used to determine your top picks:\n\n" + feature_list)
    else:
        st.error("That file doesn't have any rows to work with.")

if st.session_state.index is not None:
    result_count = st.slider("How many songs should I suggest?", min_value=1, max_value=10, value=5)

for message in active_chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.index is None:
    st.chat_input("Upload a song file to start chatting", disabled=True)
else:
    query = st.chat_input("Describe your mood (e.g. \"upbeat happy songs for a road trip\")")
    if query:
        active_chat["messages"].append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        if is_gibberish(query):
            reply = "🤔 I couldn't quite understand that — try describing your mood in a few plain words (e.g. \"chill acoustic songs for studying\")."
        else:
            index = st.session_state.index
            with st.spinner("Finding your top matches..."):
                results = retrieve(query, index["matrix"], index["songs"], k=result_count)
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

        active_chat["messages"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
