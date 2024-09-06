import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import copy

# Load data
@st.cache(allow_output_mutation=True)
def load_data():
    # Load datasets
    customers = pd.read_csv(r'C:\Users\65917\Artificial Intelligence\EDA\music_customers.csv')
    listening_history = pd.read_excel(r'C:\Users\65917\Artificial Intelligence\EDA\music_listening_history.xlsx')
    audio = pd.read_excel('music_listening_history.xlsx', sheet_name=1)
    sessions = pd.read_excel('music_listening_history.xlsx', sheet_name=2)
    
    # Return deep copies of the data to avoid mutation issues
    return copy.deepcopy(customers), copy.deepcopy(listening_history), copy.deepcopy(audio), copy.deepcopy(sessions)

# Clean the customer data
def clean_data(customers):
    customers['Member Since'] = pd.to_datetime(customers['Member Since'])
    customers['Subscription Rate'] = pd.to_numeric(customers['Subscription Rate'].astype(str).str.replace('$', '', regex=False), errors='coerce')
    customers['Cancellation Date'] = pd.to_datetime(customers['Cancellation Date'])
    customers['Subscription Plan'] = customers['Subscription Plan'].fillna('Basic (Ads)')
    return customers

# Perform basic EDA
def eda(customers, listening_history, audio, sessions):
    st.write("### Customers Data")
    st.write(customers.head())

    st.write("### Listening History")
    st.write(listening_history.head())

    st.write("### Audio Data")
    st.write(audio.head())

    st.write("### Sessions Data")
    st.write(sessions.head())

    st.write("### Distribution of Customer Subscription Plans")
    st.bar_chart(customers['Subscription Plan'].value_counts())

    st.write("### Correlation Heatmap")
    corr = customers.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    st.pyplot(plt)

# Additional visualizations for customers
def visualize_customers(customers):
    st.write("### Distribution of Subscription Rates")
    fig, ax = plt.subplots()
    sns.histplot(customers['Subscription Rate'], bins=10, kde=True, ax=ax)
    st.pyplot(fig)

    st.write("### Customer Subscription Plan vs. Rate Boxplot")
    fig, ax = plt.subplots()
    sns.boxplot(x='Subscription Plan', y='Subscription Rate', data=customers, ax=ax)
    st.pyplot(fig)

# Main function to run the Streamlit app
def main():
    st.title("Customer Churn Reduction - EDA App")

    # Load and clean data
    customers, listening_history, audio, sessions = load_data()
    customers_cleaned = clean_data(customers)

    # Sidebar options for EDA
    st.sidebar.title("EDA Options")

    if st.sidebar.checkbox("Show Data Info"):
        eda(customers_cleaned, listening_history, audio, sessions)

    if st.sidebar.checkbox("Visualize Customers"):
        visualize_customers(customers_cleaned)

    if st.sidebar.checkbox("Show Correlations"):
        st.write("Correlation Matrix")
        st.write(customers_cleaned.corr())

# Run the app
if __name__ == '__main__':
    main()
