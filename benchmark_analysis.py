import pandas as pd
import numpy as np
import time
import psutil
import json
from datetime import datetime

def measure_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        return {
            'result': result,
            'execution_time': execution_time,
            'memory_used': memory_used
        }
    return wrapper

@measure_performance
def transform_weather_data(data):
    df = pd.DataFrame(data)
    # Perform some transformations
    df['temp_fahrenheit'] = df['temp'] * 9/5 + 32
    df['temp_category'] = pd.cut(df['temp'], 
                                bins=[-float('inf'), 0, 15, 25, float('inf')],
                                labels=['Cold', 'Cool', 'Mild', 'Hot'])
    return df

def generate_benchmark_report(benchmark_results):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Benchmark Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Benchmark Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
        
        <h2>Performance Metrics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Execution Time (seconds)</td>
                <td>{benchmark_results['execution_time']:.4f}</td>
            </tr>
            <tr>
                <td>Memory Usage (MB)</td>
                <td>{benchmark_results['memory_used']:.2f}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    with open('benchmark_results.html', 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    try:
        # Load sample weather data
        with open('sample_weather_data.json', 'r') as f:
            weather_data = json.load(f)
        
        # Run benchmarks
        benchmark_results = transform_weather_data(weather_data)
        
        # Generate report
        generate_benchmark_report(benchmark_results)
        print('Benchmark report generated successfully')
        
    except Exception as e:
        print(f'Error: {e}')
        exit(1)

if __name__ == '__main__':
    main()