import requests
from sense_hat import SenseHat

sense = SenseHat()
sense.low_light = True

apiKey = "d45dca8645c0b739603ef14631a198d9"

cities = ["new+york",
          "manama",
          "phoenix",
          "singapore",
          "orlando"]

citiesIndex = 0
currentCity = ""
temp = 0
minTemp = 0
maxTemp = 0
humidity = 0

def getWeatherData():
    global temp
    global minTemp
    global maxTemp
    global humidity
    global currentCity
    
    url = ("http://api.openweathermap.org/data/2.5/weather?"
           "q="+cities[citiesIndex]+"&appid="+apiKey+"&units=metric")
    r = requests.get(url)
    data = r.json()

    sense.clear()

    currentCity = data["name"]
    temp = data["main"]["temp"]
    minTemp = data["main"]["temp_min"]
    maxTemp = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]

def calculatePixels(measurement,color,right,left):
    pixels = int(measurement / 3)
    #more than 16 pixels will cause an error with Sense HAT
    if pixels > 16:
        pixels = 16

    for pixel in range(int(pixels / 2) + (pixels % 2)):
        sense.set_pixel(right,pixel,color)
    for pixel in range(int(pixels / 2)):
        sense.set_pixel(left,pixel,color)

def updateTemp():
    calculatePixels(humidity,(0,0,204),0,1)
    calculatePixels(minTemp,(51,204,204),2,3)
    calculatePixels(maxTemp,(255,0,0),4,5)
    calculatePixels(temp,(51,153,102),6,7)

def showCity():
    global currentCity
    sense.show_message(currentCity, 0.04, text_colour=[100,100,100])

def showValues():
    sense.show_message("current temp: " + str(temp), 0.05, text_colour=[51,153,102])
    sense.show_message("max temp: " + str(maxTemp), 0.05, text_colour=[255,0,0])
    sense.show_message("min temp: " + str(minTemp), 0.05, text_colour=[51,204,204])
    sense.show_message("humidity: " + str(humidity), 0.05, text_colour=[51,153,102])
    
getWeatherData()
showCity()
updateTemp()
sense.set_rotation(180)
while True:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            print(event.direction, event.action)

            if event.direction == "left":
                citiesIndex -= 1

            if event.direction == "right":
                citiesIndex += 1

            if 0 >citiesIndex or citiesIndex > len(cities) - 1:
                citiesIndex = 0

            getWeatherData()
            sense.set_rotation(0)
            showCity()

            if event.direction == "middle":
                showValues()
            sense.set_rotation(180)
            updateTemp()
            
            
