# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import io



# st.title("Interactive Data Explorer & Analyzer")
# st.sidebar.header("Upload Your Dataset")

# # File uploader in the sidebar (accepts CSV and Excel files)
# uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

# if uploaded_file is not None:
#     try:
#         # Load the file into a DataFrame
#         if uploaded_file.name.endswith('csv'):
#             df = pd.read_csv(uploaded_file)
#         else:
#             df = pd.read_excel(uploaded_file)
        
#         st.write("### Dataset Preview")
#         st.dataframe(df.head())
        
#         # Display basic dataset info
#         st.write("### Dataset Info")
#         st.write(f"**Shape:** {df.shape}")
#         st.write("**Columns:**", list(df.columns))
#         st.write("**Missing Values per Column:**")
#         st.dataframe(df.isnull().sum().to_frame(name="Missing Values"))
        
#         # Summary statistics
#         st.write("### Summary Statistics")
#         st.dataframe(df.describe())
        

        
#         # Visualization options in the sidebar
#         st.sidebar.header("Visualization Options")
#         chart_type = st.sidebar.selectbox("Select Chart Type", 
#                                           ["Histogram", "Scatter Plot", "Box Plot", "Line Chart"])
        
#         if chart_type == "Histogram":
#             num_cols = df.select_dtypes(include=["number"]).columns
#             if len(num_cols) > 0:
#                 col = st.sidebar.selectbox("Select column for Histogram", num_cols)
#                 fig = px.histogram(df, x=col, title=f"Histogram of {col}")
#                 st.plotly_chart(fig)
#             else:
#                 st.info("No numeric columns available for histogram.")
        
#         elif chart_type == "Scatter Plot":
#             num_cols = df.select_dtypes(include=["number"]).columns
#             if len(num_cols) >= 2:
#                 x_col = st.sidebar.selectbox("X-axis", num_cols, index=0)
#                 y_col = st.sidebar.selectbox("Y-axis", num_cols, index=1)
#                 fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
#                 st.plotly_chart(fig)
#             else:
#                 st.info("Need at least two numeric columns for scatter plot.")
        
#         elif chart_type == "Box Plot":
#             num_cols = df.select_dtypes(include=["number"]).columns
#             if len(num_cols) > 0:
#                 col = st.sidebar.selectbox("Select column for Box Plot", num_cols)
#                 fig = px.box(df, y=col, title=f"Box Plot of {col}")
#                 st.plotly_chart(fig)
#             else:
#                 st.info("No numeric columns available for box plot.")
        
#         elif chart_type == "Line Chart":
#             # For line chart, x-axis can be non-numeric (like dates or categorical data)
#             x_col = st.sidebar.selectbox("Select X-axis column", df.columns)
#             num_cols = df.select_dtypes(include=["number"]).columns
#             if len(num_cols) > 0:
#                 y_col = st.sidebar.selectbox("Select Y-axis column", num_cols)
#                 fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart: {y_col} over {x_col}")
#                 st.plotly_chart(fig)
#             else:
#                 st.info("No numeric columns available for line chart.")
                
#     except Exception as e:
#         st.error("Error loading file: " + str(e))
# else:
#     st.info("Please upload a dataset to begin.")




import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.title("Advanced Interactive Data Explorer & Analyzer")

# Sidebar: File Upload
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load file into DataFrame
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
        
        st.write("### Summary Statistics")
        st.dataframe(df.describe())

        # Sidebar: Data Filtering & Cleaning
        st.sidebar.header("Data Filtering")
        filtered_df = df.copy()

        # Filter numeric columns with sliders
        num_cols = filtered_df.select_dtypes(include=['number']).columns
        if len(num_cols) > 0:
            st.sidebar.subheader("Filter Numeric Columns")
            for col in num_cols:
                col_min = float(filtered_df[col].min())
                col_max = float(filtered_df[col].max())
                selected_range = st.sidebar.slider(f"{col} range", min_value=col_min, max_value=col_max, value=(col_min, col_max))
                filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[1])]
        
        # Filter categorical columns using multiselect
        cat_cols = filtered_df.select_dtypes(include=['object', 'category']).columns
        if len(cat_cols) > 0:
            st.sidebar.subheader("Filter Categorical Columns")
            for col in cat_cols:
                unique_vals = filtered_df[col].dropna().unique().tolist()
                selected_vals = st.sidebar.multiselect(f"Filter {col}", options=unique_vals, default=unique_vals)
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
        
        st.write("### Filtered Dataset Preview")
        st.dataframe(filtered_df.head())
        st.write(f"Filtered shape: {filtered_df.shape}")

        # Export filtered data as CSV
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered Data as CSV", data=csv_data, file_name="filtered_data.csv", mime="text/csv")

        # Sidebar: Visualization Options
        st.sidebar.header("Visualization Options")
        chart_type = st.sidebar.selectbox("Select Chart Type", 
                                          ["Histogram", "Scatter Plot", "Box Plot", "Line Chart", "Density Plot", "Correlation Matrix"])
        
        if chart_type == "Histogram":
            if len(num_cols) > 0:
                col = st.sidebar.selectbox("Select column for Histogram", num_cols)
                fig = px.histogram(filtered_df, x=col, title=f"Histogram of {col}")
                st.plotly_chart(fig)
            else:
                st.info("No numeric columns available for histogram.")
        
        elif chart_type == "Scatter Plot":
            if len(num_cols) >= 2:
                x_col = st.sidebar.selectbox("X-axis", num_cols, index=0)
                y_col = st.sidebar.selectbox("Y-axis", num_cols, index=1)
                fig = px.scatter(filtered_df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
                st.plotly_chart(fig)
            else:
                st.info("Need at least two numeric columns for scatter plot.")
        
        elif chart_type == "Box Plot":
            if len(num_cols) > 0:
                col = st.sidebar.selectbox("Select column for Box Plot", num_cols)
                fig = px.box(filtered_df, y=col, title=f"Box Plot of {col}")
                st.plotly_chart(fig)
            else:
                st.info("No numeric columns available for box plot.")
        
        elif chart_type == "Line Chart":
            # X-axis can be any column (e.g., dates or categories)
            x_col = st.sidebar.selectbox("Select X-axis column", filtered_df.columns)
            if len(num_cols) > 0:
                y_col = st.sidebar.selectbox("Select Y-axis column", num_cols)
                fig = px.line(filtered_df, x=x_col, y=y_col, title=f"Line Chart: {y_col} over {x_col}")
                st.plotly_chart(fig)
            else:
                st.info("No numeric columns available for line chart.")
        
        elif chart_type == "Density Plot":
            if len(num_cols) > 0:
                col = st.sidebar.selectbox("Select column for Density Plot", num_cols)
                fig = px.density_contour(filtered_df, x=col, title=f"Density Plot of {col}")
                st.plotly_chart(fig)
            else:
                st.info("No numeric columns available for density plot.")
        
        elif chart_type == "Correlation Matrix":
            if len(num_cols) > 1:
                corr_matrix = filtered_df[num_cols].corr()
                fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Matrix Heatmap")
                st.plotly_chart(fig)
            else:
                st.info("Not enough numeric columns to compute correlation matrix.")
                
    except Exception as e:
        st.error("Error loading file: " + str(e))
else:
    st.info("Please upload a dataset to begin.")
