import requests
import argparse

def zip_to_coords(zip_code):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "postalcode": zip_code,
        "country": "us",
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "BonsaiApp/1.0 (aidenk123aiden@gmail.com)"  # Replace with your real email/app
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json()

        if not results:
            print(f"No location found for ZIP code {zip_code}")
            return None, None

        lat = float(results[0]['lat'])
        lon = float(results[0]['lon'])
        return lat, lon

    except Exception as e:
        print(f"Error fetching coordinates from Nominatim for ZIP {zip_code}: {e}")
        return None, None

def get_weather_data(lat, lon):
    headers = {
        "User-Agent": "Bonsai_Weather_Grab/1.0 (aidenk123aiden@gmail.com)"
    }

    # Step 1: Get point metadata
    point_url = f"https://api.weather.gov/points/{lat},{lon}"
    point_data = requests.get(point_url, headers=headers).json()

    # Step 2: Get list of nearby stations
    stations_url = point_data['properties']['observationStations']
    stations_data = requests.get(stations_url, headers=headers).json()
    stations = stations_data.get('features', [])

    # Step 3: Try each station until one has valid data
    for station in stations:
        station_id = station['properties']['stationIdentifier']
        obs_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"

        try:
            obs_data = requests.get(obs_url, headers=headers, timeout=10).json()
            props = obs_data['properties']

            temp = props['temperature']['value']
            humidity = props['relativeHumidity']['value']
            wind = props['windSpeed']['value']
            altitude = props['elevation']['value']

            # Check that required values are not None
            if all(v is not None for v in [temp, humidity, wind, altitude]):
                return {
                    "station_id": station_id,
                    "latitude": lat,
                    "longitude": lon,
                    "temperature_F": temp,
                    "humidity_percent": humidity,
                    "wind_speed_m_s": wind,
                    "altitude_m": altitude
                }

        except Exception as e:
            print(f"Error fetching data from station {station_id}: {e}")
            continue

    print("No station with complete weather data found.")
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zipcode', type=str, default='95618', help=
                        'Please enter a zipcode')
    args = parser.parse_args()

    lat, lon = zip_to_coords(args.zipcode)
    data = get_weather_data(lat, lon)
    print(data)

if __name__ == '__main__':
    main()