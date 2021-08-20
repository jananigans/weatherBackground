import requests, json
from requests import get
from PIL import Image, ImageFont, ImageDraw
import os
import math

#Main method. Gets location, calls stuff
def main():
    api_key = "secret key"

    #Gets current external IP
    ip = get('https://api.ipify.org').text

    #Gets lat and lon from IP
    response = requests.get("https://freegeoip.app/json/").json()

    lat=response.get('latitude')
    lon=response.get('longitude')

    #Gets the icons for the next 5 hours probably
    hourlyIcons=hourly(api_key,lat,lon)

    #Gets the temperature in kelvin, converts to Farenheights
    temp=(((current(api_key,lat,lon)[0]-273.15)*1.8)+32)
    temp=round(temp,2)

    #Gets humidity and current weather icon
    humid=current(api_key,lat,lon)[1]
    icon=current(api_key,lat,lon)[2]

    #creates desktop background with helpful weather information
    drawImage(icon,hourlyIcons,temp,humid)

    #prints current weather for polybar
    print(icon)

#Gets weather info from openweathermap API
def current(api_key,lat,lon):
    icon=''
    temp=''
    humid=''

    #Gets the things from the stuff
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(lat)+"&lon="+str(lon)+"&exclude=hourly,minutely,daily,alerts&appid="+api_key

    response = requests.get(base_url)

    #parsing
    x=response.json()

    #more parsing
    currentForcast=x.get('current')
    temp=currentForcast.get('temp')
    humid=currentForcast.get('humidity')
    weather=currentForcast.get('weather')

    #icon
    icon=iconGuy(weather[0].get('icon'))

    #probably a smarter way of doing this but whatever
    return(temp,humid,icon)

#Returns a string of five icons regarding the weather
def hourly(api_key,lat,lon):
    icons=''
    finalIconList=''
    #get stuff
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(lat)+"&lon="+str(lon)+"&exclude=current,minutely,daily,alerts&appid="+api_key

    response = requests.get(base_url)

    x=response.json()

    hourlyForcast=x.get('hourly')

    #parses stuff six times. Not starting at 0 because that's current? I think?
    for i in range(1,6):
            weather=hourlyForcast[i].get('weather')
            icons+=iconGuy(weather[0].get('icon'))+" "

    #returns stuff
    return(icons)

#Draw the image to my desktop background
def drawImage(weather_icon,hourly_icons,current_temperature,current_humidiy):
    try:
        #open a temporary image in my polybar directory
        #I have no idea how the PIL works, actually
        img = Image.open("~/.config/polybar/tmp.png")
        draw = ImageDraw.Draw(img)

        #fonts are scary
        font = ImageFont.truetype("/usr/share/fonts/TTF/NotoSansMono-Regular-Nerd-Font-Complete.ttf", 100)
        smallIconFont = ImageFont.truetype("/usr/share/fonts/TTF/NotoSansMono-Regular-Nerd-Font-Complete.ttf", 50)
        textFont = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 100)
        smallFont = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 50)

        #todo: make things align better
        draw.text((100, 100),str(weather_icon),(74,114,81),font=font)
        draw.text((250, 100),str(hourly_icons),(74,114,81),font=smallIconFont)
        draw.text((100, 200),str(current_temperature)+"°",(74,114,81),font=textFont)
        draw.text((100, 300),str(current_humidiy)+"%",(74,114,81),font=smallFont)
        img.save('~/.config/polybar/tmp1.png')

        #using feh, make it my background
        os.system('feh --bg-scale ~/.config/polybar/tmp1.png')

    #standard error stuff
    except FileNotFoundError as error:
        print ("No image found.")
    except:
        print (str(weather_icon))

#return the proper NerdFont icon from the three character code from openweathermap
#night varients optional
def iconGuy(icon):
        if str(icon) == "01d":
                icon = " "
        elif str(icon) == "01n":
                icon = " "
        elif str(icon) == "02d":
                icon = " "
        elif str(icon) == "03d":
                icon = " "
        elif str(icon) == "02n":
                icon = " "
        elif str(icon) == "03n":
                icon = " "
        elif str(icon)[:2] == "04":
                icon = " "
        elif str(icon)[:2] == "09":
                icon = " "
        elif str(icon)[:2] == "10":
                icon = " "
        elif str(icon)[:2] == "11":
                icon = " "
        elif str(icon)[:2] == "13":
                icon = " "
        elif str(icon)[:2] == "50":
                icon = "敖"

        return icon

main() 
