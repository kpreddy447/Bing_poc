import streamlit as st
from PIL import Image
from backend import analyze_graphs
from db_connector import load_data_from_postgres
import pandas as pd
import plotly.express as px
import os

# Streamlit page config
st.set_page_config(layout="wide")
st.title("Graph Comparison")

# Initialize session state for chart paths
if "chart_paths" not in st.session_state:
    st.session_state.chart_paths = {"path1": None, "path2": None}

# Load restaurant list
query = 'SELECT DISTINCT restaurant_name FROM public.main_table'
restaurants_df = load_data_from_postgres(query)
restaurants_df.columns = restaurants_df.columns.str.strip()
col_name = restaurants_df.columns[0]
restaurant_list = restaurants_df[col_name].dropna().sort_values().unique().tolist()

restaurant_name = st.selectbox("Select a Restaurant", restaurant_list)

# Date selection
col1, col2 = st.columns(2)
with col1:
    start_date_1 = st.date_input("Start Date (Period 1)")
    end_date_1 = st.date_input("End Date (Period 1)")
with col2:
    start_date_2 = st.date_input("Start Date (Period 2)")
    end_date_2 = st.date_input("End Date (Period 2)")

# Helper function to save charts
def save_plotly_chart(df, x_col, y_col, title, save_dir="charts"):
    fig = px.line(df, x=x_col, y=y_col, title=title)

    # Ensure x-axis shows readable date format
    fig.update_xaxes(
        title_text="Date",
        tickformat="%b %d",  # Format: Jan 01, Feb 15
        tickangle=-45
    )
    fig.update_yaxes(title_text="Total Bill Amount")

    os.makedirs(save_dir, exist_ok=True)
    filename = f"{title.replace(' ', '_')}.png"
    file_path = os.path.join(save_dir, filename)
    fig.write_image(file_path)
    return fig, file_path

# Generate charts
if st.button("Generate Comparison Chart"):
    query = 'SELECT * FROM public.main_table WHERE restaurant_name = %s'
    df = load_data_from_postgres(query, params=(restaurant_name,))

    # Convert columns to proper formats
    df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
    df["total_bill_amount"] = pd.to_numeric(df["total_bill_amount"], errors='coerce')

    # Convert input dates to datetime64[ns] for comparison
    start_date_1 = pd.to_datetime(start_date_1)
    end_date_1 = pd.to_datetime(end_date_1)
    start_date_2 = pd.to_datetime(start_date_2)
    end_date_2 = pd.to_datetime(end_date_2)

    # Filter by date
    period1 = df[(df["date_of_visit"] >= start_date_1) & (df["date_of_visit"] <= end_date_1)]
    period2 = df[(df["date_of_visit"] >= start_date_2) & (df["date_of_visit"] <= end_date_2)]

    # Group by just the date (not full datetime)
    daily_rev_1 = period1.groupby(period1["date_of_visit"].dt.date)["total_bill_amount"].sum().reset_index()
    daily_rev_2 = period2.groupby(period2["date_of_visit"].dt.date)["total_bill_amount"].sum().reset_index()

    # Rename to standard column name for plotting
    daily_rev_1.rename(columns={"date_of_visit": "Date"}, inplace=True)
    daily_rev_2.rename(columns={"date_of_visit": "Date"}, inplace=True)

    # Save charts
    fig1, path1 = save_plotly_chart(daily_rev_1, "Date", "total_bill_amount", "Revenue Line Chart - Period 1")
    fig2, path2 = save_plotly_chart(daily_rev_2, "Date", "total_bill_amount", "Revenue Line Chart - Period 2")

    # Save paths in session state
    st.session_state.chart_paths["path1"] = path1
    st.session_state.chart_paths["path2"] = path2

# Load from session state
path1 = st.session_state.chart_paths["path1"]
path2 = st.session_state.chart_paths["path2"]

# Display charts in sidebar
if path1 and os.path.exists(path1):
    st.sidebar.image(Image.open(path1), caption="Graph 1", use_container_width=True)

if path2 and os.path.exists(path2):
    st.sidebar.image(Image.open(path2), caption="Graph 2", use_container_width=True)

# Button to compare charts using LLM
if path1 and path2:
    if st.button("Compare Graphs"):
        with st.spinner("Analyzing..."):
            # comparison_text = analyze_graphs(path1, path2)
            comparison_text = analyze_graphs(path1, path2, restaurant_name, start_date_1, end_date_1, start_date_2, end_date_2)

        st.markdown("### Comparison Summary")
        st.write(comparison_text)
else:
    st.info("Generate both graphs to enable comparison.")


# import streamlit as st
# from PIL import Image
# from backend import analyze_graphs  
# from db_connector import load_data_from_postgres
# import pandas as pd
# import plotly.express as px
# import os

# # Streamlit page config
# st.set_page_config(layout="wide")
# st.title("Graph Comparison")

# # Initialize session state for chart paths
# if "chart_paths" not in st.session_state:
#     st.session_state.chart_paths = {"path1": None, "path2": None}

# # Load restaurant list
# query = 'SELECT DISTINCT restaurant_name FROM public.main_table'
# restaurants_df = load_data_from_postgres(query)
# restaurants_df.columns = restaurants_df.columns.str.strip()
# col_name = restaurants_df.columns[0]
# restaurant_list = restaurants_df[col_name].dropna().sort_values().unique().tolist()

# restaurant_name = st.selectbox("Select a Restaurant", restaurant_list)

# # Date selection
# col1, col2 = st.columns(2)
# with col1:
#     start_date_1 = st.date_input("Start Date (Period 1)")
#     end_date_1 = st.date_input("End Date (Period 1)")
# with col2:
#     start_date_2 = st.date_input("Start Date (Period 2)")
#     end_date_2 = st.date_input("End Date (Period 2)")

