import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show(df):
    st.markdown("## :material/speed: ARCHITECTURE EFFICIENCY & POWER")
    
    # 1. Preparation of basic data
    d = df.dropna(subset=['Perf_Per_Watt', 'Graphics Processor__Architecture', 'TDP_Watts'])
    d = d[d['Release_Year'] >= 2012].copy()
    
    # Filter Top 15 Architectures
    top_arch = d['Graphics Processor__Architecture'].value_counts().head(15).index
    d = d[d['Graphics Processor__Architecture'].isin(top_arch)]
    order = d.groupby('Graphics Processor__Architecture')['Release_Year'].median().sort_values().index

    # KPI calculation
    best = d.loc[d['Perf_Per_Watt'].idxmax()]
    ada = d[d['Graphics Processor__Architecture'] == 'Ada Lovelace']['Perf_Per_Watt'].median()
    ampere = d[d['Graphics Processor__Architecture'] == 'Ampere']['Perf_Per_Watt'].median()
    leap = ((ada - ampere) / ampere) * 100 if (pd.notna(ada) and pd.notna(ampere)) else 0
    
    tab1, tab2 = st.tabs([":material/battery_charging_full: The Solution: Efficiency", ":material/dangerous: The Problem: Power & Frequency"])

    with tab1:
        # Figure 1: Efficiency Box Plot
        st.markdown("#### SOLUTION: GETTING SMARTER (GFLOPS PER WATT)")
        fig = px.box(d, x='Graphics Processor__Architecture', y='Perf_Per_Watt', color='Brand', points="all",
                    category_orders={'Graphics Processor__Architecture': order}, height=500)
        
        fig.update_layout(
            title="Efficiency Evolution: GFLOPS per Watt (Higher is Better)",
            xaxis=dict(title="GPU Architecture"),
            yaxis=dict(title="Efficiency (GFLOPS/Watt)"),
            margin=dict(t=50, b=50, l=60, r=60),
            font=dict(family="Oswald")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 3列 KPI
        m1, m2, m3 = st.columns(3)
        m1.metric(":material/bolt: Peak Efficiency", f"{best['Perf_Per_Watt']:.0f} GFLOPS/W", best['Name'])
        m2.metric(":material/trending_up: Ada Lovelace Leap", f"+{leap:.0f}%", "vs Ampere")
        m3.info("Blackwell drops slightly as it optimizes for AI (FP8), not FP32.")

    with tab2:
        # Figure 2: Frequency Chart (Interpolation Completion)
        st.markdown("#### 1. THE CAUSE: FREQUENCY STAGNATION")
        st.caption("Why do we need more power? Because we can't just increase clock speed anymore.")
        trend = df.groupby('Release_Year')['GPU_Clock_MHz'].agg(['max', 'mean']).reset_index()
        full_yr = pd.DataFrame({'Release_Year': np.arange(1995, 2027)})
        trend = pd.merge(full_yr, trend, on='Release_Year', how='left').interpolate()

        fig_clk = go.Figure()
        fig_clk.add_trace(go.Scatter(x=trend['Release_Year'], y=trend['max'], name='Max Clock', line=dict(color='#FF4B4B', width=4), connectgaps=True))
        fig_clk.add_trace(go.Scatter(x=trend['Release_Year'], y=trend['mean'], name='Avg Clock', line=dict(color='grey', width=2, dash='dot'), connectgaps=True))
        
        fig_clk.update_layout(
            title="Frequency Stagnation", 
            xaxis=dict(title="Release Year", range=[1995, 2026]),
            yaxis=dict(title="Core Clock (MHz)"),
            margin=dict(t=50, b=50, l=60, r=60),
            height=400, font=dict(family="Oswald"), hovermode="x unified"
        )
        st.plotly_chart(fig_clk, use_container_width=True)

        st.divider()

        # Figure 3: TDP Power Consumption Chart
        st.markdown("#### 2. THE CONSEQUENCE: POWER EXPLOSION (TDP)")
        st.caption("Since we can't make clocks faster, we add more cores, which explodes power consumption.")
        # Filter out extreme outliers (such as 800W engineering cards) and early high-power dual-chip cards (to prevent raising the baseline)
        mask_clean = (
            (d['TDP_Watts'] < 800) & 
            ~((d['TDP_Watts'] > 350) & (d['Release_Year'] < 2019))
        )
        d_tdp = d[mask_clean]
        
        # Recalculate the statistical values
        tdp_stat = d_tdp.groupby('Graphics Processor__Architecture')['TDP_Watts'].agg(['max', 'mean']).reindex(order).reset_index()
        
        fig_tdp = go.Figure()
        fig_tdp.add_trace(go.Scatter(x=tdp_stat['Graphics Processor__Architecture'], y=tdp_stat['max'], name='Flagship Max TDP', line=dict(color='black', width=3, shape='linear'), marker=dict(size=8, symbol='diamond')))
        fig_tdp.add_trace(go.Scatter(x=tdp_stat['Graphics Processor__Architecture'], y=tdp_stat['mean'], name='Average TDP', line=dict(color='grey', width=2, dash='dot')))
        
        # 300W red line
        fig_tdp.add_hline(
            y=300, line=dict(color='red', dash='dash', width=2), 
            annotation_text="🛑 Old 300W Limit", annotation_position="top left"
        )
        
        fig_tdp.update_layout(
            title="Power Consumption (TDP) Trends", 
            xaxis=dict(title="GPU Architecture"),
            yaxis=dict(title="TDP (Watts)", range=[0, 650]), # Fix the Y-axis range for a more stable visual effect
            margin=dict(t=50, b=50, l=60, r=60),
            height=400, font=dict(family="Oswald")
        )
        st.plotly_chart(fig_tdp, use_container_width=True)