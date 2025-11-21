# 文件路径: sections/moores_law.py
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show(df):
    st.markdown("## 📉 Moore's Law Validator")
    st.markdown("### Question: Are we hitting the physical wall?")

    # --- 1. 过滤器 (从侧边栏移至主界面，保持布局整洁) ---
    with st.expander("⚙️ Filter Settings", expanded=True):
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

    # --- 3. 绘图逻辑 (保持原样) ---
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
            hovertemplate=f"<b>{{text}}</b><br>Foundry: {foundry}<br>Density: {{y:.2f}} M/mm²<br>Year: {{x}}<extra></extra>",
            text=subset['Name']
        ))

    # 绘制工艺制程趋势线 (黑线)
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
    
    st.info("""
    **📈 Interpretation:**
    The black dashed line shows the **Process Node** shrinking (steps down). 
    Every time it steps down, the colored dots (Transistor Density) jump up. 
    This confirms that process shrinkage is the engine behind Moore's Law.
    """)