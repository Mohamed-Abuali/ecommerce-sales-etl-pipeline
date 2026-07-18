import pandas as pd
import numpy as np
from ingest_data import engine
from sqlalchemy import text

def read_data():
    
    df = pd.read_sql("SELECT * FROM sales", engine)
    df.rename(columns={" Category": "Category"}, inplace=True)
    df.to_sql("sales", engine, if_exists="replace", index=False)
    #print(df[df["Category"].isnull()])
    return df



def fix_price_formula(data):
    data["Price"] = data["Price"].str.replace(r'[a-zA-Z]+', "0",regex=True)
    data["Price"] = data["Price"].str.replace("$", "")
    data["Price"] = pd.to_numeric(data["Price"], errors="coerce")
    data["Price"] = data["Price"].fillna(0)
    return data
def  clean_quantity(data):
    
    return data
def total_missing_data(data):
    data["Total"] = (data["Quantity"] * data["Price"]).fillna(0)
    return data
def fix_data_types(data):
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["Quantity"] = data["Quantity"].fillna(0)
    data["Quantity"] = data["Quantity"].astype(int)
    return data



def fix_category_missing(data):
    df = data
    #filter the category
    cat= pd.Series(df["Category"].unique())
    exclude_list = ['electronic',
    'ELECTRONICS',
    'electronics',
    'sports']
    filtered_cat = cat[~cat.isin(exclude_list)].dropna()
    #filter the product
    product  = pd.Series(df["Product"].unique())

    #print(filtered_cat)
    #assign the missing category
    for category, products in product_categories.items():
        df.loc[df['Product'].isin(products), 'Category'] = category

    df.to_sql("sales", engine, if_exists="replace", index=False)
    #print(pd.read_sql("SELECT * FROM sales", engine))
    return df

def fix_date_formula(data):
    return


product_categories = {
    "Home": ["Blender", "Microwave", "Vacuum", "Lamp"],
    "Electronics": ["Smartphone", "Smartwatch", "Headphones", "Laptop"],
    "Sports": ["Tennis Racket", "Basketball", "Yoga Mat", "Football"],
    "Books": ["Science", "Biography", "Comics", "Fiction"],
    "Clothing": ["Shoes", "T-shirt", "Jacket", "shoes", "Jeans"]
}