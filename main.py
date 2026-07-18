from clean_data import read_data, fix_price_formula, clean_quantity, fix_data_types, total_missing_data, fix_category_missing
from ingest_data import ingest_data



ingest_data()
df = read_data()


df = fix_data_types(df)
# clean_quantity(df)
# total_missing_data(df)
df = fix_category_missing(df)
df = fix_price_formula(df)

print(df)


