#!/usr/bin/env python3
"""
Ecommerce Data Processing Pipeline

This script runs the complete data processing pipeline for ecommerce sales data.
It loads raw data, cleans it, and saves the cleaned results.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent))

from src.pipeline import DataPipeline
from src.data_loader import DataLoader

def main():
    """Run the complete data processing pipeline."""
    try:
        print("Ecommerce Data Processing Pipeline")
        print("=" * 50)
        
        # Initialize the pipeline
        pipeline = DataPipeline()
        
        # Run the full cleaning pipeline
        cleaned_df = pipeline.run_full_pipeline(input_source="csv")
        
        # Save the cleaned data
        pipeline.save_cleaned_data(cleaned_df, output_format="both")
        
        # Print processing summary
        pipeline.print_processing_summary()
        
        print("\nPipeline completed successfully!")
        
    except Exception as e:
        print(f"Error running pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()