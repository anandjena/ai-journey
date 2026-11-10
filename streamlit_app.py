import os
import chromadb
import streamlit as st

try :
    os.environ['GEMINI_API_KEY'] = st.secrets['GEMINI_API_KEY']
except Exception:
    pass

from reg import answer_question
from build_index import build_index

@st.cache_resource
def ensure_index():
    client = chromadb.PersistentClient(path='./chroma_db')

    try:
        if client.get_collection('knowledge').count() > 0:
            return 'ready'
    except Exception:
        pass

    build_index()
    return "built"

st.title("Policy Support Docs")
st.caption("Ask about shipping, returns, refunds, cancellations or wrranty. ")

with st.spinner("Preparing the knowledge base (first start only)... "):
    ensure_index()

if "count" not in st.session_state:
    st.session_state.count = 0

question = st.text_input("Your question")

if st.button("Ask") and question.strip():
    if st.session_state.count > 10:
        st.warning("Demo limit reached for this session (10 questions) .")
        st.stop()
    st.session_state.count += 1

    with st.spinner("Thinking..."):
        answer, matches = answer_question(question)

        if answer is None:
            st.error("The model is busy right now. Please try again after in a minute.")
        else:
            st.subheader("Answer")
            st.write(answer)

            if matches:
                with st.expander("Sources"):
                    for score, docs in matches:
                        st.write(f"**Score{score:.3f}**")
                        st.write(docs)