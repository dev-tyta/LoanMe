import streamlit as st
import pickle

voting_pickle = open('voting_ensemble.pickle', 'rb')
map_pickle = open('output_result.pickle', 'rb')

voting_clf = pickle.load(voting_pickle)
unique_mapping = pickle.load(map_pickle)

st.title('Loan Availability Prediction')
st.write('Intro...... ')

gender = st.selectbox('Pick your Gender:', ['Female', 'Male'])

married = st.selectbox('Marital Status:', ['Married', 'Single'])

dependent = st.selectbox('Are you dependent on anyone:', ['Yes', 'No'])

education = st.selectbox('Educational Background:', ['Graduate', 'Non-Graduate'])

employed = st.selectbox('Employment Status:', ['Self-Employed', 'Employed'])

base_currency = st.selectbox('Base Currency:', ['NGN', 'USD', 'EURO'])

app_income = st.number_input('Applicant Income:').is_integer()

if base_currency == 'NGN':
    dol_income = app_income / 570
elif base_currency == 'USD':
    dol_income = app_income
elif base_currency == 'EURO':
    dol_income = app_income * 0.877

co_income = st.number_input('Side Income ny Applicant:').is_integer()

if base_currency == 'NGN':
    dol_co_income = co_income / 570
elif base_currency == 'USD':
    dol_co_income = co_income
elif base_currency == 'EURO':
    dol_co_income = co_income * 0.877

loan_amount = st.number_input('Amount you would love to borrow:').is_integer()


# Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome,\
# Co-applicant Income, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area
