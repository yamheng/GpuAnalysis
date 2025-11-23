import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re

def show(df):
    st.markdown("## :material/speed: Architecture Efficiency & Power")
    
    # === 1. 数据准备 (Patching Data) ===
    def patch_gflops(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        val_str = str(val).lower().replace(',', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'tflops' in val_str: return num * 1000 
        return num

    df_eff = df.copy()
    df_eff['FP32_GFLOPS'] = df_eff['Theoretical Performance__FP32 (float)'].apply(patch_gflops)
    # 重新解析 TDP
    df_eff['TDP_Watts'] = df['Board Design__TDP'].apply(lambda x: float(re.search(r"(\d+)", str(x)).group(1)) if re.search(r"(\d+)", str(x)) else np.nan)
    df_eff['Perf_Per_Watt'] = df_eff['FP32_GFLOPS'] / df_eff['TDP_Watts']
    
    df_eff = df_eff.dropna(subset=['Perf_Per_Watt', 'Graphics Processor__Architecture', 'Release_Year', 'TDP_Watts'])
    df_eff = df_eff[df_eff['Release_Year'] >= 2012] 
    
    top_archs = df_eff['Graphics Processor__Architecture'].value_counts().head(15).index.tolist()
    df_eff_filtered = df_eff[df_eff['Graphics Processor__Architecture'].isin(top_archs)].copy()
    arch_order = df_eff_filtered.groupby('Graphics Processor__Architecture')['Release_Year'].median().sort_values().index.tolist()

    # KPI 计算
    max_eff_row = df_eff_filtered.loc[df_eff_filtered['Perf_Per_Watt'].idxmax()]
    max_eff_val = max_eff_row['Perf_Per_Watt']
    max_eff_name = max_eff_row['Name']
    
    ada_median = df_eff_filtered[df_eff_filtered['Graphics Processor__Architecture'] == 'Ada Lovelace']['Perf_Per_Watt'].median()
    ampere_median = df_eff_filtered[df_eff_filtered['Graphics Processor__Architecture'] == 'Ampere']['Perf_Per_Watt'].median()
    leap_pct = ((ada_median - ampere_median) / ampere_median) * 100 if (pd.notna(ada_median) and pd.notna(ampere_median)) else 0

    # === 2. Tabs ===
    tab1, tab2 = st.tabs([
        ":material/battery_charging_full: The Solution: Efficiency", 
        ":material/dangerous: The Problem: Power & Frequency"
    ])

    # --- Tab 1: Efficiency (保持完美状态) ---
    with tab1:
        st.markdown("#### SOLUTION: GETTING SMARTER (GFLOPS PER WATT)")
        fig_eff = px.box(
            df_eff_filtered,
            x='Graphics Processor__Architecture',
            y='Perf_Per_Watt',
            color='Brand',
            points="all",
            hover_data=['Name', 'TDP_Watts', 'FP32_GFLOPS'],
            category_orders={'Graphics Processor__Architecture': arch_order},
            title="Efficiency Evolution: GFLOPS per Watt (Higher is Better)",
            height=500
        )
        # 美化字体
        fig_eff.update_layout(font=dict(family="Oswald, sans-serif"))
        st.plotly_chart(fig_eff, use_container_width=True)
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(":material/bolt: Peak Efficiency", f"{max_eff_val:.0f} GFLOPS/W", max_eff_name)
        m_col2.metric(":material/trending_up: Ada Lovelace Leap", f"+{leap_pct:.0f}%", "vs Ampere")
        m_col3.info("Blackwell drops slightly as it optimizes for AI (FP8), not FP32.")

    # --- Tab 2: Power Wall (核心修复区域) ---
    with tab2:
        # === Part A: 频率停滞 (Frequency Stagnation) ===
        st.markdown("#### 1. THE CAUSE: FREQUENCY STAGNATION")
        st.caption("Why do we need more power? Because we can't just increase clock speed anymore.")
        
        # 1. 计算原始数据的年度趋势
        raw_trend = df.groupby('Release_Year')['GPU_Clock_MHz'].agg(['max', 'mean']).reset_index()
        
        # 2. 强制创建一个完整的年份表 (1995 - 2026)
        # 这样不管原始数据里有没有2023、2024，X轴上都会有这些年份的位置
        full_years = pd.DataFrame({'Release_Year': np.arange(1995, 2027)})
        
        # 3. 合并并进行插值填充 (Interpolate)
        # merge 会让缺失年份的 max/mean 变成 NaN
        freq_trend = pd.merge(full_years, raw_trend, on='Release_Year', how='left')
        
        # interpolate 会根据前后年份的数据，画一条直线补上空缺
        freq_trend['max'] = freq_trend['max'].interpolate(method='linear', limit_direction='both')
        freq_trend['mean'] = freq_trend['mean'].interpolate(method='linear', limit_direction='both')

        fig_clock = go.Figure()

        # Line 1: 最大频率 (Max) - 加上 connectgaps=True 双重保险
        fig_clock.add_trace(go.Scatter(
            x=freq_trend['Release_Year'], y=freq_trend['max'],
            mode='lines+markers',
            name='Max Core Clock',
            line=dict(color='#FF4B4B', width=4), 
            marker=dict(color='#FF4B4B', size=6),
            connectgaps=True  # ✅ 强制连线，绝不断裂
        ))

        # Line 2: 平均频率 (Avg)
        fig_clock.add_trace(go.Scatter(
            x=freq_trend['Release_Year'], y=freq_trend['mean'],
            mode='lines',
            name='Average Clock',
            line=dict(color='grey', width=2, dash='dot'),
            connectgaps=True  # ✅ 强制连线
        ))

        # 标注
        fig_clock.add_annotation(
            x=2010, y=2000,
            text="🛑 Stagnation (The Wall)",
            showarrow=True, arrowhead=1, ay=-40
        )

        fig_clock.update_layout(
            title="GPU Clock Speeds (MHz): Hitting the Ceiling",
            yaxis_title="MHz",
            xaxis=dict(range=[1995, 2026]), # 强制X轴范围
            height=400,
            hovermode="x unified",
            font=dict(family="Oswald, sans-serif")
        )
        st.plotly_chart(fig_clock, use_container_width=True)

        st.divider() 

        # === Part B: 功耗激增 (TDP Explosion) ===
        st.markdown("#### 2. THE CONSEQUENCE: POWER EXPLOSION (TDP)")
        st.caption("Since we can't make clocks faster, we add more cores, which explodes power consumption.")
        
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
            y=300, line_dash="dash", line_color="red", 
            annotation_text="🛑 Old 300W Limit", annotation_position="bottom right"
        )

        fig_tdp.add_trace(go.Scatter(
            x=tdp_stats['Graphics Processor__Architecture'], 
            y=tdp_stats['max'],
            mode='lines+markers',
            name='Flagship Max TDP',
            line=dict(color='black', width=3, shape='linear'), 
            marker=dict(size=8, symbol='diamond')
        ))

        fig_tdp.add_trace(go.Scatter(
            x=tdp_stats['Graphics Processor__Architecture'], 
            y=tdp_stats['mean'],
            mode='lines',
            name='Average TDP',
            line=dict(color='grey', width=2, dash='dot')
        ))

        fig_tdp.update_layout(
            title="Power Consumption (TDP) Trends",
            yaxis_title="Watts",
            height=400,
            hovermode="x unified",
            font=dict(family="Oswald, sans-serif")
        )
        
        st.plotly_chart(fig_tdp, use_container_width=True)