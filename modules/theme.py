import streamlit as st

# Define CSS for dark and light themes
dark_theme_css = '''
    /* Main app background */
    .main {
        background-color: #0e1117;  /* deep dark (GitHub-style) */
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;  /* slightly lighter dark */
    }

    /* Buttons */
    .stButton > button {
        background-color: #238636;  /* green accent */
        color: #ffffff;  /* white text */
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
    }

    .stButton > button:hover {
        background-color: #2ea043;
        color: #ffffff;
    }

    /* Text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }

    p, span, label, div {
        color: #c9d1d9;  /* soft white (easy on eyes) */
    }

    /* Input fields */
    input, textarea {
        background-color: #0e1117;
        color: #ffffff;
        border: 1px solid #30363d;
        border-radius: 6px;
    }

    /* Cards / containers */
    .stCard {
        background-color: #161b22;
        border-radius: 10px;
        padding: 10px;
    }

    /* Accent */
    .accent {
        color: #58a6ff;  /* blue highlight */
    }
'''

light_theme_css = '''
    .main {
        background-color: #ffe4e1;  /* light pink */
    }
    .sidebar .sidebar-content {
        background-color: #f8d7da;  /* slightly darker pink */
    }
    .stButton > button {
        background-color: #ffc1c1;  /* pink for buttons */
        color: #1a1a2e;  /* dark text for contrast */
    }
    .stText, .stHeader, .stSubheader, .stCaption {
        color: #1a1a2e;  /* dark text for visibility */
    }
'''


# Apply theme based on session state
def apply_theme():
    if st.session_state.get('theme') == 'dark':
        st.markdown(f'<style>{dark_theme_css}</style>', unsafe_allow_html=True)
    else:
        st.markdown(f'<style>{light_theme_css}</style>', unsafe_allow_html=True)


# Render a theme toggle in the sidebar
def render_theme_toggle():
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'light'

    toggle = st.sidebar.button('🌙' if st.session_state['theme'] == 'light' else '☀️')
    if toggle:
        st.session_state['theme'] = 'dark' if st.session_state['theme'] == 'light' else 'light'