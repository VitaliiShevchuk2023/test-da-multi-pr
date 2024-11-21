import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# Завантаження даних
@st.cache_data
def load_data():
    return pd.read_csv('data/earthquake_1995-2023.csv')



def display():

    data = load_data()
    
    # Перетворення колонки з датами на формат datetime
    data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')
    # Додавання колонки для року
    data['year'] = data['date_time'].dt.year

    st.title("Earthquake Trends Analysis")

    # Заголовок додатку
    st.title("Histogram of earthquake magnitude distribution")

    # Вибір року
    years = sorted(data['year'].dropna().unique())
    selected_year = st.selectbox("Select a year", years)

    # Фільтрація даних за вибраним роком
    filtered_data = data[data['year'] == selected_year]

    # Побудова гістограми
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_data['magnitude'], bins=20, color='skyblue', edgecolor='black')
    plt.title(f"Distribution of earthquake magnitudes in {selected_year}")
    plt.xlabel("Magnitude")
    plt.ylabel("Count")

    # Відображення гістограми у Streamlit
    st.pyplot(plt)

    st.title("Trend in the number of earthquakes by year")

    # Кількість землетрусів за роками
    yearly_counts = data.groupby('year').size()

    # Візуалізація
    fig, ax = plt.subplots(figsize=(10, 6))
    yearly_counts.plot(kind='line', ax=ax)
    ax.set_title("Number of Earthquakes Per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Горизонтальна таблиця
    st.write("Earthquake Counts by Year:")
    st.dataframe(yearly_counts.reset_index().T)


    # Створення інтерфейсу в Streamlit
    st.title("Statistical Analysis of Earthquake Data")

    # Вибір стовпця для аналізу
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    selected_column = st.selectbox("Select a numeric column for analysis:", numeric_columns)

    if selected_column:
        # Розрахунок статистичних показників
        col_data = data[selected_column].dropna()  # Видалення відсутніх значень
        stats = {
            "Mean": col_data.mean(),
            "Median": col_data.median(),
            "Mode": col_data.mode()[0] if not col_data.mode().empty else None,
            "Minimum": col_data.min(),
            "Maximum": col_data.max(),
            "Standard Deviation": col_data.std(),
            "Variance": col_data.var(),
            "Count": col_data.count(),
        }

        # Вивід результатів у вигляді таблиці
        stats_df = pd.DataFrame(stats.items(), columns=["Statistic", "Value"])
        st.write("### Statistical Summary")
        st.dataframe(stats_df)

        # Додаткова візуалізація: гістограма розподілу
        st.write("### Distribution of the Selected Column")
        st.bar_chart(col_data.value_counts().sort_index())
    else:
        st.write("Please select a numeric column for analysis.")