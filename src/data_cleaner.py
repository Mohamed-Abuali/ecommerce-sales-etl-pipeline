import pandas as pd
import numpy as np
import re
from typing import Dict, List, Optional
from config.settings import PRODUCT_CATEGORIES, CLEANING_RULES

class DataCleaner:
    """Handle data cleaning operations for the ecommerce pipeline."""
    
    def __init__(self):
        self.product_categories = PRODUCT_CATEGORIES
        self.cleaning_rules = CLEANING_RULES
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names."""
        df.columns = df.columns.str.strip()
        return df
    
    def fix_price_column(self, df: pd.DataFrame, column_name: str = "Price") -> pd.DataFrame:
        """Clean price column by removing letters and currency symbols."""
        if column_name in df.columns:
            # Remove letters first
            df[column_name] = df[column_name].str.replace(
                self.cleaning_rules["price_patterns"]["remove_letters"], 
                self.cleaning_rules["price_patterns"]["replace_with"], 
                regex=True
            )
            # Remove currency symbols
            df[column_name] = df[column_name].str.replace(
                self.cleaning_rules["price_patterns"]["remove_currency"], 
                ""
            )
            # Convert to numeric
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
        return df
    
    def clean_quantity_column(self, df: pd.DataFrame, column_name: str = "Quantity") -> pd.DataFrame:
        """Clean quantity column by converting to numeric."""
        if column_name in df.columns:
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
        return df
    
    def fix_missing_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fix missing categories based on product names."""
        if "Product" in df.columns and "Category" in df.columns:
            for category, products in self.product_categories.items():
                mask = df["Product"].isin(products) & (df["Category"].isna() | df["Category"].str.strip().eq(""))
                df.loc[mask, "Category"] = category
        return df
    
    def fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fix data types for common columns."""
        # Convert date columns if they exist
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = [col for col in df.columns if any(word in col.lower() for word in ['price', 'quantity', 'amount', 'total'])]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """Handle missing values in the dataframe."""
        if strategy == "drop":
            # Drop rows with missing values in critical columns
            critical_columns = ["Product", "Price", "Quantity"]
            existing_critical = [col for col in critical_columns if col in df.columns]
            if existing_critical:
                df = df.dropna(subset=existing_critical)
        elif strategy == "fill":
            # Fill missing values with appropriate defaults
            for column in df.columns:
                if df[column].dtype in ['int64', 'float64']:
                    df[column] = df[column].fillna(0)
                elif df[column].dtype == 'object':
                    df[column] = df[column].fillna("Unknown")
        
        return df
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows."""
        initial_count = len(df)
        df = df.drop_duplicates()
        removed_count = initial_count - len(df)
        if removed_count > 0:
            print(f"Removed {removed_count} duplicate rows")
        return df
    
    def get_cleaning_report(self, df: pd.DataFrame) -> Dict:
        """Generate a report of data quality issues."""
        report = {
            "total_rows": len(df),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": len(df) - len(df.drop_duplicates()),
            "data_types": df.dtypes.to_dict()
        }
        
        # Add column-specific statistics
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            report[f"{col}_statistics"] = {
                "min": df[col].min(),
                "max": df[col].max(),
                "mean": df[col].mean(),
                "median": df[col].median()
            }
        
        return report