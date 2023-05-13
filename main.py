import streamlit as st
import random as rd
from ask_seneca import Seneca

st.set_page_config(
    page_title="Seneca",
    page_icon="img/seneca_emoji.png",
)

@st.cache_resource
def seneca():
    seneca = Seneca(
        openai_api_key=st.secrets['OPENAI_API_KEY'],
        pinecone_api_key=st.secrets['PINECONE_API_KEY'],
        pinecone_api_env=st.secrets['PINECONE_API_ENV'],
    )
    return seneca

DEFAULT_QUESTIONS = [
    'Quali sono le caratteristiche di un buon amico?',
    'Quale è la più importante virtù?',
    'Come posso essere felice?',
    'Cosa devo fare per acquistare la serenità?',
]

if 'question' not in st.session_state:
    st.session_state.question = ''
    

col1, col2, col3 = st.columns([1, 4, 1])

with col1:

    st.write('')

with col2:

    col2_1, col2_2, col2_3 = st.columns([1, 2, 1])

    with col2_1:
            
        st.write('')    

    with col2_2:
             
        st.title('Ask Seneca')
        st.image('img/seneca_emoji.png', width=200)

    with col2_3:
         
        st.write('')

    answer = None

    question_input = st.session_state.question = st.text_area(label='Chiedi qualcosa a Seneca',
                                                value=st.session_state.question,
                                                height=100)

    col2_1, col2_2 = st.columns([2, 1])

    with col2_1:

        if st.button('Non sono sicuro di cosa chiedere',
                     key='default_question'):
            
            st.session_state.question = rd.choice(DEFAULT_QUESTIONS)
            st.experimental_rerun()
            
    
    with col2_2:

        ask_ok = False

        if st.button('Chiedi a Seneca',
                      key='ask_seneca'):

            ask_ok = True
        
    if ask_ok:

        if st.session_state.question:
            
            with st.spinner('Sto elucubrando...'):
                answer = seneca().ask(st.session_state.question)

    if answer:
            
        st.write(answer)
            



with col3:
    
    st.write('')


