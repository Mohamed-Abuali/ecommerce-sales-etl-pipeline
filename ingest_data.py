from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("sqlite:///ecommerce.db")

def ingest_data():
    df = pd.read_csv("messy_ecommerce_sales_data.csv")
    df.to_sql("sales", engine, if_exists="replace", index=False)
    print("Data ingested successfully")

def ingest_to_db(df):
    df.to_sql("sales", engine, if_exists="replace", index=False)
    print("Data ingested successfully")
def to_csv(df):
    df.to_csv("cleaned_ecommerce_sales_data.csv", index=False)
    print("Data exported to cleaned_ecommerce_sales_data.csv successfully")