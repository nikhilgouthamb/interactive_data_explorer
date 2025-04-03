import streamlit as st
import pandas as pd
import plotly.express as px
import io

# For optional Pandas Profiling report
if st.sidebar.button("Generate Pandas Profiling Report"):
    try:
        profile = ProfileReport(df, explorative=True)
        # Convert report to HTML and embed it directly in Streamlit
        html = profile.to_html()
        st.components.v1.html(html, height=1000, scrolling=True)
    except Exception as e:
        st.error("Error generating profiling report: " + str(e))

st.title("Interactive Data Explorer & Analyzer")
st.sidebar.header("Upload Your Dataset")

# File uploader in the sidebar (accepts CSV and Excel files)
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load the file into a DataFrame
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("### Dataset Preview")
        st.dataframe(df.head())
        
        # Display basic dataset info
        st.write("### Dataset Info")
        st.write(f"**Shape:** {df.shape}")
        st.write("**Columns:**", list(df.columns))
        st.write("**Missing Values per Column:**")
        st.dataframe(df.isnull().sum().to_frame(name="Missing Values"))
        
        # Summary statistics
        st.write("### Summary Statistics")
        st.dataframe(df.describe())
        
        # Optional: Generate Pandas Profiling Report
        if st.sidebar.button("Generate Pandas Profiling Report"):
            try:
                profile = ProfileReport(df, explorative=True)
                st_profile_report(profile)
            except Exception as e:
                st.error("Error generating profiling report: " + str(e))
        
        # Visualization options in the sidebar
        st.sidebar.header("Visualization Options")
        chart_type = st.sidebar.selectbox("Select Chart Type", 
                                          ["Histogram", "Scatter Plot", "Box Plot", "Line Chart"])
        
        if chart_type == "Histogram":
            num_cols = df.select_dtypes(include=["number"]).columns
            if len(num_cols) > 0:
                col = st.sidebar.selectbox("Select column for Histogram", num_cols)
                fig = px.histogram(df, x=col, title=f"Histogram of {col}")
                st.plotly_chart(fig)
            else:
                st.info("No numeric columns available for histogram.")
        
        elif chart_type == "Scatter Plot":
            num_cols = df.select_dtypes(include=["number"]).columns
            if len(num_cols) >= 2:
                x_col = st.sidebar.selectbox("X-axis", num_cols, index=0)
                y_col = st.sidebar.selectbox("Y-axis", num_cols, index=1)
                fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
                st.plotly_chart(fig)
            else:
                st.info("Need at least two numeric columns for scatter plot.")
        
        elif chart_type == "Box Plot":
            num_cols = df.select_dtypes(include=["number"]).columns
            if len(num_cols) > 0:
                col = st.sidebar.selectbox("Select column for Box Plot", num_cols)
                fig = px.box(df, y=col, title=f"Box Plot of {col}")
                st.plotly_chart(fig)
            else:
                st.info("No numeric columns available for box plot.")
        
        elif chart_type == "Line Chart":
            # For line chart, x-axis can be non-numeric (like dates or categorical data)
            x_col = st.sidebar.selectbox("Select X-axis column", df.columns)
            num_cols = df.select_dtypes(include=["number"]).columns
            if len(num_cols) > 0:
                y_col = st.sidebar.selectbox("Select Y-axis column", num_cols)
                fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart: {y_col} over {x_col}")
                st.plotly_chart(fig)
            else:
                st.info("No numeric columns available for line chart.")
                
    except Exception as e:
        st.error("Error loading file: " + str(e))
else:
    st.info("Please upload a dataset to begin.")
