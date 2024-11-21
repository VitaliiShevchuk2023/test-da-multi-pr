import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Завантаження даних
@st.cache_data
def load_data():
    return pd.read_csv('data/earthquake_1995-2023.csv')


def display():
    
    data = load_data()

    # Заголовок додатку
    st.title("Scattering: Magnitude versus depth of earthquakes")

    # Побудова графіка розсіювання
    plt.figure(figsize=(10, 6))
    plt.scatter(data['depth'], data['magnitude'], alpha=0.5, c='skyblue', edgecolor='k')
    plt.title("Dependence of magnitude on earthquake depth")
    plt.xlabel("Depth (km)")
    plt.ylabel("Magnitude")
    plt.grid(True)

    # Відображення графіка у Streamlit
    st.pyplot(plt)


    st.title("Tsunami vs Depth and Magnitude")

    # Видалення пропущених значень
    filtered_data = data.dropna(subset=['tsunami', 'magnitude', 'depth'])

    # Графік розсіювання
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(
        filtered_data[filtered_data['tsunami'] == 0]['depth'], 
        filtered_data[filtered_data['tsunami'] == 0]['magnitude'], 
        color='blue', label='No Tsunami', alpha=0.5
    )
    ax.scatter(
        filtered_data[filtered_data['tsunami'] == 1]['depth'], 
        filtered_data[filtered_data['tsunami'] == 1]['magnitude'], 
        color='red', label='Tsunami', alpha=0.7
    )
    ax.set_title("Tsunami Occurrence Based on Depth and Magnitude")
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("Magnitude")
    ax.legend()
    st.pyplot(fig)