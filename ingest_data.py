from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("sqlite:///ecommerce.db")

def ingest_data():
    df = pd.read_csv("messy_ecommerce_sales_data.csv")
    df.to_sql("sales", engine, if_exists="replace", index=False)
    print("Data ingested successfully")
    
