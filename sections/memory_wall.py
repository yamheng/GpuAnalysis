# 文件路径: sections/memory_wall.py
import streamlit as st
import plotly.graph_objects as go

def show(df):
    st.markdown("## 🧱 The Memory Wall Analysis")
    st.markdown("### Question: Is Memory Bandwidth keeping up with Compute Power?")

    # 1. 数据聚合
    df_trend = df[(df['Release_Year'] >= 2010) & (df['Release_Year'] <= 2024)].copy()
    annual_stats = df_trend.groupby('Release_Year')[['FP32_GFLOPS', 'Bandwidth_GBs']].mean().reset_index()
    
    # 2. 计算指数 (Base 2013 = 100)
    base_year = 2013
    base_row = annual_stats[annual_stats['Release_Year'] == base_year]
    
    if not base_row.empty:
        base_compute = base_row['FP32_GFLOPS'].values[0]
        base_bw = base_row['Bandwidth_GBs'].values[0]
        
        annual_stats['Compute_Index'] = (annual_stats['FP32_GFLOPS'] / base_compute) * 100
        annual_stats['Bandwidth_Index'] = (annual_stats['Bandwidth_GBs'] / base_bw) * 100
        
        # 3. 绘图
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=annual_stats['Release_Year'], y=annual_stats['Compute_Index'], name='Compute Growth', line=dict(color='#FF4B4B', width=4)))
        fig.add_trace(go.Scatter(x=annual_stats['Release_Year'], y=annual_stats['Bandwidth_Index'], name='Bandwidth Growth', line=dict(color='#1f77b4', width=4), fill='tonexty', fillcolor='rgba(255, 75, 75, 0.2)'))

        fig.update_layout(
            title="The Growing Gap: Compute vs Bandwidth (Index 100 = 2013)",
            yaxis_title="Growth Index",
            height=600,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The red shaded area represents the **Memory Wall**. Compute is growing much faster than bandwidth.")
    else:
        st.error("Insufficient data for base year 2013.")