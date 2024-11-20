import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, data_analysis, map

# Словник для сторінок
PAGES = {
    "Головна": home.display,
    "Аналіз даних": data_analysis.display,
    "Інтерактивна карта": map.display,
}

st.set_page_config(page_title="Багатосторінковий застосунок", page_icon="🌟")


# Меню навігації
with st.sidebar:
    selected_page = option_menu(
        menu_title="Навігація",
        options=list(PAGES.keys()),
        icons=["house", "bar-chart-line", "map"],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f8f9fa"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#02ab21"},
        },
    )

# Відображення вибраної сторінки
if selected_page in PAGES:
    # Оновлюємо параметри в URL
    st.query_params.update({"page": selected_page})
    PAGES[selected_page]()  # Виклик функції сторінки

