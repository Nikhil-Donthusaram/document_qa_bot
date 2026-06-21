import streamlit as st
from query_bot import ask_question

st.set_page_config(
    page_title="Document QA Bot",
    page_icon="📚"
)

st.title("📚 Document QA Bot")

question = st.text_input(
    "Ask a question from your documents"
)

if question:

    answer, sources = ask_question(question)

    st.subheader("🤖 Answer")
    st.write(answer)

    st.subheader("📌 Sources")

    if len(sources) == 0:
        st.write("No relevant sources found.")

    else:

        for source in sources:

            file_name, page = source.split("|")

            st.write(f"📄 {file_name}")
            st.write(f"📍 Page: {page}")
            st.write("---")

