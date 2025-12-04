# for CONTACT/HELP page
import streamlit as st
import urllib.parse # Used for processing URL encoding

def show():
    st.markdown("## CONTACT & SUPPORT")
    st.markdown("### GET IN TOUCH OR BROWSE DOCUMENTATION")
    st.markdown("---")

    # Use a two-column layout: the left column is the form, and the right column is the document.
    col1, col2 = st.columns([1, 1], gap="large")

    # Left column: Contact form (GitHub) 
    with col1:
        st.markdown("#### :material/attach_email: SEND A MESSAGE")
        st.caption("Submit bugs or feature requests directly to our GitHub Repository.")
        
        # Create a form
        with st.form("contact_form"):
            st.caption("Fill in the details below to generate a pre-filled GitHub Issue.")
            
            # Input box
            name = st.text_input("YOUR NAME")
            email = st.text_input("YOUR EMAIL (Optional)")
            topic = st.selectbox("TOPIC", ["Report Data Error", "Feature Request", "Academic Inquiry", "General Feedback"])
            message = st.text_area("MESSAGE", height=150, placeholder="Describe your issue or suggestion...")
            
            # Submit button: Its current function is "Generate Link"
            submitted = st.form_submit_button("PREPARE GITHUB ISSUE", use_container_width=True)
        
        # The logic after form submission
        if submitted:
            if not name or not message:
                st.error("Please fill in at least your NAME and MESSAGE.")
            else:
                # 1. Construct the title and body of a GitHub Issue
                issue_title = f"[{topic}] Feedback from {name}"
                issue_body = f"""**User:** {name}
**Email:** {email}
**Topic:** {topic}

**Message:**
{message}

*(Auto-generated from GPU-FINDER Dashboard)*"""
                
                # 2. URL encoding (handling spaces, line breaks, etc.)
                params = urllib.parse.urlencode({'title': issue_title, 'body': issue_body})
                github_url = f"https://github.com/yamheng/GpuAnalysis/issues/new?{params}"
                
                # 3. Display the jump button
                st.success("Draft created! Click the button below to submit on GitHub:")
                st.link_button("OPEN GITHUB & SUBMIT", github_url, type="primary", use_container_width=True)

        st.markdown("---")
        st.markdown("#### :material/location_on: LAB LOCATION")
        st.markdown("""
        **Wuhan University of Technology** *Junshan Campus* 16 Hannan Avenue  
        Wuhan, China  
        *(EFREI Paris Joint Program)*
        """)

    # Right column: FAQ and citations
    with col2:
        st.markdown("#### :material/help: FREQUENTLY ASKED QUESTIONS")
        
        with st.expander("WHERE DOES THE DATA COME FROM?"):
            st.markdown("""
            The dataset is export from **[TechPowerUp GPU Specs Database](https://www.kaggle.com/datasets/ellimaaac/gpus-specs-from-1986-to-2026)**. 
            It covers over 3000 distinct SKUs released between 1986 and 2026. 
            We performed rigorous cleaning to standardize units (e.g., converting '4GB' and '512MB' to MB).
            """)
            
        with st.expander("HOW IS 'EFFICIENCY' CALCULATED?"):
            st.markdown("""
            Efficiency is defined as **GFLOPS per Watt**. 
            $$ Efficiency = \\frac{\\text{FP32 Performance (GFLOPS)}}{\\text{TDP (Watts)}} $$
            *Note: This metric uses 'Theoretical' performance, which may differ from real-world gaming benchmarks.*
            """)
            
        with st.expander("WHY IS THE 'ECONOMIC WALL' CURVE RISING?"):
            st.markdown("""
            Historically, cost per transistor dropped exponentially. 
            However, with the advent of **EUV Lithography** (7nm, 5nm, 3nm), the manufacturing cost per wafer has skyrocketed, offsetting the density gains.
            """)

        st.markdown("---")
        st.markdown("#### :material/library_books: CITATION")
        st.caption("If you use this tool for your research, please cite:")
        
        st.code("""
@misc{gpu_finder_2025,
  author = {Ruichen Liu},
  title = {GPU-FINDER: A Data Storytelling Dashboard},
  year = {2025},
  institution = {EFREI Paris / WUT},
  url = {https://github.com/yamheng/GpuAnalysis}
}
        """, language="bibtex")