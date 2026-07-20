import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_cleaner import DataCleaner
from config.settings import PRODUCT_CATEGORIES

class TestDataCleaner(unittest.TestCase):
    """Test cases for the DataCleaner class."""
    
    def setUp(self):
        """Set up test data."""
        self.cleaner = DataCleaner()
        
        # Create test dataframe
        self.test_df = pd.DataFrame({
            'Product': ['Smartphone', 'Blender', 'Unknown Product', 'Tennis Racket'],
            'Category': ['Electronics', 'Home', None, ''],
            'Price': ['$299.99', 'ABC123', '99.99', '$150'],
            'Quantity': ['5', '10', 'invalid', '3']
        })
    
    def test_clean_column_names(self):
        """Test column name cleaning."""
        df = pd.DataFrame({'  Product  ': [1, 2], '  Price  ': [10, 20]})
        cleaned = self.cleaner.clean_column_names(df)
        
        expected_columns = ['Product', 'Price']
        self.assertEqual(list(cleaned.columns), expected_columns)
    
    def test_fix_price_column(self):
        """Test price column cleaning."""
        cleaned = self.cleaner.fix_price_column(self.test_df.copy())
        
        # Check that prices are converted to numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned['Price']))
        # Check that invalid values are converted to NaN
        self.assertTrue(pd.isna(cleaned.loc[1, 'Price']))  # ABC123 should be NaN
    
    def test_clean_quantity_column(self):
        """Test quantity column cleaning."""
        cleaned = self.cleaner.clean_quantity_column(self.test_df.copy())
        
        # Check that quantities are converted to numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned['Quantity']))
        # Check that invalid values are converted to NaN
        self.assertTrue(pd.isna(cleaned.loc[2, 'Quantity']))  # 'invalid' should be NaN
    
    def test_fix_missing_categories(self):
        """Test category assignment based on product names."""
        cleaned = self.cleaner.fix_missing_categories(self.test_df.copy())
        
        # Check that Smartphone gets Electronics category
        smartphone_row = cleaned[cleaned['Product'] == 'Smartphone']
        self.assertEqual(smartphone_row['Category'].iloc[0], 'Electronics')
        
        # Check that Blender gets Home category
        blender_row = cleaned[cleaned['Product'] == 'Blender']
        self.assertEqual(blender_row['Category'].iloc[0], 'Home')
    
    def test_handle_missing_values_drop(self):
        """Test missing value handling with drop strategy."""
        df_with_missing = self.test_df.copy()
        df_with_missing.loc[0, 'Product'] = None
        
        cleaned = self.cleaner.handle_missing_values(df_with_missing, strategy="drop")
        
        # Check that row with missing Product is dropped
        self.assertEqual(len(cleaned), len(df_with_missing) - 1)
        self.assertNotIn(None, cleaned['Product'].values)
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        df_with_duplicates = pd.concat([self.test_df, self.test_df], ignore_index=True)
        
        cleaned = self.cleaner.remove_duplicates(df_with_duplicates)
        
        # Check that duplicates are removed
        self.assertEqual(len(cleaned), len(self.test_df))
    
    def test_get_cleaning_report(self):
        """Test cleaning report generation."""
        report = self.cleaner.get_cleaning_report(self.test_df)
        
        self.assertIn('total_rows', report)
        self.assertIn('missing_values', report)
        self.assertIn('duplicate_rows', report)
        self.assertIn('data_types', report)
        
        self.assertEqual(report['total_rows'], len(self.test_df))

if __name__ == '__main__':
    unittest.main()