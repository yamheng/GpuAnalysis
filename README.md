#  GPU-FINDER: A Data Storytelling Dashboard

### Analyzing the Limits of Silicon Physics & Economics (1986-2026)

**GPU-FINDER** is an interactive web application built with **Streamlit** that explores the evolution of Graphics Processing Units (GPUs) over the last 40 years. Moving beyond simple specification listings, this dashboard utilizes data storytelling to validate industry laws (Moore's Law, Dennard Scaling) and visualize the critical bottlenecks ("Walls") facing the semiconductor industry today.


##  Project Overview

* **Objective**: To tell the story of how GPUs evolved from simple display controllers to AI supercomputers, and to quantify the physical, thermodynamic, and economic barriers they now face.
* **Data Source**: A dataset of over 3000 GPUs (1986-2026) sourced from the TechPowerUp GPU Database.
* **Tech Stack**: Python, Streamlit, Plotly, Pandas, Scikit-learn.

##  Key Modules & Features

The dashboard is structured into narrative sections, each addressing a specific research question:

1.  ** Moore's Law (Physical Wall)**
    * Validates Gordon Moore's prediction using Transistor Density analysis.
    * Visualizes the "Reticle Limit" and the industry's shift towards **Chiplet (MCM)** technology to bypass physical sizing constraints.
    * *Key Insight*: Modern monolithic chips are hitting the physical size limit (~858mm²).

2.  ** Efficiency & Power (Power Wall)**
    * Tracks Performance per Watt (GFLOPS/W) evolution across major architectures.
    * Demonstrates the death of "Dennard Scaling" via **Frequency Stagnation** charts.
    * Visualizes the exponential rise in **TDP (Thermal Design Power)**.

3.  ** The Memory Wall**
    * Analyzes the widening gap between Compute Power and Memory Bandwidth.
    * Features an interactive **Sankey Diagram** to show strategic divergence: HBM adoption for servers vs. GDDR for consumers.

4.  ** The Economic Wall**
    * Plots the "Cost per Transistor" trend over 40 years.
    * *Key Insight*: The historical trend of exponential cost reduction has slowed or reversed with the advent of expensive 5nm/3nm nodes.

5.  ** AI Market Segmentation**
    * Applies **Unsupervised Learning (K-Means & t-SNE)** to cluster GPUs based purely on hardware specifications.
    * Visualizes market segmentation and reveals potential "overpriced" products by comparing hardware clusters with price tiers.

---

##  Installation & Usage

### Prerequisites
* Python 3.8 or higher
* pip (Python Package Installer)

### Step 1: Clone the Repository

git clone [https://github.com/yamheng/GpuAnalysis.git]
cd GpuAnalysis

### Step 2: Install Dependencies

It is recommended to create a virtual environment before installing.

# Install required packages
pip install -r requirements.txt

### Step 3: Run the App
streamlit run app.py

The dashboard will automatically open in your default web browser (usually at http://localhost:8501).

#  Project Structure
GpuAnalysis/
├── app.py                 # Main application entry point (Navigation & Routing)
├── requirements.txt       # Python dependencies list
├── gpu_1986-2026.csv      # Root dataset file
├── data/
│   └── gpu_1986-2026.csv  # Backup dataset directory
├── utils/
│   ├── data_loader.py     # Data ingestion, cleaning, regex parsing, and auto-patching
│   └── ui.py              # Custom UI styling (CSS injection for Monochrome/Oswald theme)
├── sections/              # Modular analysis components
│   ├── home.py            # Landing page with methodology
│   ├── data_info.py       # Data quality report & correlation heatmap
│   ├── moores_law.py      # Physical limits analysis module
│   ├── efficiency.py      # Power & Frequency analysis module
│   ├── memory_wall.py     # Bandwidth & Sankey diagram module
│   ├── economic.py        # Cost analysis module
│   ├── market_ai.py       # Machine Learning clustering module
│   └── contact.py         # Feedback form with GitHub Issue integration
└── assets/                # Static assets (Logos, Icons)