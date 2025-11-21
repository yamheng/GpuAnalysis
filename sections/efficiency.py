import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re

def show(df):
    st.markdown("## ⚡ Architecture Efficiency & Power")
    st.markdown("### Research Question: How did we fight the 'Power Wall'?")

    # === 1. 数据修补逻辑 (Patching Data) ===
    # 重新应用 test.py 中的补丁，确保 TFLOPS 转换正确
    def patch_gflops(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        val_str = str(val).lower().replace(',', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'tflops' in val_str: return num * 1000 # TFLOPS -> GFLOPS
        return num

    # 创建本地副本进行计算，不影响全局 df
    df_eff = df.copy()
    df_eff['FP32_GFLOPS'] = df_eff['Theoretical Performance__FP32 (float)'].apply(patch_gflops)
    
    # 重新解析 TDP (防止全局清洗时的意外)
    df_eff['TDP_Watts'] = df['Board Design__TDP'].apply(lambda x: float(re.search(r"(\d+)", str(x)).group(1)) if re.search(r"(\d+)", str(x)) else np.nan)
    
    # 计算核心指标：每瓦性能
    df_eff['Perf_Per_Watt'] = df_eff['FP32_GFLOPS'] / df_eff['TDP_Watts']
    
    # 过滤无效数据
    df_eff = df_eff.dropna(subset=['Perf_Per_Watt', 'Graphics Processor__Architecture', 'Release_Year', 'TDP_Watts'])
    df_eff = df_eff[df_eff['Release_Year'] >= 2012] 
    
    # 筛选 Top 架构
    top_archs = df_eff['Graphics Processor__Architecture'].value_counts().head(15).index.tolist()
    df_eff_filtered = df_eff[df_eff['Graphics Processor__Architecture'].isin(top_archs)].copy()
    
    # 按年份排序架构
    arch_order = df_eff_filtered.groupby('Graphics Processor__Architecture')['Release_Year'].median().sort_values().index.tolist()

    # === 2. 动态计算 KPI 指标 (找回 test.py 的逻辑) ===
    # 找出最高效率的卡
    max_eff_row = df_eff_filtered.loc[df_eff_filtered['Perf_Per_Watt'].idxmax()]
    max_eff_val = max_eff_row['Perf_Per_Watt']
    max_eff_name = max_eff_row['Name']

    # 计算 Ada Lovelace 相对于 Ampere 的提升幅度
    ada_median = df_eff_filtered[df_eff_filtered['Graphics Processor__Architecture'] == 'Ada Lovelace']['Perf_Per_Watt'].median()
    ampere_median = df_eff_filtered[df_eff_filtered['Graphics Processor__Architecture'] == 'Ampere']['Perf_Per_Watt'].median()
    
    leap_pct = 0
    if pd.notna(ada_median) and pd.notna(ampere_median) and ampere_median > 0:
        leap_pct = ((ada_median - ampere_median) / ampere_median) * 100

    # === 3. 页面 Tabs ===
    tab1, tab2 = st.tabs(["📈 The Solution: Efficiency", "🧱 The Problem: Power Trends"])

    # --- Tab 1: Efficiency (修复了散点和下方 KPI) ---
    with tab1:
        st.markdown("#### Solution: Getting smarter (GFLOPS per Watt)")
        
        fig_eff = px.box(
            df_eff_filtered,
            x='Graphics Processor__Architecture',
            y='Perf_Per_Watt',
            color='Brand',
            points="all",  # ✅ 修复点：找回了所有散点
            hover_data=['Name', 'TDP_Watts', 'FP32_GFLOPS'],
            category_orders={'Graphics Processor__Architecture': arch_order},
            title="Efficiency Evolution: GFLOPS per Watt (Higher is Better)",
            labels={'Perf_Per_Watt': 'GFLOPS / Watt'},
            height=550
        )
        st.plotly_chart(fig_eff, use_container_width=True)
        
        st.markdown("---")
        st.subheader("💡 Key Insights (Real-Time Data)")
        
        # ✅ 修复点：找回了下方的 KPI 指标卡片
        m_col1, m_col2, m_col3 = st.columns(3)
        
        with m_col1:
            st.metric(
                label=f"👑 Peak Efficiency ({max_eff_name})", 
                value=f"{max_eff_val:.0f} GFLOPS/W", 
                delta="Historic High"
            )
            
        with m_col2:
            st.metric(
                label="🚀 Ada Lovelace Leap", 
                value=f"+{leap_pct:.0f}%", 
                delta="vs Ampere (Median)"
            )
            
        with m_col3:
            st.info(f"""
            **Insight:** Data shows **Ada Lovelace** achieved a massive **+{leap_pct:.0f}%** jump over Ampere, thanks to the TSMC 4N node.
            *Note: Blackwell drops slightly because it optimizes for FP8 (AI), not FP32.*
            """)

    # --- Tab 2: Power Trends (保持不变) ---
    with tab2:
        st.markdown("#### Problem: The Power Ceiling (300W)")
        
        mask_clean = (
            (df_eff_filtered['TDP_Watts'] < 800) & 
            ~((df_eff_filtered['TDP_Watts'] > 350) & (df_eff_filtered['Release_Year'] < 2019))
        )
        df_tdp_clean = df_eff_filtered[mask_clean].copy()
        
        tdp_stats = df_tdp_clean.groupby('Graphics Processor__Architecture')['TDP_Watts'].agg(['max', 'mean']).reset_index()
        tdp_stats['Graphics Processor__Architecture'] = pd.Categorical(
            tdp_stats['Graphics Processor__Architecture'], 
            categories=arch_order, 
            ordered=True
        )
        tdp_stats = tdp_stats.sort_values('Graphics Processor__Architecture')

        fig_tdp = go.Figure()

        fig_tdp.add_hline(
            y=300, 
            line_dash="dash", line_color="red", line_width=2,
            annotation_text="🛑 The 300W Physical Limit", 
            annotation_position="top left"
        )

        fig_tdp.add_trace(go.Scatter(
            x=tdp_stats['Graphics Processor__Architecture'], 
            y=tdp_stats['max'],
            mode='lines+markers',
            name='Flagship Max Power',
            line=dict(color='#FF4B4B', width=4, shape='linear'), 
            marker=dict(size=10, symbol='diamond'),
            hovertemplate="<b>%{x}</b><br>Max TDP: %{y} W<extra></extra>"
        ))

        fig_tdp.add_trace(go.Scatter(
            x=tdp_stats['Graphics Processor__Architecture'], 
            y=tdp_stats['mean'],
            mode='lines+markers',
            name='Average Power',
            line=dict(color='grey', width=2, dash='dot'),
            hovertemplate="<b>%{x}</b><br>Avg TDP: %{y:.1f} W<extra></extra>"
        ))

        fig_tdp.update_layout(
            title="Evidence of the 'Power Wall': Plateau vs. Explosion",
            yaxis_title="Power Consumption (Watts)",
            height=550,
            hovermode="x unified",
            yaxis=dict(range=[0, 650]),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        st.plotly_chart(fig_tdp, use_container_width=True)