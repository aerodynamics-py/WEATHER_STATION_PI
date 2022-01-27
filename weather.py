# -*- coding:utf-8 -*-

import time
import requests
import locale

locale.setlocale(locale.LC_TIME, '')


# lat = "48.8511048"
# lon = "2.3915906"
# api_key = "696a01e644791c546061076bc92e4cb4"

class Weather:
    def __init__(self, latitude, longitude, api_id):
        self.latitude = latitude
        self.longitude = longitude
        self.api_key = api_id
        self.prevision = [0, [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]]
        self.data = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={self.latitude}&lon={self.longitude}&lang=fr&appid={self.api_key}").json()
        self.prevision[0] = self.data["daily"][0]["dt"]
        self.prevision[1][6] = [self.data["daily"][0]["pressure"],
                                round(self.data["daily"][0]["temp"]["day"] - 273.15, 0)]
        pass

    def update(self):
        self.data = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={self.latitude}&lon={self.longitude}&lang=fr&appid={self.api_key}").json()
        return self.data

    def current_time(self):
        return time.strftime("%d/%m/%Y %H:%M", time.localtime(self.data["current"]["dt"]))

    def current_temp(self):
        return "{:.0f}".format(self.data["current"]["temp"] - 273.15) + "°C"

    def current_hum(self):
        return "{:.0f}".format(self.data["current"]["humidity"]) + "%"

    def current_cloud_cov(self):
        return "{:.0f}".format(self.data["current"]["clouds"]) + "%"

    def current_sunrise(self):
        return time.strftime("%H:%M", time.localtime(self.data["current"]["sunrise"]))

    def current_sunset(self):
        return time.strftime("%H:%M", time.localtime(self.data["current"]["sunset"]))

    def current_wind(self):
        deg = self.data["current"]["wind_deg"]
        if deg < 30 or deg >= 330:
            direction = "N"
        elif 30 <= deg < 60:
            direction = "NE"
        elif 60 <= deg < 120:
            direction = "E"
        elif 120 <= deg < 150:
            direction = "SE"
        elif 150 <= deg < 210:
            direction = "S"
        elif 210 <= deg < 240:
            direction = "SO"
        elif 240 <= deg < 300:
            direction = "O"
        elif 300 <= deg < 330:
            direction = "NO"
        else:
            direction = "N/A"
        return "{:.0f}".format(self.data["current"]["wind_speed"] * 3.6) + "km/h", direction

    def current_weather(self):
        description = self.data["current"]["weather"][0]["id"]
        return description

    def rain_next_hour(self):
        input_minutely = self.data["minutely"]
        rain = []
        rain_next_hour = [["+10'", 0], ["+20'", 0], ["+30'", 0], ["+40'", 0], ["+50'", 0], ["+1h", 0]]
        for i in range(len(input_minutely)):
            rain.append(input_minutely[i]["precipitation"])
        for i in range(6):
            rain_next_hour[i][1] = sum(rain[i * 10 + 1:i * 10 + 10])
        return rain_next_hour

    def hourly_forecast(self):
        hourly = {"+3h": {"temp": "", "pop": "", "id": ""}, "+6h": {"temp": "", "pop": "", "id": ""},
                  "+12h": {"temp": "", "pop": "", "id": ""}}
        # Forecast +3h
        hourly["+3h"]["temp"] = "{:.0f}".format(self.data["hourly"][3]["temp"] - 273.15) + "°C"
        hourly["+3h"]["pop"] = "{:.0f}".format(self.data["hourly"][3]["pop"] * 100) + "%"
        hourly["+3h"]["id"] = self.data["hourly"][3]["weather"][0]["id"]
        # Forecast +3h
        hourly["+6h"]["temp"] = "{:.0f}".format(self.data["hourly"][6]["temp"] - 273.15) + "°C"
        hourly["+6h"]["pop"] = "{:.0f}".format(self.data["hourly"][6]["pop"] * 100) + "%"
        hourly["+6h"]["id"] = self.data["hourly"][6]["weather"][0]["id"]
        # Forecast +3h
        hourly["+12h"]["temp"] = "{:.0f}".format(self.data["hourly"][12]["temp"] - 273.15) + "°C"
        hourly["+12h"]["pop"] = "{:.0f}".format(self.data["hourly"][12]["pop"] * 100) + "%"
        hourly["+12h"]["id"] = self.data["hourly"][12]["weather"][0]["id"]

        return hourly

    def daily_forecast(self):
        daily = {"+24h": {"date": "", "min": "", "max": "", "pop": "", "id": ""},
                 "+48h": {"date": "", "min": "", "max": "", "pop": "", "id": ""},
                 "+72h": {"date": "", "min": "", "max": "", "pop": "", "id": ""},
                 "+96h": {"date": "", "min": "", "max": "", "pop": "", "id": ""}}
        i = 1
        for key in daily.keys():
            daily[key]["date"] = time.strftime("%A", time.localtime(self.data["daily"][i]["dt"]))
            daily[key]["min"] = "{:.0f}".format(self.data["daily"][i]["temp"]["min"] - 273.15) + "°C"
            daily[key]["max"] = "{:.0f}".format(self.data["daily"][i]["temp"]["max"] - 273.15) + "°C"
            daily[key]["pop"] = "{:.0f}".format(self.data["daily"][i]["pop"] * 100) + "%"
            daily[key]["id"] = self.data["daily"][i]["weather"][0]["id"]
            i += 1

        return daily

    def graph_p_t(self):
        if self.prevision[0] != self.data["daily"][0]["dt"]:
            self.prevision[0] = self.data["daily"][0]["dt"]
            self.prevision = [self.prevision[0], self.prevision[1][1:]]
            self.prevision[1].append(
                [self.data["daily"][0]["pressure"], round(self.data["daily"][0]["temp"]["day"] - 273.15, 0)])

    def weather_description(self, id):
        icon = "sun"
        weather_detail = "Beau temps"
        if id // 100 != 8:
            id = id // 100
            if id == 2:
                icon = "thunder"
                weather_detail = "Orage"
            elif id == 3:
                icon = "drizzle"
                weather_detail = "Bruine"
            elif id == 5:
                icon = "rain"
                weather_detail = "Pluie"
            elif id == 6:
                icon = "snow"
                weather_detail = "Neige"
            elif id == 7:
                icon = "atm"
                weather_detail = "Brouillard"
            else:
                weather_detail = "Erreur"
        else:
            if id == 801:
                icon = "25_clouds"
                weather_detail = "Peu nuageux"
            elif id == 802:
                icon = "50_clouds"
                weather_detail = "Nuageux"
            elif id == 803 or id == 804:
                icon = "100_clouds"
                weather_detail = "Couvert"

        return icon, weather_detail

    def alert(self):
        try:
            alert_descrip = self.data["alerts"][0]["event"]
        except:
            alert_descrip = 0
        return alert_descrip


class Pollution:
    def __init__(self):
        self.max_lvl_pollution = {"co": 10000, "no": 30, "no2": 40, "o3": 120, "so2": 50, "pm2_5": 20, "pm10": 30,
                                  "nh3": 100}
        pass

    def update(self, lattitude, longitude, api_id):
        self.data = requests.get(
            f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lattitude}&lon={longitude}&appid={api_id}").json()
        return self.data

    def co(self):
        return self.data["list"][0]["components"]["co"]

    def no(self):
        return self.data["list"][0]["components"]["no"]

    def no2(self):
        return self.data["list"][0]["components"]["no2"]

    def o3(self):
        return self.data["list"][0]["components"]["o3"]

    def so2(self):
        return self.data["list"][0]["components"]["so2"]

    def pm2_5(self):
        return self.data["list"][0]["components"]["pm2_5"]

    def pm10(self):
        return self.data["list"][0]["components"]["pm10"]

    def nh3(self):
        return self.data["list"][0]["components"]["nh3"]
