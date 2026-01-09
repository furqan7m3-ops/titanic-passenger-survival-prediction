import streamlit as st
import requests
st.title("Titanic Passenger Survival Prediction")

if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

if st.session_state['form_submitted']==False:
    st.markdown('Enter passenger details:')
    with st.form('passenger-form', clear_on_submit=True):
        age = st.number_input('Age', min_value=0, max_value=120, value=0, step=0)
        sibsp = st.number_input('Siblings & spouse', min_value=0, value=0)
        parch = st.number_input('Parent & children', min_value=0, value=0)
        sex = st.radio('Sex', options=['male','female'])
        fare = st.number_input('Fare', min_value=0.1, value=0.1, step=0.1, format='%.2f')
        deck = st.selectbox('Deck', options=['A','B','C','D','E','F','G'])
        pclass = st.selectbox('Passenger\'s Class', options=('First','Second','Third'))
        embarked = st.selectbox('Embarked', options=('C','Q','S'))
        submitted=st.form_submit_button('Submit')

    if submitted:
        st.session_state['form_submitted'] = True
        st.session_state['age'] = age
        st.session_state['sibsp'] = sibsp
        st.session_state['parch'] = parch
        st.session_state['sex'] = sex
        st.session_state['fare'] = fare
        st.session_state['deck'] = deck
        st.session_state['pclass'] = pclass
        st.session_state['embarked'] = embarked

if st.session_state['form_submitted']:
    st.success('Form Submitted')
    st.write('### Choose Model for prediction')
    model = st.radio('Select Model', options=('Random Forest', 'Logistic Regression'))
    btn = st.button('Predict Survival')
    endpoint=None
    if model == 'Random Forest':
        endpoint = 'http://localhost:8000/random-forest/predict'
    else:
        endpoint = 'http://localhost:8000/logistic-regression/predict'
    if btn:
        response=requests.post(endpoint, json={
            'age':st.session_state['age'],
            'sex':st.session_state['sex'],
            'parch': st.session_state['parch'],
            'sibsp':st.session_state['sibsp'],
            'fare':st.session_state['fare'],
            'deck':st.session_state['deck'],
            'pclass':st.session_state['pclass'],
            'embarked':st.session_state['embarked']
        })
        if response.status_code==200:
            st.write("### Prediction Result:")
            prediction=response.json()['prediction']
            if prediction==1:
                st.success('**Passenger Survived**')
            else:
                st.error('**Passenger Not Survived**')
            
        else:
            st.error('Error in prediction API call.')