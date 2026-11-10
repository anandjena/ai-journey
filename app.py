import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.title("Policy Support Bot")
st.caption("Ask about shipping, returns, refunds, cancellations or warranty.")

question = st.text_input("Your question")

if st.button("Ask") and question.strip():
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, json={"question":question}, timeout=90)
        except requests.RequestException:
            st.error("Could not reach the API. Is the server running?")
            st.stop()
    if response.status_code == 200:
        data = response.json()
        st.subheader("Answer")
        st.write(data['answer'])

        if data['sources']:
            with st.expander("Sources"):
                for s in data['sources']:
                    st.write(f"**Score {s['score']}**")
                    st.write(s['text'])
        else:
            st.error(f"Error {response.status_code}: {response.text}")