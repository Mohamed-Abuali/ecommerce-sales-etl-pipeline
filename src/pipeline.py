from typing import Optional, Dict
import pandas as pd
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from config.settings import CLEAN_DATA_PATH

class DataPipeline:
    """Main data processing pipeline for ecommerce data."""
    
    def __init__(self):
        self.loader = DataLoader()
        self.cleaner = DataCleaner()
        self.processing_report = {}
    
    def run_full_pipeline(self, input_source: str = "database") -> pd.DataFrame:
        """
        Run the complete data processing pipeline.
        
        Args:
            input_source: "database" or "csv" to specify data source
            
        Returns:
            Cleaned pandas DataFrame
        """
        print("Starting data processing pipeline...")
        
        # Step 1: Load data
        if input_source == "database":
            df = self.loader.load_from_database()
        else:
            df = self.loader.load_raw_data()
        
        print(f"Loaded {len(df)} rows of raw data")
        
        # Step 2: Generate initial report
        self.processing_report["initial"] = self.cleaner.get_cleaning_report(df)
        
        # Step 3: Clean column names
        df = self.cleaner.clean_column_names(df)
        
        # Step 4: Fix data types
        df = self.cleaner.fix_data_types(df)
        
        # Step 5: Clean specific columns
        df = self.cleaner.fix_price_column(df)
        df = self.cleaner.clean_quantity_column(df)
        
        # Step 6: Fix missing categories
        df = self.cleaner.fix_missing_categories(df)
        
        # Step 7: Handle missing values
        df = self.cleaner.handle_missing_values(df, strategy="drop")
        
        # Step 8: Remove duplicates
        df = self.cleaner.remove_duplicates(df)
        
        # Step 9: Generate final report
        self.processing_report["final"] = self.cleaner.get_cleaning_report(df)
        
        print(f"Pipeline completed. Final dataset: {len(df)} rows")
        return df
    
    def save_cleaned_data(self, df: pd.DataFrame, output_format: str = "both") -> None:
        """
        Save cleaned data to specified formats.
        
        Args:
            df: Cleaned DataFrame
            output_format: "csv", "database", or "both"
        """
        if output_format in ["csv", "both"]:
            self.loader.save_to_csv(df, str(CLEAN_DATA_PATH))
        
        if output_format in ["database", "both"]:
            self.loader.save_to_database(df)
    
    def get_processing_report(self) -> Dict:
        """Get the processing report with before/after statistics."""
        return self.processing_report
    
    def print_processing_summary(self) -> None:
        """Print a summary of the data processing."""
        if not self.processing_report:
            print("No processing report available. Run the pipeline first.")
            return
        
        initial = self.processing_report["initial"]
        final = self.processing_report["final"]
        
        print("\n" + "="*50)
        print("DATA PROCESSING SUMMARY")
        print("="*50)
        print(f"Initial rows: {initial['total_rows']}")
        print(f"Final rows: {final['total_rows']}")
        print(f"Rows removed: {initial['total_rows'] - final['total_rows']}")
        print(f"Duplicate rows removed: {initial['duplicate_rows']}")
        print("\nMissing values by column:")
        for col, count in final['missing_values'].items():
            if count > 0:
                print(f"  {col}: {count}")
        print("="*50)