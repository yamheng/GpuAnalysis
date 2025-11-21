# 文件路径: app.py
import streamlit as st
from utils.data_loader import load_and_clean_data
from utils.ui import load_css, render_sidebar_info

# 引入你的所有模块
from sections import home, data_info, moores_law, efficiency, memory_wall, market_ai

# -----------------------------------------------------------------------------
# 1. 页面配置 (Page Config)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GPU-FINDER",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 Session State 用于导航
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

# -----------------------------------------------------------------------------
# 2. 加载资源 & 侧边栏 (Load Resources & Sidebar)
# -----------------------------------------------------------------------------
load_css()
df = load_and_clean_data()
render_sidebar_info() # 侧边栏现在只显示信息，不负责导航

# -----------------------------------------------------------------------------
# 3. 顶部导航栏 (Top Navigation Bar)
# -----------------------------------------------------------------------------
# 使用 3 列布局放置按钮
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])

with col_nav1:
    # 如果当前是 Home，按钮变色 (Primary)，否则白色 (Secondary)
    if st.button("🏠 HOME", use_container_width=True, 
                 type="primary" if st.session_state['current_page'] == 'Home' else "secondary"):
        st.session_state['current_page'] = 'Home'
        st.rerun()

with col_nav2:
    if st.button("📊 ANALYSIS TOOLS", use_container_width=True, 
                 type="primary" if st.session_state['current_page'] == 'Tools' else "secondary"):
        st.session_state['current_page'] = 'Tools'
        st.rerun()

with col_nav3:
    if st.button("📧 CONTACT / HELP", use_container_width=True, 
                 type="primary" if st.session_state['current_page'] == 'Contact' else "secondary"):
        st.session_state['current_page'] = 'Contact'
        st.rerun()

st.markdown("---") # 导航栏下方的分割线

# -----------------------------------------------------------------------------
# 4. 页面路由逻辑 (Page Routing)
# -----------------------------------------------------------------------------

# === 页面 1: 首页 ===
if st.session_state['current_page'] == 'Home':
    home.show(df)

# === 页面 2: 分析工具集 (整合了所有分析模块) ===
elif st.session_state['current_page'] == 'Tools':
    st.markdown("## 🛠️ Analysis Dashboard")
    st.markdown("Explore the evolution of GPUs through different lenses.")
    
    # 使用 Tabs 将原来的侧边栏子菜单变成顶部标签
    # 这种方式非常符合 "Sharp" 和 "Dashboard" 的感觉
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧹 Data Info", 
        "📉 Moore's Law", 
        "⚡ Efficiency", 
        "🧱 Memory Wall", 
        "🤖 AI Segments"
    ])
    
    with tab1:
        data_info.show(df)
    with tab2:
        moores_law.show(df)
    with tab3:
        efficiency.show(df)
    with tab4:
        memory_wall.show(df)
    with tab5:
        market_ai.show(df)

# === 页面 3: 联系/帮助 ===
elif st.session_state['current_page'] == 'Contact':
    st.markdown("## 📧 Contact & Documentation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("### 📬 Get in Touch")
        st.markdown("""
        Have questions about the dataset or the code?  
        **Email:** mano.mathew@efrei.fr  
        **Office:** EFREI Paris, Lab 302  
        """)
        
        st.markdown("### 🐛 Report a Bug")
        st.text_area("Describe the issue:", height=100)
        st.button("Submit Report")
        
    with col2:
        st.warning("### 📄 License & Data")
        st.markdown("""
        **Dataset Source:** TechPowerUp GPU Database (Scraped)  
        **License:** MIT License  
        **Last Update:** November 2025  
        """)