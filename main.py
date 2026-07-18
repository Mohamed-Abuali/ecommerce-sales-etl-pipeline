from clean_data import read_data, fix_price_formula, clean_quantity, total_missing_data, fix_product_missing, fix_category_missing
from ingest_data import ingest_data



ingest_data()
df = read_data()

# fix_price_formula(df)
# clean_quantity(df)
# total_missing_data(df)
fix_category_missing(df)



