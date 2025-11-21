import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* --- 1. 引入 Google Fonts (Oswald 用于标题，Roboto 用于正文) --- */
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Roboto:wght@300;400;700&display=swap');

        /* --- 2. 全局锋利化 & 字体设置 --- */
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
            color: black;
        }
        
        /* 标题专用字体：Oswald (高挑、硬朗、设计感) */
        h1, h2, h3, .stMetricLabel {
            font-family: 'Oswald', sans-serif !important;
            text-transform: uppercase; /* 全大写 */
            letter-spacing: 1px; /* 增加字间距 */
        }
        
        /* 强制直角 */
        div, button, input, select, textarea, .stAlert, .st-emotion-cache-1wbqy5l {
            border-radius: 0px !important;
        }
        
        /* --- 3. 顶部导航条 (黑白风格) --- */
        .stButton button {
            width: 100%;
            border: 2px solid #000000; /* 加粗边框 */
            font-family: 'Oswald', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 15px 0;
            transition: all 0.2s;
            background-color: white;
            color: black;
        }
        
        /* 激活状态：黑底白字 */
        .stButton button[kind="primary"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border: 2px solid #000000 !important;
            box-shadow: 5px 5px 0px rgba(0,0,0,0.3); /* 硬阴影 */
        }
        
        /* 未激活状态：白底黑字 */
        .stButton button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
        }
        .stButton button[kind="secondary"]:hover {
            background-color: #F0F0F0 !important;
            transform: translate(-2px, -2px);
            box-shadow: 5px 5px 0px rgba(0,0,0,1); /* 悬停时纯黑阴影 */
        }

        /* --- 4. 侧边栏 (极简黑白) --- */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 3px solid #000000; /* 粗黑线分割 */
        }
        
        /* --- 5. 提示框样式重写 (覆盖 Streamlit 默认颜色) --- */
        /* Success (原绿色) -> 黑白 */
        .stAlert[data-baseweb="notification"] {
            background-color: #FFFFFF;
            border: 2px solid #000000;
            color: #000000;
        }
        .stAlertIcon {
            color: #000000 !important; /* 图标也变黑 */
        }

        /* --- 6. 隐藏多余元素 --- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar_info():
    """侧边栏：只展示个人信息"""
    with st.sidebar:
        # 1. Logo 区域
        try:
            st.image("assets/logo.png", use_container_width=True)
        except:
            # 如果没有图片，用纯黑方块代替
            st.markdown("""
                <div style="background:#000000; color:white; padding:30px 20px; text-align:center; font-family:'Oswald'; font-size:30px; border: 4px solid black;">
                    GPU<br>FINDER
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 2. 个人信息
        st.markdown("### 👤 STUDENT INFO")
        st.markdown("""
        **NAME:** Mano Joseph Mathew  
        **EMAIL:** mano.mathew@efrei.fr  
        **SCHOOL:** EFREI Paris  
        """)

        st.markdown("### 👨‍🏫 SUPERVISOR")
        st.markdown("**PROF.** Name Here")
        
        st.markdown("---")
        
        # 3. 按钮 (黑白风)
        st.markdown("### 🔗 RESOURCES")
        st.markdown("""
        <a href="https://github.com" target="_blank" style="text-decoration:none;">
            <button style="width:100%; background:white; border:2px solid black; color:black; padding:10px; cursor:pointer; font-family:'Oswald'; letter-spacing:1px; font-weight:bold; text-transform:uppercase;">
                💻 View Source on GitHub
            </button>
        </a>
        <br><br>
        <a href="https://efrei.fr" target="_blank" style="text-decoration:none;">
            <button style="width:100%; background:black; border:none; color:white; padding:10px; cursor:pointer; font-family:'Oswald'; letter-spacing:1px; font-weight:bold; text-transform:uppercase;">
                🏫 EFREI Paris
            </button>
        </a>
        """, unsafe_allow_html=True)