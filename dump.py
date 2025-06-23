# app.py

# import streamlit as st
# import pandas as pd
# from db_connector import load_data_from_postgres  # Replace 'your_module' with actual filename

# st.title("📈 Revenue Comparison by Date Range")

# # Load distinct restaurant names safely
# query = 'SELECT DISTINCT restaurant_name FROM public.main_table'
# restaurants_df = load_data_from_postgres(query)
# restaurants_df.columns = restaurants_df.columns.str.strip()
# col_name = restaurants_df.columns[0]
# restaurant_list = restaurants_df[col_name].dropna().sort_values().unique().tolist()

# # Dropdown to select restaurant
# restaurant_name = st.selectbox("Select a Restaurant", restaurant_list)

# col1, col2 = st.columns(2)
# with col1:
#     start_date_1 = st.date_input("Start Date (Period 1)")
#     end_date_1 = st.date_input("End Date (Period 1)")
# with col2:
#     start_date_2 = st.date_input("Start Date (Period 2)")
#     end_date_2 = st.date_input("End Date (Period 2)")

# if st.button("Generate Comparison Chart"):
#     # Use parameterized query here to avoid SQL injection / quoting issues
#     query = 'SELECT * FROM public.main_table WHERE restaurant_name = %s'
#     df = load_data_from_postgres(query, params=(restaurant_name,))

#     df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
#     df["total_bill_amount"] = pd.to_numeric(df["total_bill_amount"], errors='coerce')

#     # Filter each period
#     period1 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_1)) & 
#                  (df["date_of_visit"] <= pd.to_datetime(end_date_1))]
#     period2 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_2)) & 
#                  (df["date_of_visit"] <= pd.to_datetime(end_date_2))]

#     # Aggregate revenue per day
#     daily_rev_1 = period1.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()
#     daily_rev_1["Period"] = "Period 1"

#     daily_rev_2 = period2.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()
#     daily_rev_2["Period"] = "Period 2"

#     combined = pd.concat([daily_rev_1, daily_rev_2])

#     st.subheader("📊 Revenue Line Chart - Period 1")
#     st.line_chart(data=daily_rev_1, x="date_of_visit", y="total_bill_amount")

#     st.subheader("📊 Revenue Line Chart - Period 2")
#     st.line_chart(data=daily_rev_2, x="date_of_visit", y="total_bill_amount")

#     st.subheader("📄 Summary Table")
#     st.dataframe(combined)


# app.py


# import streamlit as st
# import pandas as pd
# from db_connector import load_data_from_postgres  # Your database connector
# from llm_summary import generate_analysis_summary

# st.title("📈 Revenue Comparison by Date Range")

# # Load distinct restaurant names safely
# query = 'SELECT DISTINCT restaurant_name FROM public.main_table'
# restaurants_df = load_data_from_postgres(query)
# restaurants_df.columns = restaurants_df.columns.str.strip()
# col_name = restaurants_df.columns[0]
# restaurant_list = restaurants_df[col_name].dropna().sort_values().unique().tolist()

# # Dropdown to select restaurant
# restaurant_name = st.selectbox("Select a Restaurant", restaurant_list)

# col1, col2 = st.columns(2)
# with col1:
#     start_date_1 = st.date_input("Start Date (Period 1)")
#     end_date_1 = st.date_input("End Date (Period 1)")
# with col2:
#     start_date_2 = st.date_input("Start Date (Period 2)")
#     end_date_2 = st.date_input("End Date (Period 2)")

# if st.button("Generate Comparison Chart"):
#     query = 'SELECT * FROM public.main_table WHERE restaurant_name = %s'
#     df = load_data_from_postgres(query, params=(restaurant_name,))

#     df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
#     df["total_bill_amount"] = pd.to_numeric(df["total_bill_amount"], errors='coerce')

#     # Filter each period
#     period1 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_1)) & 
#                  (df["date_of_visit"] <= pd.to_datetime(end_date_1))]
#     period2 = df[(df["date_of_visit"] >= pd.to_datetime(start_date_2)) & 
#                  (df["date_of_visit"] <= pd.to_datetime(end_date_2))]

#     # Aggregate revenue per day
#     daily_rev_1 = period1.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()
#     daily_rev_2 = period2.groupby("date_of_visit")["total_bill_amount"].sum().reset_index()

#     st.subheader("📊 Revenue Line Chart - Period 1")
#     st.line_chart(data=daily_rev_1, x="date_of_visit", y="total_bill_amount")

#     st.subheader("📊 Revenue Line Chart - Period 2")
#     st.line_chart(data=daily_rev_2, x="date_of_visit", y="total_bill_amount")

#     combined = pd.concat([
#         daily_rev_1.assign(Period="Period 1"), 
#         daily_rev_2.assign(Period="Period 2")
#     ])

#     st.subheader("📄 Summary Table")
#     st.dataframe(combined)

# if st.button("Generate AI Summary"):
#     if 'daily_rev_1' in locals() and 'daily_rev_2' in locals():
#         period1_label = f"{start_date_1} to {end_date_1}"
#         period2_label = f"{start_date_2} to {end_date_2}"
#         summary = generate_analysis_summary(daily_rev_1, daily_rev_2, restaurant_name, period1_label, period2_label)
#         st.subheader("🧠 AI-Generated Revenue Summary")
#         st.markdown(summary)
#     else:
#         st.warning("Please generate the comparison charts first.")
