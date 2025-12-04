# 求你了别报错能运行别中断
import streamlit as st
from utils.data_loader import load_and_clean_data
from utils.ui import load_css, render_sidebar_info
from sections import home, data_info, moores_law, efficiency, memory_wall, market_ai, economic, contact

# 1. Page Configuration
st.set_page_config(
    page_title="GPU-FINDER",
    page_icon="▪️", # Replace the original Streamlit icon with this icon that looks a bit like a chip.
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

# 2. Loading Resources & Sidebar
load_css()
df = load_and_clean_data()
render_sidebar_info()

# 3. Top navigation bar
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])

with col_nav1:
    # Keeping only uppercase English, it's very cool with the Oswald font.
    if st.button("HOME", use_container_width=True, 
                 type="primary" if st.session_state['current_page'] == 'Home' else "secondary"):
        st.session_state['current_page'] = 'Home'
        st.rerun()

with col_nav2:
    if st.button("ANALYSIS TOOLS", use_container_width=True, 
                 type="primary" if st.session_state['current_page'] == 'Tools' else "secondary"):
        st.session_state['current_page'] = 'Tools'
        st.rerun()

with col_nav3:
    if st.button("CONTACT / HELP", use_container_width=True, 
                 type="primary" if st.session_state['current_page'] == 'Contact' else "secondary"):
        st.session_state['current_page'] = 'Contact'
        st.rerun()

st.markdown("---")

# 4. Page routing
if st.session_state['current_page'] == 'Home':
    home.show(df)

elif st.session_state['current_page'] == 'Tools':
    st.markdown("## ANALYSIS DASHBOARD")
    st.markdown("Explore the evolution of GPUs through different lenses.")
    
    # Tabs also directly use uppercase titles
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "DATA INFO", 
        "MOORE'S LAW", 
        "EFFICIENCY", 
        "MEMORY WALL", 
        "ECONOMIC WALL",
        "AI SEGMENTS"
    ])
    
    with tab1: data_info.show(df)
    with tab2: moores_law.show(df)
    with tab3: efficiency.show(df)
    with tab4: memory_wall.show(df)
    with tab5: economic.show(df)
    with tab6: market_ai.show(df)

elif st.session_state['current_page'] == 'Contact':
    contact.show()