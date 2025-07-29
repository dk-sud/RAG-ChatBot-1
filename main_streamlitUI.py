from pathlib import Path
import streamlit as st
from faq_data_ings_pipeline import faq_ingestion, chain_query_context
from sql_pipeline import chain_sql_query_and_context
from sql_faq_router import router


file_path = Path(__file__).parent / 'resources' / 'faq_data.csv'
faq_ingestion(file_path)


def ask(query):
    route = router(query).name #type: ignore
    if route == 'faq':
        return chain_query_context(query)
    elif route == 'sql':
        return chain_sql_query_and_context(query)
    else:
        return f"{query} not in the lib"
    

st.title('e-commerce ai-bot')
query = st.chat_input("how can I help?")


if "messages" not in st.session_state:
    st.session_state['messages'] = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if query:
    with st.chat_message('user'):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    response = ask(query)
    with st.chat_message('assistant'):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
