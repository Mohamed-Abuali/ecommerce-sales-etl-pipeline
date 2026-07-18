from clean_data import read_data, fix_price_formula, clean_quantity, fix_data_types, total_missing_data, fix_category_missing
from ingest_data import ingest_data, ingest_to_db, to_csv



ingest_data()
df = read_data()


df = fix_data_types(df)
df = clean_quantity(df)

df = fix_category_missing(df)
df = fix_price_formula(df)
df =total_missing_data(df)

print(df.isnull().sum())
ingest_to_db(df)

to_csv(df)
