import streamlit as st
# ❌ 不再导入 render_green_box, render_header，因为 ui.py 里已经删了
# ✅ 只导入需要的工具
from utils.ui import load_css 

def show(df):
    # 1. 顶部通知框 
    # 直接用 st.success，因为我们在 CSS 里强制设为了直角，它现在就是一个锋利的绿色方块
    st.success("👋 **Project Update:** GPU-FINDER is growing every day! We analyze 3000+ GPUs to reveal hardware trends.")
    
    # 2. 主标题 (使用原生 Markdown，CSS 会让字体变硬朗)
    st.markdown("# 🚀 GPU Evolution: A Data Storytelling Tool")
    st.markdown("### Analyzing 40 years of graphics hardware history (1986-2026)")
    st.markdown("---")

    # 3. 核心内容区
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 What is this tool?")
        st.markdown("""
        This is an interactive dashboard built with **Streamlit** to explore the evolution of Graphics Processing Units (GPUs).
        
        **Key Features:**
        * **Moore's Law Validator:** See if transistor density is still doubling.
        * **Efficiency Tracker:** Analyze Performance per Watt trends.
        * **AI Segmentation:** Use Machine Learning to group GPUs by specs.
        """)
        
        # 提示框
        st.info("👈 **Get Started:** Use the TOP NAVIGATION bar to switch to 'Analysis Tools'.")

    with col2:
        # 数据集统计
        st.markdown("### 📊 Dataset Stats")
        # 原生 Metric 现在也会被 CSS 变成直角
        st.metric("Total GPUs", len(df))
        st.metric("Time Span", "1986 - 2026")
        st.metric("Brands", f"{df['Brand'].nunique()} (Nvidia, AMD, Intel...)")

    # 4. 底部流程图
    st.markdown("### 🛠️ How it works")
    st.graphviz_chart("""
        digraph G {
            rankdir=LR;
            // 设置节点为矩形，字体为无衬线，制造工业感
            node [shape=rect, style="filled,bold", fillcolor="white", color="black", penwidth=2, fontname="Helvetica"];
            edge [penwidth=2];
            
            Raw [label="Raw Dataset\n(CSV)"];
            Clean [label="Data Cleaning\n(Pandas)"];
            Viz [label="Visualization\n(Plotly)"];
            App [label="Interactive App\n(Streamlit)"];
            
            Raw -> Clean -> Viz -> App;
        }
    """)