import streamlit as st
from utils.ui import load_css 

def show(df):
    
    # Main Title
    st.markdown("# GPU EVOLUTION INSIGHT(1986-2026)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;————The Twilight of Moore's Law")
    st.markdown("---")

    # Main Title
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
        
        st.info("**START:** CLICK 'ANALYSIS TOOLS' IN THE TOP MENU.", icon=":material/call_made:")

    with col2:
        st.markdown("### :material/query_stats: STATS")
        # Here I attempted to use Metric to automatically adapt black and white CSS and add some visual effects.
        st.metric("TOTAL GPUs", len(df))
        st.metric("TIME SPAN", "1986 - 2026")
        st.metric("VENDORS", f"{df['Brand'].nunique()}")

    # "Digital Process Cards" as an alternative to Graphviz
    st.markdown("---")
    st.markdown("### :material/azm: METHODOLOGY")
    
    # Create 4 columns of pure CSS cards using HTML/CSS,
    # It will also generate 4 boxes with borders, each containing a huge numbered label.
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
        opacity: 0.3; 
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
    /* The numbers turn white when hovered over */
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