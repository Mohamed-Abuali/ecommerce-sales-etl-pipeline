import pandas as pd
import numpy as np
from ingest_data import engine
from sqlalchemy import text

def read_data():
    
    df = pd.read_sql("SELECT * FROM sales", engine)
    df.rename(columns={" Category": "Category"}, inplace=True)
    df.to_sql("sales", engine, if_exists="replace", index=False)
    print(df[df["Category"].isnull()])
    return df



def fix_price_formula(data):
    data["Price"] = data["Price"].str.replace(r'[a-zA-Z]+', "Null",regex=True)
    data["Price"] = data["Price"].str.replace("$", "")
    print(data["Price"].head())
    return
def  clean_quantity(data):
    return    
def total_missing_data(data):
    return
def fix_product_missing(data):
    return
def fix_category_missing(data):
    df = pd.read_sql("SELECT * FROM sales", engine)
    #filter the category
    cat= pd.Series(df["Category"].unique())
    exclude_list = ['electronic',
    'ELECTRONICS',
    'electronics',
    'sports']
    filtered_cat = cat[~cat.isin(exclude_list)].dropna()
    #assign the missing category
    with engine.connect() as conn:
        conn.execute(text("""
        UPDATE sales
        SET Category = CASE
            WHEN product  IN ("Smartphone", "Laptop", "Tablet", "Camera","Smartwatch","Headphones") THEN "Electronics"
            WHEN product  IN ("Vacuum","Blender","Lamp") THEN "Home"
            ELSE Category
        END;
        """))
        conn.commit()
    df = pd.read_sql("SELECT * FROM sales", engine)
    print(cat)
    return df

def fix_date_formula(data):
    return


