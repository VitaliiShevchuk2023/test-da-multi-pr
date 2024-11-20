import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Завантаження даних
@st.cache_data
def load_data():
    return pd.read_csv('data/earthquake_1995-2023.csv')

def display():
    st.title("Аналіз даних")
    st.write("Це сторінка для аналізу даних.")

    # Завантаження даних
    data = load_data()

    # Перетворення колонки з датами на формат datetime
    data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')
    data['year'] = data['date_time'].dt.year

    # Групування кількості землетрусів за роками
    earthquakes_per_year = data.groupby('year').size().reset_index()
    earthquakes_per_year.columns = ['Year', 'Earthquake_Count']

    # Розділення даних на ознаки (X) та цільову змінну (y)
    X = earthquakes_per_year[['Year']].values  # Роки
    y = earthquakes_per_year['Earthquake_Count'].values  # Кількість землетрусів

    # Розділення даних на тренувальну та тестову вибірки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Вибір моделі
    st.sidebar.header("Model Selection")
    model_name = st.sidebar.radio(
        "Choose a model:",
        options=["Linear Regression", "Ridge Regression", "Lasso Regression", "Random Forest", "Gradient Boosting"]
    )

    # Ініціалізація моделі залежно від вибору
    if model_name == "Linear Regression":
        model = LinearRegression()
    elif model_name == "Ridge Regression":
        alpha = st.sidebar.slider("Alpha for Ridge Regression:", 0.1, 10.0, step=0.1, value=1.0)
        model = Ridge(alpha=alpha)
    elif model_name == "Lasso Regression":
        alpha = st.sidebar.slider("Alpha for Lasso Regression:", 0.1, 10.0, step=0.1, value=1.0)
        model = Lasso(alpha=alpha)
    elif model_name == "Random Forest":
        n_estimators = st.sidebar.slider("Number of Trees:", 10, 100, step=10, value=50)
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    elif model_name == "Gradient Boosting":
        learning_rate = st.sidebar.slider("Learning Rate:", 0.01, 0.5, step=0.01, value=0.1)
        model = GradientBoostingRegressor(learning_rate=learning_rate, random_state=42)

    # Навчання моделі
    model.fit(X_train, y_train)

    # Прогнозування на тестових даних
    y_pred = model.predict(X_test)

    # Оцінка моделі
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Виведення результатів
    st.write(f"**Model**: {model_name}")
    st.write(f"Mean Squared Error (MSE): {mse:.2f}")
    st.write(f"R-squared (R2): {r2:.2f}")

    # Прогнозування для майбутніх років
    future_years = np.array([[2025], [2026], [2027], [2028], [2029], [2030]])
    future_predictions = model.predict(future_years)

    predictions_df = pd.DataFrame({
        "Year": future_years.flatten(),
        "Predicted_Earthquakes": np.round(future_predictions).astype(int)
    })
    st.write("### Predictions for 2025–2030")
    st.dataframe(predictions_df)

    # Візуалізація
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Historical Data')
    plt.plot(X, model.predict(X), color='red', label='Model Prediction')
    plt.scatter(future_years, future_predictions, color='green', label='Future Predictions')
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.title(f'Earthquake Predictions Using {model_name}')
    plt.legend()
    st.pyplot(plt)


