import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Локальний шлях до файлу
local_file_path = "data/earthquake_1995-2023.csv"

# Завантаження даних
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


def display():
    # Заголовок сторінки
    st.title("Geographical Analysis of Earthquakes")

    
    try:
        data = load_data(local_file_path)
        #st.success("Data successfully loaded from the local file!")

        # Перевірка необхідних колонок
        required_columns = ['latitude', 'longitude', 'magnitude']
        if all(col in data.columns for col in required_columns):
            # Обробка пропущених значень
            data = data.dropna(subset=required_columns)

            # Карта розподілу землетрусів
            st.subheader("Map of Earthquake Magnitudes")
            map_center = [data['latitude'].mean(), data['longitude'].mean()]
            earthquake_map = folium.Map(location=map_center, zoom_start=2)

            # Додавання кластерів
            marker_cluster = MarkerCluster().add_to(earthquake_map)
            for _, row in data.iterrows():
                popup_text = f"Magnitude: {row['magnitude']}"
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=max(1, row['magnitude'] / 2),
                    color="red",
                    fill=True,
                    fill_opacity=0.6,
                    popup=popup_text,
                ).add_to(marker_cluster)

            # Відображення карти
            st_data = st_folium(earthquake_map, width=700, height=500)

            # Графік розсіювання
            st.subheader("Scatter Plot: Magnitude vs. Geographic Location")
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = sns.scatterplot(
                data=data,
                x='longitude',
                y='latitude',
                hue='magnitude',
                palette='coolwarm',
                size='magnitude',
                sizes=(20, 200),
                ax=ax
            )
            ax.set_title("Magnitude Distribution by Latitude and Longitude")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            plt.legend(loc='upper right', title="Magnitude")
            st.pyplot(fig)

            # Кореляція
            st.subheader("Correlation Analysis")
            corr_matrix = data[['latitude', 'longitude', 'magnitude']].corr()
            st.write("Correlation Matrix:")
            st.dataframe(corr_matrix)

        else:
            st.error("The dataset does not contain the required columns: latitude, longitude, magnitude.")

    except FileNotFoundError:
        st.error(f"The file was not found at the specified path: {local_file_path}")


    # Заголовок додатку
    st.title("Comparison of the number of earthquakes by country or continent")

    # Вибір групування: за країнами або континентами
    group_by_option = st.radio("Sort by:", ['Country', 'Continent'])

    # Групування та підрахунок
    if group_by_option == 'Country':
        data_grouped = data['country'].value_counts().dropna().head(10)  # Топ-10 країн
        ylabel = "Number of earthquakes"
        title = "Number of earthquakes by country (Top 10)"
    else:
        data_grouped = data['continent'].value_counts().dropna()
        ylabel = "Number of earthquakes"
        title = "Number of earthquakes by continent"

    # Побудова стовпчикової діаграми
    plt.figure(figsize=(10, 6))
    data_grouped.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.xlabel(group_by_option)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)

    # Відображення графіка у Streamlit
    st.pyplot(plt)