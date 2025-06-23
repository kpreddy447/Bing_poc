from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import base64
from db_connector import load_data_from_postgres
import pandas as pd
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# def compare_images(img1_path, img2_path):
#     img1_b64 = image_to_base64(img1_path)
#     img2_b64 = image_to_base64(img2_path)

#     response = client.chat.completions.create(
#         model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  
#         messages=[
#             {"role": "system", "content": "In 3-5 bullter points Summarize differences the two graphs at same day of the week.Any assumptions as to why it might happened"},
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": (
#                             "These two line charts show data for two different weeks (Monday to Sunday). "
#                             "Extract numeric values for each day (Mon–Sun) from both charts. Then, compare "
#                             "the same weekday (e.g., Monday vs Monday), and only list days where the difference "
#                             "between Week 1 and Week 2 is large (e.g., >300 units).\n\n"
#                             "Return the result as a markdown table with columns:\n\n"
#                             "| Day | Week 1 Value | Week 2 Value | Difference | Comment |"
#                         )},
#                     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img1_b64}"}},
#                     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img2_b64}"}}
#                 ]
#             }
#         ],
#         max_tokens=500
#     )

#     return response.choices[0].message.content

def compare_images(img1_path, img2_path, restaurant_name=None, start_date_1=None, end_date_1=None, start_date_2=None, end_date_2=None):
    img1_b64 = image_to_base64(img1_path)
    img2_b64 = image_to_base64(img2_path)

    # Adjusted columns based on your actual schema
    if all([restaurant_name, start_date_1, end_date_1, start_date_2, end_date_2]):
        query = """
        SELECT date_of_visit, visited_customer_name, total_bill_amount, time_of_visit
        FROM public.main_table
        WHERE restaurant_name = %s
          AND (
              (date_of_visit BETWEEN %s AND %s) OR
              (date_of_visit BETWEEN %s AND %s)
          )
        """
        df = load_data_from_postgres(query, params=(restaurant_name, start_date_1, end_date_1, start_date_2, end_date_2))

        df["date_of_visit"] = df["date_of_visit"].astype(str)
        df["total_bill_amount"] = pd.to_numeric(df["total_bill_amount"], errors='coerce')
        sample_data = df.head(100).to_csv(index=False)
    else:
        sample_data = "No tabular data available."

    prompt = f"""
You are a restaurant data analyst comparing customer and revenue patterns between two time periods.

### Visual Input:
- Two line charts showing total bill amounts per day for different weeks.

### Tabular Input:
Raw transaction data including:
- Customer name
- Total bill amount
- Date and time of visit

### Your Task:
1. Identify any days of the week with large revenue differences (> $300) between charts.
2. Analyze the tabular data to suggest **possible reasons**, such as:
   - More customers on high-revenue days
   - Presence of very high-value bills
   - Fewer or no visits on low-revenue days
   - Time-of-day clustering (e.g., lunch rush vs dinner)
   - Any anomalies you detect

### Output:
- Markdown table:

| Day | Week 1 Value | Week 2 Value | Difference | Observation |

- 3–5 bullet points explaining what might have caused the differences.
- Don’t make up facts—stick to the data provided.

"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a data expert specializing in visual and transactional analysis of restaurant data."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img1_b64}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img2_b64}"}}
                ]
            }
        ],
        max_tokens=1200
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    result = compare_images("graph1.png", "graph2.png")
    print(result)

