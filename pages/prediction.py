import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns

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

    st.title("Earthquake Prediction for 2025–2030 Using Machine Learning")

    # Підготовка даних
    earthquakes_per_year = data.groupby('year').size().reset_index()
    earthquakes_per_year.columns = ['Year', 'Earthquake_Count']

    # Розділення даних на ознаки (X) та цільову змінну (y)
    X = earthquakes_per_year[['Year']].values  # Роки
    y = earthquakes_per_year['Earthquake_Count'].values  # Кількість землетрусів

    # Розділення даних на тренувальну та тестову вибірки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Ініціалізація моделі лінійної регресії
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Прогнозування на тестових даних
    y_pred = model.predict(X_test)

    # Оцінка моделі
    mse = mean_squared_error(y_test, y_pred)
    st.write(f"Mean Squared Error (MSE): {mse:.2f}")

    # Прогнозування на 2025–2030 роки
    future_years = np.array([[2025], [2026], [2027], [2028], [2029], [2030]])
    future_predictions = model.predict(future_years)

    # Виведення прогнозів
    predictions_df = pd.DataFrame({
        "Year": future_years.flatten(),
        "Predicted_Earthquakes": future_predictions.astype(int)
    })
    st.write("### Predictions for 2025–2030")
    st.dataframe(predictions_df)

    # Візуалізація
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Historical Data')
    plt.plot(X, model.predict(X), color='red', label='Regression Line')
    plt.scatter(future_years, future_predictions, color='green', label='Future Predictions')
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.title('Earthquake Predictions (2025–2030)')
    plt.legend()
    st.pyplot(plt)

    # Заголовок
    st.title("K-Means Clustering for Earthquake Dataset")

    # Вибір змінних для кластеризації
    st.header("Clustering Parameters")
    selected_columns = st.multiselect(
        "Select columns for clustering:", 
        data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    )

    # Вибір кількості кластерів
    n_clusters = st.slider("Number of Clusters (k):", min_value=2, max_value=10, value=3)

    if selected_columns:
        # Підготовка даних
        clustering_data = data[selected_columns].dropna()
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clustering_data)
        
        # K-Means моделювання
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clustering_data['Cluster'] = kmeans.fit_predict(scaled_data)
        
        # Виведення кластерної статистики
        st.subheader("Cluster Statistics")
        st.write(clustering_data.groupby('Cluster').mean())
        
    # Візуалізація кластерів 
    if len(selected_columns) == 2:  # Якщо обрано рівно 2 змінні
        st.subheader(f"Visualization of Clusters (k={n_clusters})")
        
        # Перевірка на пропущені значення
        if clustering_data[selected_columns].isnull().any().any():
            st.warning("Selected columns contain missing values. Removing rows with NaN.")
            clustering_data = clustering_data.dropna(subset=selected_columns)
        
        # Перевірка чи дані доступні після очищення
        if clustering_data.shape[0] > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(
                x=clustering_data[selected_columns[0]],
                y=clustering_data[selected_columns[1]],
                hue=clustering_data['Cluster'],
                palette='viridis',
                ax=ax
            )
            ax.set_title(f"K-Means Clustering with {n_clusters} Clusters")
            ax.set_xlabel(selected_columns[0])
            ax.set_ylabel(selected_columns[1])
            st.pyplot(fig)
        else:
            st.error("No data available for the selected columns after cleaning.")
    else:
        st.write("Please select exactly 2 columns to visualize the clusters.")