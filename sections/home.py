import streamlit as st
from utils.ui import load_css 

def show(df):
    
    # 2. 主标题
    st.markdown("# GPU EVOLUTION: A DATA STORY")
    st.markdown("### ANALYZING THE LIMITS OF SILICON PHYSICS & ECONOMICS")
    st.markdown("---")

    # 3. 核心内容区
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### :material/ads_click: OBJECTIVE")
        st.markdown("""
        This dashboard deconstructs the history of Graphics Processing Units (GPUs) to validate industry laws and expose hidden bottlenecks.
        
        **CORE MODULES:**
        * **MOORE'S LAW:** Tracking transistor density vs. physical limits.
        * **POWER WALL:** The end of Dennard Scaling and the rise of TDP.
        * **ECONOMIC WALL:** Why computing is getting expensive again.
        """)
        
        st.info("**START:** CLICK 'ANALYSIS TOOLS' IN THE TOP MENU.", icon=":material/line_start_arrow:")

    with col2:
        st.markdown("### :material/query_stats: STATS")
        # Metric 会自动适配我们的黑白 CSS，看起来非常酷
        st.metric("TOTAL GPUs", len(df))
        st.metric("TIME SPAN", "1986 - 2026")
        st.metric("VENDORS", f"{df['Brand'].nunique()}")

    # 4. 替代 Graphviz 的“数字流程卡片”
    st.markdown("---")
    st.markdown("### :material/azm: METHODOLOGY")
    
    # 使用 HTML/CSS 创建 4 列纯 CSS 卡片，不使用任何图片或 Emoji
    # 这段 HTML 代码会生成 4 个带边框的盒子，里面有巨大的数字编号
    st.markdown("""
    <style>
    .step-card {
        border: 2px solid black;
        padding: 20px;
        height: 100%;
        background: white;
        transition: transform 0.2s;
    }
    .step-card:hover {
        background: black;
        color: white;
        cursor: default;
    }
    .step-num {
        font-family: 'Oswald', sans-serif;
        font-size: 40px;
        font-weight: bold;
        opacity: 0.3; /* 数字半透明，显高级 */
        margin-bottom: 10px;
    }
    .step-title {
        font-family: 'Oswald', sans-serif;
        font-size: 18px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .step-desc {
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
        line-height: 1.4;
    }
    /* 悬停时数字变白 */
    .step-card:hover .step-num { color: white; opacity: 0.8; }
    </style>

    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 200px;">
            <div class="step-card">
                <div class="step-num">01</div>
                <div class="step-title">Raw Data</div>
                <div class="step-desc">Ingesting unstructured CSV specs from TechPowerUp database.</div>
            </div>
        </div>
        <div style="flex: 1; min-width: 200px;">
            <div class="step-card">
                <div class="step-num">02</div>
                <div class="step-title">Processing</div>
                <div class="step-desc">Cleaning regex, handling units, and extracting features.</div>
            </div>
        </div>
        <div style="flex: 1; min-width: 200px;">
            <div class="step-card">
                <div class="step-num">03</div>
                <div class="step-title">Visualization</div>
                <div class="step-desc">Plotly interactive charts with regression analysis.</div>
            </div>
        </div>
        <div style="flex: 1; min-width: 200px;">
            <div class="step-card">
                <div class="step-num">04</div>
                <div class="step-title">Insight</div>
                <div class="step-desc">Interactive dashboard for validating Moore's Law.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)