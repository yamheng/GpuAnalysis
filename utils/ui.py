import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* --- 1. 引入 Google Fonts --- */
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Roboto:wght@300;400;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');
        
        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined';
            font-size: 20px;
            vertical-align: sub;
            margin-right: 8px;
        }
        
        /* --- 2. 全局设置 --- */
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
            color: black;
        }
        
        h1, h2, h3, .stMetricLabel {
            font-family: 'Oswald', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        div, button, input, select, textarea, .stAlert {
            border-radius: 0px !important;
        }
        
        /* --- 3. 顶部导航条 --- */
        .stButton button {
            width: 100%;
            border: 2px solid #000000;
            font-family: 'Oswald', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 15px 0;
            transition: all 0.2s;
            background-color: white;
            color: black;
        }
        .stButton button[kind="primary"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border: 2px solid #000000 !important;
            box-shadow: 5px 5px 0px rgba(0,0,0,0.3);
        }
        .stButton button[kind="secondary"]:hover {
            background-color: #F0F0F0 !important;
            transform: translate(-2px, -2px);
            box-shadow: 5px 5px 0px rgba(0,0,0,1);
        }

        /* --- 4. 侧边栏 --- */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 3px solid #000000;
        }
        
        /* --- 5. Logo 灰度处理 (新加功能) --- */
        /* 针对侧边栏底部的合作 Logo，让它们默认变成黑白，融入主题 */
        [data-testid="stSidebar"] [data-testid="column"] img {
            filter: grayscale(100%);
            opacity: 0.7;
            transition: filter 0.3s, opacity 0.3s;
        }
        /* 鼠标悬停时恢复彩色 (可选) */
        [data-testid="stSidebar"] [data-testid="column"] img:hover {
            filter: grayscale(0%);
            opacity: 1;
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
            st.markdown("""
                <div style="background:#000000; color:white; padding:30px 20px; text-align:center; font-family:'Oswald'; font-size:30px; border: 4px solid black;">
                    GPU<br>FINDER
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 2. 个人信息 (已修改)
        st.markdown("### :material/person: STUDENT INFO")
        st.markdown("""
        **NAME:** Ruichen Liu (刘睿琛)
        **EMAIL:** ruichen.liu@efrei.net
        **SCHOOL:** EFREI Paris
        """)

        st.markdown("### :material/supervisor_account: SUPERVISOR")
        st.markdown("""
        **PROF.** Mano Joseph Mathew
        **EMAIL:** mano.mathew@efrei.fr
        """)
        
        st.markdown("---")
        
        # 3. 按钮 (Resources)
        st.markdown("### :material/link: RESOURCES")
        st.markdown("""
        <a href="https://github.com" target="_blank" style="text-decoration:none;">
            <button style="width:100%; background:white; border:2px solid black; color:black; padding:10px; cursor:pointer; font-family:'Oswald'; letter-spacing:1px; font-weight:bold; text-transform:uppercase;">
                <span class="material-symbols-outlined">deployed_code_update</span>
                View Source on GitHub
            </button>
        </a>
        <br><br>
        <a href="https://efrei.fr" target="_blank" style="text-decoration:none;">
            <button style="width:100%; background:black; border:none; color:white; padding:10px; cursor:pointer; font-family:'Oswald'; letter-spacing:1px; font-weight:bold; text-transform:uppercase;">
               <span class="material-symbols-outlined">school</span>
                EFREI Paris
            </button>
        </a>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 4. 合作机构 Logo (新加部分)
        # 放在最底部，双列布局，利用 CSS 滤镜自动变黑白
        st.markdown("### :material/verified: AFFILIATIONS")
        col_logo1, col_logo2 = st.columns(2)
        
        with col_logo1:
            # 确保 assets 文件夹里有这个文件
            st.image("assets/logo_efrei.png", use_container_width=True)
        with col_logo2:
            st.image("assets/logo_WUT.png", use_container_width=True)