import streamlit as st
from query_bot import ask_question

st.set_page_config(
    page_title="AI Document Q&A",
    page_icon="📚",
    layout="wide"
)

# ---------- HEADER ----------
st.title("📚 AI Document Q&A Assistant")
st.caption("Ask questions from your PDFs with page-level citations")

# ---------- INPUT ----------
query = st.text_input("🔎 Enter your question")

# ---------- BUTTON ----------
if st.button("Ask"):

    if query.strip():

        with st.spinner("Thinking... 🤖"):

            answer, sources = ask_question(query)

        # ---------- ANSWER ----------
        st.markdown("## 🤖 Answer")
        st.success(answer)

        # ---------- SOURCES ----------
        st.markdown("## 📌 Sources")

        if sources:

            for s in sources:
                file, page = s.split("|")   # SAFE SPLIT

                st.markdown(f"""
📄 **{file}**  
📍 Page: `{page}`
""")

                st.markdown("---")

        else:
            st.warning("No sources found")

    else:
        st.error("Please enter a question")

