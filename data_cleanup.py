import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
from datetime import datetime

def compress_to_parquet(input_file, output_file):
    """
    Compress data to parquet format with optimized settings
    """
    # Read the input file (assuming CSV for this example)
    df = pd.read_csv(input_file)
    
    # Convert to Arrow table
    table = pa.Table.from_pandas(df)
    
    # Write to Parquet with compression
    pq.write_table(
        table,
        output_file,
        compression='snappy',  # Using snappy for good compression/speed balance
        row_group_size=100000  # Optimize row groups for better performance
    )

def cleanup_data(input_file):
    """
    Perform data cleanup operations
    """
    df = pd.read_csv(input_file)
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.fillna({
        'temp': df['temp'].mean(),
        'humidity': df['humidity'].mean(),
        'description': 'unknown'
    })
    
    # Remove outliers (example for temperature)
    temp_mean = df['temp'].mean()
    temp_std = df['temp'].std()
    df = df[abs(df['temp'] - temp_mean) <= 3 * temp_std]
    
    return df

def generate_cleanup_report(original_size, compressed_size, cleanup_stats):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data Cleanup Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Data Cleanup Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
        
        <h2>Compression Results</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Original Size (MB)</td>
                <td>{original_size:.2f}</td>
            </tr>
            <tr>
                <td>Compressed Size (MB)</td>
                <td>{compressed_size:.2f}</td>
            </tr>
            <tr>
                <td>Compression Ratio</td>
                <td>{original_size/compressed_size:.2f}x</td>
            </tr>
        </table>
        
        <h2>Cleanup Statistics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Duplicates Removed</td>
                <td>{cleanup_stats['duplicates_removed']}</td>
            </tr>
            <tr>
                <td>Missing Values Filled</td>
                <td>{cleanup_stats['missing_values_filled']}</td>
            </tr>
            <tr>
                <td>Outliers Removed</td>
                <td>{cleanup_stats['outliers_removed']}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    with open('cleanup_report.html', 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    try:
        input_file = 'weather_data.csv'
        parquet_file = 'weather_data.parquet'
        
        # Get original file size
        original_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
        
        # Perform cleanup
        df_original = pd.read_csv(input_file)
        df_cleaned = cleanup_data(input_file)
        
        # Calculate cleanup statistics
        cleanup_stats = {
            'duplicates_removed': len(df_original) - len(df_cleaned),
            'missing_values_filled': df_original.isna().sum().sum(),
            'outliers_removed': len(df_original) - len(df_cleaned)
        }
        
        # Compress to parquet
        compress_to_parquet(input_file, parquet_file)
        
        # Get compressed file size
        compressed_size = os.path.getsize(parquet_file) / (1024 * 1024)  # MB
        
        # Generate report
        generate_cleanup_report(original_size, compressed_size, cleanup_stats)
        print('Data cleanup and compression completed successfully')
        
    except Exception as e:
        print(f'Error: {e}')
        exit(1)

if __name__ == '__main__':
    main()