# -*- coding:utf-8 -*-

from weather import *
from news import *
from display import *
import json

lat = "47.2108023"
lon = "-1.5596322"
api_key_weather = ""
api_key_news = ""
debug = 0
if debug ==0:
    import epd7in5b_V2
else:
    pass

def map_resize(val, in_mini, in_maxi, out_mini, out_maxi):
    if in_maxi - in_mini != 0:
        out_temp = (val - in_mini) * (out_maxi - out_mini) // (in_maxi - in_mini) + out_mini
    else:
        out_temp = out_mini
    return out_temp


def main():
    ##################################################################################################################
    # FRAME
    display.draw_black.rectangle((5, 5, 795, 475), fill=255, outline=0, width=2)  # INNER FRAME
    display.draw_black.line((540, 5, 540, 350), fill=0, width=1)  # VERTICAL SEPARATION
    display.draw_black.line((350, 5, 350, 350), fill=0, width=1)  # VERTICAL SEPARATION slim
    display.draw_black.line((5, 350, 795, 350), fill=0, width=1)  # HORIZONTAL SEPARATION

    # UPDATED AT
    display.draw_black.text((10, 8), "Mis à jour le " + weather.current_time(), fill=0, font=font8)

    ###################################################################################################################
    # CURRENT WEATHER
    display.draw_icon(20, 55, "r", 75, 75,
                      weather.weather_description(weather.current_weather())[0])  # CURRENT WEATHER ICON
    display.draw_black.text((120, 15), weather.current_temp(), fill=0, font=font48)  # CURRENT TEMP
    display.draw_black.text((230, 15), weather.current_hum(), fill=0, font=font48)  # CURRENT HUM
    display.draw_black.text((245, 65), "Humidité", fill=0, font=font12)  # LABEL "HUMIDITY"
    display.draw_black.text((120, 75), weather.current_wind()[0] + " " + weather.current_wind()[1], fill=0, font=font24)

    display.draw_icon(120, 105, "b", 35, 35, "sunrise")  # SUNRISE ICON
    display.draw_black.text((160, 110), weather.current_sunrise(), fill=0, font=font16)  # SUNRISE TIME
    display.draw_icon(220, 105, "b", 35, 35, "sunset")  # SUNSET ICON
    display.draw_black.text((260, 110), weather.current_sunset(), fill=0, font=font16)  # SUNSET TIME

    ###################################################################################################################
    # NEXT HOUR RAIN
    try :
        data_rain = weather.rain_next_hour()

        # FRAME
        display.draw_black.text((20, 150), "Pluie dans l'heure - " + time.strftime("%H:%M", time.localtime()), fill=0,
                                font=font16)  # NEXT HOUR RAIN LABEL
        display.draw_black.rectangle((20, 175, 320, 195), fill=255, outline=0, width=1)  # Red rectangle = rain

        # LABEL
        for i in range(len(data_rain)):
            display.draw_black.line((20 + i * 50, 175, 20 + i * 50, 195), fill=0, width=1)
            display.draw_black.text((20 + i * 50, 195), data_rain[i][0], fill=0, font=font16)
            if data_rain[i][1] != 0:
                display.draw_red.rectangle((20 + i * 50, 175, 20 + (i + 1) * 50, 195), fill=0)
    except:
        pass

    ###################################################################################################################
    # HOURLY FORECAST
    display.draw_black.text((30, 227), "+3h", fill=0, font=font16)  # +3h LABEL
    display.draw_black.text((150, 227), "+6h", fill=0, font=font16)  # +6h LABEL
    display.draw_black.text((270, 227), "+12h", fill=0, font=font16)  # +12h LABEL
    # 3H
    display.draw_icon(25, 245, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[0])  # +3H WEATHER ICON
    display.draw_black.text((25, 295), weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +3h
    display.draw_black.text((35, 307), weather.hourly_forecast()["+3h"]["temp"], fill=0, font=font16)  # TEMP +3H
    display.draw_black.text((35, 323), weather.hourly_forecast()["+3h"]["pop"], fill=0, font=font16)  # POP +3H
    # +6h
    display.draw_icon(145, 245, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[0])  # +6H WEATHER ICON
    display.draw_black.text((145, 295), weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +6h
    display.draw_black.text((155, 307), weather.hourly_forecast()["+6h"]["temp"], fill=0, font=font16)  # TEMP +6H
    display.draw_black.text((155, 323), weather.hourly_forecast()["+6h"]["pop"], fill=0, font=font16)  # POP +6H
    # +12h
    display.draw_icon(265, 245, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[0])  # +12H WEATHER ICON
    display.draw_black.text((265, 295), weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +12h
    display.draw_black.text((275, 307), weather.hourly_forecast()["+12h"]["temp"], fill=0, font=font16)  # TEMP +12H
    display.draw_black.text((275, 323), weather.hourly_forecast()["+12h"]["pop"], fill=0, font=font16)  # POP +12H

    ###################################################################################################################
    # DAILY FORECAST
    # +24h
    display.draw_black.text((360, 30), weather.daily_forecast()["+24h"]["date"], fill=0, font=font16)  # +24H DAY
    display.draw_icon(400, 50, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+24h"]["id"])[0])  # +24H WEATHER ICON
    display.draw_black.text((465, 50), weather.daily_forecast()["+24h"]["min"], fill=0, font=font14)
    display.draw_black.text((498, 50), "min", fill=0, font=font14)  # +24H MIN TEMPERATURE
    display.draw_black.text((465, 65), weather.daily_forecast()["+24h"]["max"], fill=0, font=font14)
    display.draw_black.text((498, 65), "max", fill=0, font=font14)  # +24H MAX TEMPERATURE
    display.draw_black.text((465, 80), weather.daily_forecast()["+24h"]["pop"], fill=0, font=font14)
    display.draw_black.text((498, 80), "pluie", fill=0, font=font14)  # +24H RAIN PROBABILITY

    # +48h
    display.draw_black.text((360, 105), weather.daily_forecast()["+48h"]["date"], fill=0, font=font16)  # +48H DAY
    display.draw_icon(400, 125, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+48h"]["id"])[0])  # +48H WEATHER ICON
    display.draw_black.text((465, 125), weather.daily_forecast()["+48h"]["min"], fill=0, font=font14)
    display.draw_black.text((498, 125), "min", fill=0, font=font14)  # +48H MIN TEMPERATURE
    display.draw_black.text((465, 140), weather.daily_forecast()["+48h"]["max"], fill=0, font=font14)
    display.draw_black.text((498, 140), "max", fill=0, font=font14)  # +48H MAX TEMPERATURE
    display.draw_black.text((465, 155), weather.daily_forecast()["+48h"]["pop"], fill=0, font=font14)
    display.draw_black.text((498, 155), "pluie", fill=0, font=font14)  # +48H RAIN PROBABILITY

    # +72h
    display.draw_black.text((360, 180), weather.daily_forecast()["+72h"]["date"], fill=0, font=font16)  # +72H DAY
    display.draw_icon(400, 200, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+72h"]["id"])[0])  # +72H WEATHER ICON
    display.draw_black.text((465, 200), weather.daily_forecast()["+72h"]["min"], fill=0, font=font14)
    display.draw_black.text((498, 200), "min", fill=0, font=font14)  # +72H MIN TEMPERATURE
    display.draw_black.text((465, 215), weather.daily_forecast()["+72h"]["max"], fill=0, font=font14)
    display.draw_black.text((498, 215), "max", fill=0, font=font14)  # +72H MAX TEMPERATURE
    display.draw_black.text((465, 230), weather.daily_forecast()["+72h"]["pop"], fill=0, font=font14)
    display.draw_black.text((498, 230), "pluie", fill=0, font=font14)  # +72H RAIN PROBABILITY

    # +96h
    display.draw_black.text((360, 255), weather.daily_forecast()["+96h"]["date"], fill=0, font=font16)  # +96H DAY
    display.draw_icon(400, 275, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+96h"]["id"])[0])  # +96H WEATHER ICON
    display.draw_black.text((465, 275), weather.daily_forecast()["+96h"]["min"], fill=0, font=font14)
    display.draw_black.text((498, 275), "min", fill=0, font=font14)  # +96H MIN TEMPERATURE
    display.draw_black.text((465, 290), weather.daily_forecast()["+96h"]["max"], fill=0, font=font14)
    display.draw_black.text((498, 290), "max", fill=0, font=font14)  # +96H MAX TEMPERATURE
    display.draw_black.text((465, 305), weather.daily_forecast()["+96h"]["pop"], fill=0, font=font14)
    display.draw_black.text((498, 305), "pluie", fill=0, font=font14)  # +96H RAIN PROBABILITY

    ###################################################################################################################
    # GRAPHS
    # PRESSURE & TEMPERATURE
    pression = []
    temperature = []
    maxi = 440  # MAX VERT. PIXEL OF THE GRAPH
    mini = 360  # MIN VERT PIXEL OF THE GRAPH
    x = [55, 105, 155, 205, 255, 305, 355]  # X value of the points
    j = ["J-6", "J-5", "J-4", "J-3", "J-2", "J-1", "J"]  # LABELS


    weather.graph_p_t()
    data = weather.prevision[1]
    global been_reboot
    if (been_reboot == 1):
        try :
            file = open("saved.txt","r")
            weather.prevision[1] = json.loads(file.read())
            data = weather.prevision[1]
            been_reboot = 0
            file.close()
        except:
            pass

    else :
        pass

    file = open("saved.txt", "w")
    file.write(str(data))
    file.close()
    for i in range(len(data)):
        pression.append(data[i][0])
        temperature.append(data[i][1])

    # PRESSURE
    display.draw_black.line((40, mini, 40, maxi + 20), fill=0, width=1)  # GRAPH AXIS
    display.draw_black.text((10, mini), str(max(pression)), fill=0, font=font12)  # MAX AXIS GRAPH LABEL
    display.draw_black.text((10, maxi), str(min(pression)), fill=0, font=font12)  # MIN AXIS GRAPH LABEL
    display.draw_black.text((10, mini + (maxi - mini) // 2), str((max(pression) + min(pression)) // 2), fill=0,
                            font=font12)  # MID VALUE LABEL
    for i in range(len(x)):  # UPDATE CIRCLE POINTS
        display.draw_black.text((x[i], 455), j[i], fill=0, font=font12)
        display.draw_circle(x[i], map_resize(pression[i], min(pression), max(pression), maxi, mini), 3, "r")
    for i in range(len(x) - 1):  # UPDATE LINE
        display.draw_red.line((x[i], map_resize(pression[i], min(pression), max(pression), maxi, mini), x[i + 1],
                               map_resize(pression[i + 1], min(pression), max(pression), maxi, mini)), fill=0,
                              width=2)
    # TEMPERATURE
    display.draw_black.line((430, mini, 430, maxi + 20), fill=0, width=1)  # GRAPH AXIS
    display.draw_black.text((410, mini), str(max(temperature)), fill=0, font=font12)  # MAX AXIS GRAPH LABEL
    display.draw_black.text((410, maxi), str(min(temperature)), fill=0, font=font12)  # MIN AXIS GRAPH LABEL
    display.draw_black.text((410, mini + (maxi - mini) // 2), str((max(temperature) + min(temperature)) // 2), fill=0,
                            font=font12)  # MID VALUE LABEL
    for i in range(len(x)):  # UPDATE CIRCLE POINTS
        display.draw_black.text((x[i] + 400, 455), j[i], fill=0, font=font12)
        display.draw_circle(x[i] + 400, map_resize(temperature[i], min(temperature), max(temperature), maxi, mini), 3,
                            "r")
    for i in range(len(x) - 1):  # UPDATE LINE
        display.draw_red.line((x[i] + 400, map_resize(temperature[i], min(temperature), max(temperature), maxi, mini),
                               x[i + 1] + 400,
                               map_resize(temperature[i + 1], min(temperature), max(temperature), maxi, mini)),
                              fill=0, width=2)

    ###################################################################################################################
    # ALERT AND POLLUTION

    ###################################################################################################################
    # NEWS UPDATE
    news_selected = news.selected_title()
    display.draw_black.text((550, 15), "NEWS", fill=0, font=font24)
    for i in range(5):
        if len(news_selected) == 1:
            display.draw_black.text((550, 40), news_selected[0], fill=0, font=font14)
            break
        else:
            if len(news_selected[i]) <= 3 :
                for j in range(len(news_selected[i])):
                    display.draw_black.text((550, 40 + j * 15 + i * 60), news_selected[i][j], fill=0, font=font14)
            else:
                for j in range(2):
                    display.draw_black.text((550, 40 + j * 15 + i * 60), news_selected[i][j], fill=0, font=font14)
                display.draw_black.text((550, 40 + 2 * 15 + i * 60), news_selected[i][2] + "[...]", fill=0, font=font14)



    ###################################################################################################################
    print("Updating screen...")
    # display.im_black.show()
    # display.im_red.show()  
    print("\tPrinting...")

    time.sleep(2)
    epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
    time.sleep(2)	
    return True


if __name__ == "__main__":
    global been_reboot
    been_reboot=1
    while True:
        try:
            weather = Weather(lat, lon, api_key_weather)
            # pollution = Pollution()
            news = News()
            break
        except:
            current_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            print("INITIALIZATION PROBLEM- @" + current_time)
            time.sleep(2)
    epd = epd7in5b_V2.EPD()
    while True:
        # Defining objects
        current_time = time.strftime("%d/%m/%Y %H:%M", time.localtime())
        print("Begin update @" + current_time)
        print("Creating display")
        display = Display()
        # Update values
        weather.update()
        print("Weather Updated")
        # pollution.update(lat, lon, api_key_weather)
        news.update(api_key_news)
        print("News Updated")        
        print("Main program running...")
        epd.init()
        epd.Clear()
        main()
        print("Going to sleep...")
        epd.init()
        epd.sleep()
        print("Sleeping ZZZzzzzZZZzzz")
        print("Done")
        print("------------")
        time.sleep(1800)

