import pandas as pd
from sqlalchemy import create_engine, text
from config.settings import DATABASE_URL, RAW_DATA_PATH

class DataLoader:
    """Handle data loading operations for the ecommerce pipeline."""
    
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
    
    def load_raw_data(self) -> pd.DataFrame:
        """Load raw data from CSV file."""
        try:
            df = pd.read_csv(RAW_DATA_PATH)
            print(f"Successfully loaded {len(df)} rows from {RAW_DATA_PATH}")
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Raw data file not found: {RAW_DATA_PATH}")
    
    def load_from_database(self, table_name: str = "sales") -> pd.DataFrame:
        """Load data from database."""
        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", self.engine)
            print(f"Successfully loaded {len(df)} rows from {table_name} table")
            return df
        except Exception as e:
            raise Exception(f"Error loading from database: {e}")
    
    def save_to_database(self, df: pd.DataFrame, table_name: str = "sales", if_exists: str = "replace") -> None:
        """Save dataframe to database."""
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            print(f"Successfully saved {len(df)} rows to {table_name} table")
        except Exception as e:
            raise Exception(f"Error saving to database: {e}")
    
    def save_to_csv(self, df: pd.DataFrame, file_path: str) -> None:
        """Save dataframe to CSV file."""
        try:
            df.to_csv(file_path, index=False)
            print(f"Successfully saved data to {file_path}")
        except Exception as e:
            raise Exception(f"Error saving to CSV: {e}")
    
    def get_table_info(self, table_name: str = "sales") -> dict:
        """Get basic information about a database table."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) as count FROM {table_name}"))
                count = result.scalar()
                
                columns = pd.read_sql(f"PRAGMA table_info({table_name})", self.engine)
                
                return {
                    "row_count": count,
                    "columns": columns["name"].tolist(),
                    "column_count": len(columns)
                }
        except Exception as e:
            raise Exception(f"Error getting table info: {e}")