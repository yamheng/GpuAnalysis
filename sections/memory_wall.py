import streamlit as st
import plotly.graph_objects as go

def show(df):
    st.markdown("## :material/shield_locked: The Memory Wall Analysis")
    st.markdown("### BANDWIDTH BOTTLENECKS & TECHNOLOGY FLOW")

    # === PART 1: 交互式桑基图 ===
    st.markdown("#### 1. STRATEGY MAP: FROM CHAOS TO ORDER")
    is_focus = st.toggle("FOCUS MODE: FILTER NOISE & HIGHLIGHT BIG 3", value=False)

    # 1. 数据准备 & 清洗
    d = df.dropna(subset=['Brand', 'Memory__Memory Type']).copy()
    top_mem = ['GDDR6X', 'GDDR6', 'HBM2', 'HBM2e', 'HBM3', 'GDDR5', 'GDDR5X', 'HBM', 'DDR3', 'DDR4', 'SDRAM', 'DDR']
    d['Mem'] = d['Memory__Memory Type'].apply(lambda x: next((m for m in top_mem if m in str(x)), "Other"))

    # 2. 分支逻辑 (数据筛选)
    if is_focus:
        d = d[(d['Release_Year'] >= 2015) & (d['Brand'].isin(['NVIDIA', 'AMD', 'Intel'])) & (d['Mem'] != 'Other')]
        title = "Strategic Divergence (2015-2026): The Big Three"
    else:
        d = d[d['Brand'].isin(d['Brand'].value_counts().head(15).index)]
        title = "The Chaos of History (1986-2026): All Vendors"

    # 3. 流量计算 & 节点映射
    flow = d.groupby(['Brand', 'Mem']).size().reset_index(name='Count')
    nodes = list(flow['Brand'].unique()) + list(flow['Mem'].unique())
    node_map = {n: i for i, n in enumerate(nodes)}

    # 4. 高级配色逻辑 (这是保留美感的关键)
    brand_colors = {'NVIDIA': '#76B900', 'AMD': '#ED1C24', 'Intel': '#0071C5'}
    
    # 节点颜色：品牌用特定色，显存用黑色/深灰
    node_c = [brand_colors.get(n, 'black' if is_focus else '#333') for n in nodes]
    
    # 连线颜色：品牌色加透明度 (focus模式) 或 统一灰色 (chaos模式)
    if is_focus:
        link_c = [brand_colors.get(b, 'rgba(0,0,0,0.2)').replace('#', 'rgba(').replace(')', ',0.4)') 
                  if b in brand_colors else 'rgba(0,0,0,0.2)' for b in flow['Brand']]
        # 注意：简单的 hex->rgba 转换需要额外库，为了稳健我们手动映射
        link_map = {'NVIDIA': 'rgba(118, 185, 0, 0.4)', 'AMD': 'rgba(237, 28, 36, 0.4)', 'Intel': 'rgba(0, 113, 197, 0.4)'}
        link_c = [link_map.get(b, 'rgba(0,0,0,0.2)') for b in flow['Brand']]
    else:
        link_c = ["rgba(0, 0, 0, 0.15)"] * len(flow)

    # 5. 绘图 (保留所有样式)
    fig = go.Figure(go.Sankey(
        textfont=dict(color="black", size=12, family="Oswald"),
        node=dict(pad=15, thickness=15, line=dict(color="white", width=0.5), label=nodes, color=node_c),
        link=dict(source=flow['Brand'].map(node_map), target=flow['Mem'].map(node_map), value=flow['Count'], color=link_c)
    ))
    st.plotly_chart(fig.update_layout(title=title, height=600, font=dict(family="Oswald")), use_container_width=True)

    st.divider()

    # === PART 2: 带宽 Gap 图 (保留原设计) ===
    st.markdown("#### 2. THE BANDWIDTH GAP")
    
    # 趋势计算
    trend = df[(df['Release_Year'] >= 2010) & (df['Release_Year'] <= 2024)].groupby('Release_Year')[['FP32_GFLOPS', 'Bandwidth_GBs']].mean()
    
    if not trend.empty:
        # 归一化 (以 2013 为基准)
        base = trend.loc[2013] if 2013 in trend.index else trend.iloc[0]
        trend = (trend / base) * 100
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=trend.index, y=trend['FP32_GFLOPS'], name='Compute Growth', line=dict(color='#FF4B4B', width=4)))
        fig2.add_trace(go.Scatter(x=trend.index, y=trend['Bandwidth_GBs'], name='Bandwidth Growth', 
                                 line=dict(color='#1565C0', width=4), fill='tonexty', fillcolor='rgba(255, 75, 75, 0.2)'))

        fig2.update_layout(
            title="The Growing Gap: Compute vs Bandwidth (Index 100 = 2013)",
            yaxis_title="Growth Index", height=600, hovermode="x unified",
            font=dict(family="Oswald, sans-serif")
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("The red shaded area represents the **Memory Wall**. Compute is growing much faster than bandwidth.")
    else:
        st.error("Insufficient data for trend analysis.")