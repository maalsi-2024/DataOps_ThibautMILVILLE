import os
import json
from datetime import datetime
import urllib.request

CITIES = [
    {'id': '6618607', 'name': 'Paris'},
    {'id': '7284885', 'name': 'Marseille'},
    {'id': '6454573', 'name': 'Lyon'},
    {'id': '6453974', 'name': 'Toulouse'},
    {'id': '5376959', 'name': 'Nice'}
]

def fetch_weather_data():
    api_key = os.environ['WEATHER_API_KEY']
    weather_data = []

    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?id={city['id']}&appid={api_key}&units=metric"
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            weather_data.append({
                'city': city['name'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description']
            })
    
    return weather_data

def generate_html_report(weather_data):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .chart-container {{ width: 800px; height: 400px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>Weather Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
        
        <div class="chart-container">
            <canvas id="tempChart"></canvas>
        </div>
        
        <div class="chart-container">
            <canvas id="humidityChart"></canvas>
        </div>

        <script>
            const weatherData = {json.dumps(weather_data)};
            
            new Chart(document.getElementById('tempChart'), {{
                type: 'bar',
                data: {{
                    labels: weatherData.map(d => d.city),
                    datasets: [{{
                        label: 'Temperature (°C)',
                        data: weatherData.map(d => d.temp),
                        backgroundColor: 'rgba(255, 99, 132, 0.5)'
                    }}]
                }}
            }});

            new Chart(document.getElementById('humidityChart'), {{
                type: 'bar',
                data: {{
                    labels: weatherData.map(d => d.city),
                    datasets: [{{
                        label: 'Humidity (%)',
                        data: weatherData.map(d => d.humidity),
                        backgroundColor: 'rgba(54, 162, 235, 0.5)'
                    }}]
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    with open('weather-report.html', 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    try:
        weather_data = fetch_weather_data()
        generate_html_report(weather_data)
        print('Weather report generated successfully')
    except Exception as e:
        print(f'Error: {e}')
        exit(1)

if __name__ == '__main__':
    main()