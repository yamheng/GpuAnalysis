import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show(df):
    st.markdown("## :material/paid: The Economic Wall")
    st.markdown("### Is Moore's Law getting too expensive?")
    
    # 1. Data filtering, the price restriction should not be too strict to prevent filtering out all the cards of a certain year.
    df_eco = df.dropna(subset=['Launch_Price', 'Transistors_Million', 'Release_Year'])
    df_eco = df_eco[df_eco['Launch_Price'] > 50] 
    
    # Ensure the column exists
    if 'Cost_Per_Transistor' not in df_eco.columns:
        df_eco['Cost_Per_Transistor'] = df_eco['Launch_Price'] / df_eco['Transistors_Million']

    # 2. Calculate trend (median)
    cost_trend = df_eco.groupby('Release_Year')['Cost_Per_Transistor'].median().reset_index()

    fig_cost = go.Figure()

    # Layer 1: Background scatter points (black, semi-transparent)
    fig_cost.add_trace(go.Scattergl(
        x=df_eco['Release_Year'], y=df_eco['Cost_Per_Transistor'],
        mode='markers',
        name='Individual GPUs',
        marker=dict(color='black', opacity=0.2, size=5),
        text=df_eco['Name'],
        hovertemplate="<b>%{text}</b><br>Cost: $%{y:.4f} / M-Transistors<extra></extra>"
    ))

    # Layer 2: Trend line (thick blue line)
    fig_cost.add_trace(go.Scatter(
        x=cost_trend['Release_Year'], y=cost_trend['Cost_Per_Transistor'],
        mode='lines',
        name='Median Cost Trend',
        line=dict(color='#1565C0', width=5),
        connectgaps=True  # Automatic connection of breakpoints
    ))

    # Add annotations
    fig_cost.add_annotation(
        x=2022, y=cost_trend[cost_trend['Release_Year']==2022]['Cost_Per_Transistor'].values[0],
        text="Flattening / Rising?",
        showarrow=True, arrowhead=1, ay=-30
    )

    fig_cost.update_layout(
        title="Cost Per Million Transistors ($) - Log Scale",
        yaxis_type="log", # Note to use a logarithmic coordinate system
        yaxis_title="Cost ($) / Million Transistors",
        xaxis_title="Release Year",
        height=550,
        showlegend=True
    )
    
    st.plotly_chart(fig_cost, use_container_width=True)
    
    st.warning("""
    **Economic Insight:** The blue line shows the cost dropping exponentially for 20 years. 
    But look at the end (2020+): **The curve stops dropping**. 
    Advanced nodes (5nm/3nm) are so expensive that "Cost per Transistor" is no longer falling fast.
    """)