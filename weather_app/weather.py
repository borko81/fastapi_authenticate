import requests
from datetime import datetime
from decouple import config

class Weather:
    def __init__(self, name_pos_token: str, weather_token: str) -> None:
        self.name_pos_token = name_pos_token
        self.weather_token = weather_token


    def convert_name_to_positions(self, town_name: str):
        URL_NAME_TO_LAT=f"https://api.api-ninjas.com/v1/geocoding?city={town_name}&country=Bulgaria"
        response = requests.get(URL_NAME_TO_LAT, headers={'X-Api-Key': f'{self.name_pos_token}'})
        if response.status_code == 200:
            result = response.json()[0]
            return result['latitude'], result['longitude']
        else:
            raise ValueError("An error acquire when try to convert name to position.")
        


    def weather_parse(self, town_name):
        lat, lon = self.convert_name_to_positions(town_name)
        api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.weather_token}&lang=bg&units=metric'
        
        response = requests.get(api_url)
        if response.status_code == 200:
            status = response.json()
            result = {}
            result['temp_min'] = status['main']['temp_min']
            result['temp_max'] = status['main']['temp_max']
            result['sunrise'] = datetime.fromtimestamp(status['sys']['sunrise']).time().strftime("%H:%M")
            result['sunset'] = datetime.fromtimestamp(status['sys']['sunset']).time().strftime("%H:%M")
            return result


if __name__ == '__main__':
    check = Weather(config('name_pos_token'), config('WEATHER_TOKEN'))
    check.weather_parse('velingrad')

