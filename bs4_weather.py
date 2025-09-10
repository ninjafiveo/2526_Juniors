#!/usr/bin/env python3
"""
Weather Underground Web Scraper - Updated Version
Scrapes 7-day weather forecast from Weather Underground
"""

import requests
from bs4 import BeautifulSoup
import sys
import re
from urllib.parse import quote
import json

class WeatherScraper:
    def __init__(self):
        self.base_url = "https://www.wunderground.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def get_location_url(self, location):
        """Convert location input to Weather Underground URL format"""
        location = location.strip()
        
        # Check if it's a ZIP code (5 digits)
        if re.match(r'^\d{5}$', location):
            return f"/weather/us/zipcode/{location}"
        
        # Otherwise, assume it's city, state format
        location_parts = location.replace(',', '').split()
        if len(location_parts) >= 2:
            # Take last part as state, everything else as city
            state = location_parts[-1].lower()
            city = '-'.join(location_parts[:-1]).lower()
            return f"/weather/us/{state}/{city}"
        else:
            # Single word location
            location_encoded = quote(location.replace(' ', '-').lower())
            return f"/weather/{location_encoded}"
    
    def scrape_forecast(self, location):
        """Scrape the 7-day forecast from Weather Underground"""
        try:
            location_path = self.get_location_url(location)
            url = self.base_url + location_path
            
            print(f"Fetching weather data from: {url}")
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract location name
            location_name = self.extract_location_name(soup)
            
            # Try multiple methods to extract forecast data
            forecast_data = self.extract_forecast_data_v2(soup)
            
            if not forecast_data:
                forecast_data = self.extract_forecast_data_fallback(soup)
            
            return location_name, forecast_data
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None, None
        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return None, None
    
    def extract_location_name(self, soup):
        """Extract the location name from the page"""
        # Try multiple selectors for location name
        selectors = [
            'h1[data-testid="CurrentConditionsHeader"]',
            'h1.CurrentConditions--location--1Ayv3',
            '[data-testid="CurrentConditionsHeader"]',
            'h1',
            '.location-name',
            '.current-conditions-header h1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text and text not in ['undefined', '']:
                    return text
        
        return "Location"
    
    def extract_forecast_data_v2(self, soup):
        """Updated method to extract forecast data from current Weather Underground layout"""
        forecasts = []
        
        # Look for JSON data in script tags (common in modern websites)
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'forecast' in script.string.lower():
                try:
                    # Try to extract JSON data
                    script_content = script.string
                    if 'dailyForecast' in script_content or 'forecast' in script_content:
                        forecast_data = self.parse_json_forecast(script_content)
                        if forecast_data:
                            return forecast_data
                except:
                    continue
        
        # Look for modern forecast cards
        forecast_containers = soup.find_all(['div', 'li'], attrs={
            'data-testid': re.compile(r'(DailyWeatherCard|ForecastCard)', re.I),
            'class': re.compile(r'(daily|forecast|day)', re.I)
        })
        
        if not forecast_containers:
            # Alternative selectors
            forecast_containers = soup.select('[data-testid*="Daily"], [class*="daily"], [class*="forecast"]')
        
        if not forecast_containers:
            # Look for any containers with temperature patterns
            temp_elements = soup.find_all(string=re.compile(r'\d+°'))
            day_elements = soup.find_all(string=re.compile(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Today)', re.I))
            
            if temp_elements and day_elements:
                return self.build_forecast_from_elements(day_elements, temp_elements, soup)
        
        # Process forecast containers
        for container in forecast_containers[:7]:
            forecast = self.parse_forecast_container_v2(container)
            if forecast:
                forecasts.append(forecast)
        
        return forecasts
    
    def parse_json_forecast(self, script_content):
        """Try to extract forecast data from JSON in script tags"""
        forecasts = []
        try:
            # Look for common JSON patterns
            json_patterns = [
                r'"dailyForecast":\s*(\[.*?\])',
                r'"forecast":\s*(\{.*?\})',
                r'"daily":\s*(\[.*?\])'
            ]
            
            for pattern in json_patterns:
                match = re.search(pattern, script_content, re.DOTALL)
                if match:
                    try:
                        data = json.loads(match.group(1))
                        if isinstance(data, list):
                            for item in data[:7]:
                                forecast = self.extract_from_json_item(item)
                                if forecast:
                                    forecasts.append(forecast)
                            if forecasts:
                                return forecasts
                    except:
                        continue
        except:
            pass
        
        return forecasts
    
    def extract_from_json_item(self, item):
        """Extract forecast info from JSON item"""
        try:
            forecast = {}
            
            # Extract day
            if 'dayOfWeek' in item:
                forecast['day'] = item['dayOfWeek']
            elif 'day' in item:
                forecast['day'] = item['day']
            
            # Extract temperatures
            high_temp = None
            low_temp = None
            
            if 'temperature' in item:
                temp_data = item['temperature']
                if isinstance(temp_data, dict):
                    high_temp = temp_data.get('high', temp_data.get('max'))
                    low_temp = temp_data.get('low', temp_data.get('min'))
            
            if 'high' in item:
                high_temp = item['high']
            if 'low' in item:
                low_temp = item['low']
            
            if high_temp and low_temp:
                forecast['temperature'] = f"{high_temp}° / {low_temp}°"
            elif high_temp:
                forecast['temperature'] = f"{high_temp}°"
            
            # Extract condition
            if 'condition' in item:
                forecast['condition'] = item['condition']
            elif 'weather' in item:
                forecast['condition'] = item['weather']
            elif 'description' in item:
                forecast['condition'] = item['description']
            
            return forecast if 'day' in forecast else None
            
        except:
            return None
    
    def parse_forecast_container_v2(self, container):
        """Enhanced parsing for forecast containers"""
        forecast = {}
        
        # Extract day
        day_patterns = [
            r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Today|Tonight|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b'
        ]
        
        for pattern in day_patterns:
            day_match = container.find(string=re.compile(pattern, re.I))
            if day_match:
                forecast['day'] = day_match.strip()
                break
        
        # Extract temperatures - look for high/low patterns
        temp_elements = container.find_all(string=re.compile(r'\d+°'))
        temps = [temp.strip() for temp in temp_elements if temp.strip()]
        
        if len(temps) >= 2:
            # Assume first is high, second is low
            forecast['temperature'] = f"{temps[0]} / {temps[1]}"
        elif len(temps) == 1:
            forecast['temperature'] = temps[0]
        
        # If no temps found, look in nearby elements
        if 'temperature' not in forecast:
            parent = container.parent
            if parent:
                nearby_temps = parent.find_all(string=re.compile(r'\d+°'))
                nearby_temps = [temp.strip() for temp in nearby_temps if temp.strip()][:2]
                if nearby_temps:
                    forecast['temperature'] = ' / '.join(nearby_temps)
        
        # Extract condition
        condition_keywords = [
            'sunny', 'cloudy', 'rain', 'snow', 'storm', 'clear', 'partly', 'mostly', 
            'thunderstorm', 'showers', 'overcast', 'fog', 'windy', 'fair'
        ]
        condition_pattern = '|'.join(condition_keywords)
        
        condition_elem = container.find(string=re.compile(condition_pattern, re.I))
        if condition_elem:
            forecast['condition'] = condition_elem.strip()
        else:
            # Look for common weather icons or alt text
            img_elements = container.find_all('img')
            for img in img_elements:
                alt_text = img.get('alt', '')
                title_text = img.get('title', '')
                if alt_text and any(keyword in alt_text.lower() for keyword in condition_keywords):
                    forecast['condition'] = alt_text
                    break
                elif title_text and any(keyword in title_text.lower() for keyword in condition_keywords):
                    forecast['condition'] = title_text
                    break
        
        return forecast if 'day' in forecast else None
    
    def build_forecast_from_elements(self, day_elements, temp_elements, soup):
        """Build forecast from separate day and temperature elements"""
        forecasts = []
        
        # Clean and organize elements
        days = []
        temps = []
        
        for day_elem in day_elements[:7]:
            day_text = day_elem.strip()
            if day_text and len(day_text) <= 10:  # Reasonable day name length
                days.append(day_text)
        
        for temp_elem in temp_elements:
            temp_text = temp_elem.strip()
            if re.match(r'\d+°', temp_text):
                temps.append(temp_text)
        
        # Pair days with temperatures
        for i, day in enumerate(days):
            forecast = {'day': day}
            
            # Try to find corresponding temperatures
            if i * 2 + 1 < len(temps):
                # Assume pairs of high/low
                high_temp = temps[i * 2]
                low_temp = temps[i * 2 + 1]
                forecast['temperature'] = f"{high_temp} / {low_temp}"
            elif i < len(temps):
                # Single temperature
                forecast['temperature'] = temps[i]
            else:
                forecast['temperature'] = 'N/A'
            
            forecast['condition'] = 'Check website for details'
            forecasts.append(forecast)
        
        return forecasts
    
    def extract_forecast_data_fallback(self, soup):
        """Fallback method using broader search"""
        forecasts = []
        
        # Get all text content and search for patterns
        page_text = soup.get_text()
        
        # Find day patterns
        day_pattern = r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Today|Tonight|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b'
        days = re.findall(day_pattern, page_text, re.I)
        
        # Find temperature patterns
        temp_pattern = r'\b\d+°[CF]?\b'
        temperatures = re.findall(temp_pattern, page_text)
        
        if days and temperatures:
            # Create forecast entries
            unique_days = []
            seen_days = set()
            
            for day in days:
                if day.lower() not in seen_days and len(unique_days) < 7:
                    unique_days.append(day)
                    seen_days.add(day.lower())
            
            for i, day in enumerate(unique_days):
                forecast = {
                    'day': day,
                    'temperature': 'N/A',
                    'condition': 'Check website for details'
                }
                
                # Try to match temperatures
                temp_start_idx = i * 2
                if temp_start_idx + 1 < len(temperatures):
                    high_temp = temperatures[temp_start_idx]
                    low_temp = temperatures[temp_start_idx + 1]
                    forecast['temperature'] = f"{high_temp} / {low_temp}"
                elif temp_start_idx < len(temperatures):
                    forecast['temperature'] = temperatures[temp_start_idx]
                
                forecasts.append(forecast)
        
        return forecasts
    
    def display_forecast(self, location_name, forecast_data):
        """Display the forecast in a formatted way"""
        if not forecast_data:
            print("No forecast data available.")
            return
        
        print("\n" + "="*60)
        print(f"7-Day Weather Forecast for {location_name}")
        print("="*60)
        
        for i, day_forecast in enumerate(forecast_data, 1):
            day = day_forecast.get('day', 'N/A')
            temp = day_forecast.get('temperature', 'N/A')
            condition = day_forecast.get('condition', 'N/A')
            
            print(f"\nDay {i}: {day}")
            print(f"Temperature: {temp}")
            print(f"Conditions: {condition}")
            print("-" * 40)

def main():
    print("Weather Underground Forecast Scraper")
    print("=====================================")
    
    scraper = WeatherScraper()
    
    while True:
        try:
            location = input("\nEnter ZIP code or City, State (or 'quit' to exit): ").strip()
            
            if location.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not location:
                print("Please enter a valid location.")
                continue
            
            print("\nFetching weather data...")
            location_name, forecast_data = scraper.scrape_forecast(location)
            
            if location_name and forecast_data:
                scraper.display_forecast(location_name, forecast_data)
            else:
                print("Sorry, couldn't retrieve weather data for that location.")
                print("Please check your input and try again.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()