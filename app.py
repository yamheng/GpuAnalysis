# 文件路径: app.py
import streamlit as st
from utils.data_loader import load_and_clean_data
from utils.ui import load_css, render_sidebar_info
from sections import home, data_info, moores_law, efficiency, memory_wall, market_ai, economic, contact

# 1. 页面配置
st.set_page_config(
    page_title="GPU-FINDER",
    page_icon="▪️", # 换成一个极简的几何图形，或者干脆不设
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

# 2. 加载资源 & 侧边栏
load_css()
df = load_and_clean_data()
render_sidebar_info()

# 3. 顶部导航栏 (去掉了 Emoji，纯文字)
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])

with col_nav1:
    # 只保留大写英文，配合 Oswald 字体非常有力
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

# 4. 页面路由
if st.session_state['current_page'] == 'Home':
    home.show(df)

elif st.session_state['current_page'] == 'Tools':
    st.markdown("## ANALYSIS DASHBOARD")
    st.markdown("Explore the evolution of GPUs through different lenses.")
    
    # Tabs 也不要 Emoji，直接用大写标题
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