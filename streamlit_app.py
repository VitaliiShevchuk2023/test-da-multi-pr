import streamlit as st
import base64

# Функція для додавання фонового зображення з локального файлу
def add_local_bg(image_file):
    # Читаємо зображення у base64
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    
    # Вставка стилів у Streamlit
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Використання локального зображення
add_local_bg("background.jpg")  # Замініть на назву вашого файлу з фоном

# Головна сторінка
st.title("Earthquake Data Analysis")
st.write("""
### Welcome to the Earthquake Data Analysis Project! 

Use the sidebar to navigate through different analysis tools:
- **Interactive Map**
- **Trends Analysis**
- **Tsunami vs Depth & Magnitude Analysis**
""")
