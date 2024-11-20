import streamlit as st
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# Ініціалізація стану
if 'model_name' not in st.session_state:
    st.session_state.model_name = "Linear Regression"

# Вибір моделі через sidebar
st.sidebar.header("Model Selection")
model_name = st.sidebar.radio(
    "Choose a model:",
    options=["Linear Regression", "Ridge Regression", "Lasso Regression", "Random Forest", "Gradient Boosting"],
    index=["Linear Regression", "Ridge Regression", "Lasso Regression", "Random Forest", "Gradient Boosting"].index(st.session_state.model_name),
)

# Зберігаємо вибір в session_state
st.session_state.model_name = model_name

# Ініціалізація моделі залежно від вибору
def get_model():
    if st.session_state.model_name == "Linear Regression":
        return LinearRegression()
    elif st.session_state.model_name == "Ridge Regression":
        alpha = st.sidebar.slider("Alpha for Ridge Regression:", 0.1, 10.0, step=0.1, value=1.0)
        return Ridge(alpha=alpha)
    elif st.session_state.model_name == "Lasso Regression":
        alpha = st.sidebar.slider("Alpha for Lasso Regression:", 0.1, 10.0, step=0.1, value=1.0)
        return Lasso(alpha=alpha)
    elif st.session_state.model_name == "Random Forest":
        n_estimators = st.sidebar.slider("Number of Trees:", 10, 100, step=10, value=50)
        return RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    elif st.session_state.model_name == "Gradient Boosting":
        learning_rate = st.sidebar.slider("Learning Rate:", 0.01, 0.5, step=0.01, value=0.1)
        return GradientBoostingRegressor(learning_rate=learning_rate, random_state=42)

# Виклик функції для створення моделі
model = get_model()

# Демонстрація вибору
st.write(f"**Selected Model**: {st.session_state.model_name}")
st.write(f"**Model Parameters**: {model}")

