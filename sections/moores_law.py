import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show(df):
    st.markdown("## :material/ssid_chart: Moore's Law (Physical Limits)")
    st.markdown("### Chapter 1: The Physical Wall")

    # --- 1. 过滤器 ---
    with st.expander("Filter Settings", expanded=False, icon=":material/shield_locked:"):
        col_filters, col_display = st.columns([1, 3])
        with col_filters:
            valid_foundries = df['Graphics Processor__Foundry'].dropna().unique()
            foundry_filter = st.multiselect(
                "Select Foundry", 
                options=valid_foundries,
                default=['TSMC', 'Samsung', 'Intel', 'GlobalFoundries', 'UMC']
            )
            show_regression = st.checkbox("Show Regression Line", value=True)

    # --- 2. 数据准备 ---
    mask = (
        (df['Graphics Processor__Foundry'].isin(foundry_filter)) & 
        (df['Release_Year'] > 1990) & 
        ((df['Transistor_Density'].notna()) | (df['Process_Size_nm'].notna()))
    )
    df_moore = df[mask].copy()

    # --- 3. 绘图逻辑 ---
    color_map = {
        'TSMC': '#FF6347', 'Samsung': '#32CD32', 'Intel': "#1D5DBC",
        'GlobalFoundries': '#911EB4', 'UMC': "#EEF10F", 'Sony': '#000000',
    }
    def get_color(foundry):
        return color_map.get(foundry, '#808080')
    
    fig = go.Figure()

    # 绘制各个代工厂的点
    for foundry in foundry_filter:
        subset = df_moore[df_moore['Graphics Processor__Foundry'] == foundry]
        if subset.empty: continue
        
        fig.add_trace(go.Scattergl(
            x=subset['Release_Year'],
            y=subset['Transistor_Density'],
            mode='markers',
            marker=dict(color=get_color(foundry), size=8, opacity=0.8, line=dict(width=1, color='white')),
            name=foundry,
            yaxis='y1',
            # ✅ 修复点：加上了 %，并正确处理了 f-string 转义
            hovertemplate=f"<b>%{{text}}</b><br>Foundry: {foundry}<br>Density: %{{y:.2f}} M/mm²<br>Year: %{{x}}<extra></extra>",
            text=subset['Name']
        ))

    # 绘制工艺制程趋势线
    process_trend = df_moore.groupby('Release_Year')['Process_Size_nm'].min().reset_index()
    fig.add_trace(go.Scatter(
        x=process_trend['Release_Year'],
        y=process_trend['Process_Size_nm'],
        mode='lines+markers',
        name='Process Node (nm)',
        line=dict(color='black', width=4, dash='dot'),
        marker=dict(color='black', size=6, symbol='x'),
        yaxis='y2',
        opacity=0.6
    ))

    # 绘制回归线
    if show_regression:
        df_reg = df_moore.dropna(subset=['Release_Year', 'Transistor_Density'])
        if len(df_reg) > 10:
            x = df_reg['Release_Year']
            y = np.log10(df_reg['Transistor_Density'])
            m, b = np.polyfit(x, y, 1)
            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = 10**(m * x_line + b)
            fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Moore\'s Law (Fit)', line=dict(color='grey', width=2, dash='solid'), yaxis='y1'))

    # 布局设置
    fig.update_layout(
        title="Transistor Density vs. Process Node (nm)",
        xaxis=dict(title="Release Year"),
        yaxis=dict(title="Transistor Density (M/mm²) - Log Scale", type="log"),
        yaxis2=dict(title="Process Node (nm)", overlaying="y", side="right", autorange="reversed"),
        height=600,
        legend=dict(orientation="h", y=1.1, x=0),
        margin=dict(t=50, r=50) 
    )

    st.plotly_chart(fig, use_container_width=True)
# --- 4. 第二张图：芯片面积 (Physical Wall) ---
    st.markdown("---")
    st.markdown("### :material/shield_locked: The Physical Wall: Reticle Limit vs. Chiplets")
    st.markdown("Standard chips hit the wall at ~858mm². Points above this line use **Chiplet (MCM)** technology.")

    df_die = df.dropna(subset=['Die_Size_mm2', 'Release_Year'])
    
    fig_die = go.Figure()
    
    # 1. 绘制普通点
    fig_die.add_trace(go.Scatter(
        x=df_die['Release_Year'], y=df_die['Die_Size_mm2'],
        mode='markers', name='Single Die',
        marker=dict(color='black', opacity=0.3, size=6),
        hovertemplate="<b>%{text}</b><br>Size: %{y} mm²<br>Year: %{x}<extra></extra>",
        text=df_die['Name']
    ))
    
    # 2. 绘制“越界”的点 (Chiplets) - 单独高亮
    df_chiplets = df_die[df_die['Die_Size_mm2'] > 858]
    fig_die.add_trace(go.Scatter(
        x=df_chiplets['Release_Year'], y=df_chiplets['Die_Size_mm2'],
        mode='markers+text', name='Multi-Chip (Chiplet)',
        textposition="top center",
        marker=dict(color='#FF4B4B', size=10, symbol='star'),
        hovertemplate="<b>%{text}</b><br>Size: %{y} mm²<br>Tech: Chiplet/MCM<extra></extra>",
        text=df_chiplets['Name'] # 显示名字
    ))
    
    # 3. 添加光罩极限线
    fig_die.add_hline(
        y=858, line_width=3, line_dash="dash", line_color="red",
        annotation_text="🛑 Reticle Limit (Single Die Max)", annotation_position="bottom right"
    )

    fig_die.update_layout(
        title="Breaking the Limit: Monolithic vs. Chiplet Era",
        yaxis_title="Die Size (mm²)",
        height=550,
        showlegend=True
    )
    st.plotly_chart(fig_die, use_container_width=True)
    
    st.caption("""
    **Answer to your question:** Why are some points above the red line?
    Those are **Chiplets** (e.g., NVIDIA Blackwell, AMD MI300). They stitch multiple dies together to bypass the physical limit of a single exposure (~858mm²).
    """)