# # Helper function to save charts
# def save_plotly_chart(df, x_col, y_col, title, save_dir="charts"):
#     print(x_col,y_col)
#     fig = px.line(df, x=x_col, y=y_col, title=title)
#     os.makedirs(save_dir, exist_ok=True)
#     filename = f"{title.replace(' ', '_')}.png"
#     file_path = os.path.join(save_dir, filename)
#     fig.write_image(file_path)
#     return fig, file_path

# # Generate charts
# if st.button("Generate Comparison Chart"):
#     query = 'SELECT * FROM public.main_table WHERE restaurant_name = %s'
#     df = load_data_from_postgres(query, params=(restaurant_name,))

#     df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
#     df["total_bill_amount"] = pd.to_numeric(df["total_bill_amount"], errors='coerce')

#     # Filter by date
#     period1 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_1)) & 
#                  (df["date_of_visit"] <= pd.to_datetime(end_date_1))]
#     period2 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_2)) & 
#                  (df["date_of_visit"] <= pd.to_datetime(end_date_2))]

#     # Group by day
#     daily_rev_1 = period1.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()
#     daily_rev_2 = period2.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()

#     # Save charts
#     fig1, path1 = save_plotly_chart(daily_rev_1, "date_of_visit", "total_bill_amount", "Revenue Line Chart - Period 1")
#     fig2, path2 = save_plotly_chart(daily_rev_2, "date_of_visit", "total_bill_amount", "Revenue Line Chart - Period 2")

#     # Save paths in session state
#     st.session_state.chart_paths["path1"] = path1
#     st.session_state.chart_paths["path2"] = path2

# # Load from session state
# path1 = st.session_state.chart_paths["path1"]
# path2 = st.session_state.chart_paths["path2"]

# if path1 and os.path.exists(path1):
#     st.sidebar.image(Image.open(path1), caption="Graph 1", use_container_width=True)

# if path2 and os.path.exists(path2):
#     st.sidebar.image(Image.open(path2), caption="Graph 2", use_container_width=True)

# if path1 and path2:
#     if st.button("Compare Graphs"):
#         with st.spinner("Analyzing..."):
#             comparison_text = analyze_graphs(path1, path2)

#         st.markdown("### Comparison Summary")
#         st.write(comparison_text)
# else:
#     st.info("Generate both graphs to enable comparison.")


# # import streamlit as st
# # from PIL import Image
# # from backend import analyze_graphs  
# # from db_connector import load_data_from_postgres
# # import pandas as pd
# # import plotly.express as px
# # import os


# # st.set_page_config(layout="wide")
# # st.title("Graph Comparison")

# # query = 'SELECT DISTINCT restaurant_name FROM public.main_table'
# # restaurants_df = load_data_from_postgres(query)
# # restaurants_df.columns = restaurants_df.columns.str.strip()
# # col_name = restaurants_df.columns[0]
# # restaurant_list = restaurants_df[col_name].dropna().sort_values().unique().tolist()

# # restaurant_name = st.selectbox("Select a Restaurant", restaurant_list)

# # col1, col2 = st.columns(2)
# # with col1:
# #     start_date_1 = st.date_input("Start Date (Period 1)")
# #     end_date_1 = st.date_input("End Date (Period 1)")
# # with col2:
# #     start_date_2 = st.date_input("Start Date (Period 2)")
# #     end_date_2 = st.date_input("End Date (Period 2)")

# # def save_plotly_chart(df, x_col, y_col, title, save_dir="charts"):
# #     fig = px.line(df, x=x_col, y=y_col, title=title)

# #     os.makedirs(save_dir, exist_ok=True)

# #     filename = f"{title.replace(' ', '_')}.png"
# #     file_path = os.path.join(save_dir, filename)

# #     fig.write_image(file_path)
# #     return fig, file_path


# # if st.button("Generate Comparison Chart"):
# #     query = 'SELECT * FROM public.main_table WHERE restaurant_name = %s'
# #     df = load_data_from_postgres(query, params=(restaurant_name,))

# #     df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
# #     df["total_bill_amount"] = pd.to_numeric(df["total_bill_amount"], errors='coerce')

# #     period1 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_1)) & 
# #                  (df["date_of_visit"] <= pd.to_datetime(end_date_1))]
# #     period2 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_2)) & 
# #                  (df["date_of_visit"] <= pd.to_datetime(end_date_2))]

# #     daily_rev_1 = period1.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()
# #     daily_rev_2 = period2.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()

# #     img1, path1 = save_plotly_chart(daily_rev_1, "date_of_visit", "total_bill_amount", "Revenue Line Chart - Period 1")
# #     img2, path2 = save_plotly_chart(daily_rev_2, "date_of_visit", "total_bill_amount", "Revenue Line Chart - Period 2")

# #     if img1:
# #         st.sidebar.image(Image.open(path1), caption="Graph 1", use_container_width=True)

# #     if img2:
# #         st.sidebar.image(Image.open(path2), caption="Graph 2", use_container_width=True)
# #     st.write(img1)
# #     st.write(path1)
# #     st.write(img2)
# #     st.write(path2)
# #     if path1 and path2:
# #         if st.button("Compare Graphs"):
# #             with st.spinner("Analyzing..."):
# #                 comparison_text = analyze_graphs(path1, path2)

# #             st.markdown("### Comparison Summary")
# #             st.write(comparison_text)


# #     else:
# #         st.info("Upload two graph images in the sidebar to enable comparison.")
