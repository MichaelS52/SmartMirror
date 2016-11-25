import pygame, sys, os, pytz, calendar, time as t, constants
from datetime import datetime
from pytz import timezone
from forecastio import *

running = True
pygame.init()
screen = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

width, height = screen.get_size()
lastWeather = -constants.WEATHER_UPDATE #this makes it so the first time the update() method is called, it gets the weather.
fade = -constants.FADE_INCREMENT

# create time label
tFont70 = pygame.font.Font(None, 70)
tFont35 = pygame.font.Font(None, 35)
fontColor = (255, 255, 255)
fontBackground = (0, 0, 0)

def fadeIn():
    global fade
    global fontColor
    while(True):
        if(abs(fade-t.clock())>constants.FADE_INCREMENT):
            fade = t.clock() #update last fade
            newInc = fontColor[0]+1
            fontColor = (newInc,newInc,newInc)
            if(newInc<255):
                break

def fadeOut():
    global fade
    global fontColor
    while(True):
        if(abs(fade-t.clock())>constants.FADE_INCREMENT):
            fade = t.clock() #update last fade
            newInc = fontColor[0]-1
            fontColor = (newInc,newInc,newInc)
            print(fontColor)
        else:
            print(abs(fade-t.clock()))
            if(fontColor[0]>0):
                break

def getTime():
    tz = timezone('EST')
    fmt = '%H:%M'
    nowTime = datetime.now().strftime(fmt)
    convertedTime = datetime.strptime(nowTime, fmt)
    return convertedTime.strftime('%I:%M %p')
def getWeekDay():
    return calendar.day_name[datetime.today().weekday()]

def getDate():
    return datetime.today().strftime("%b %d %Y")

def getCompassDirection(angle):
    dirs = {
        0 : 'N',
        45 : 'NE',
        90 : 'E',
        135 : 'SE',
        180 : 'S',
        225 : 'SW',
        270 : 'W',
        315 : 'NW',
        360 : 'N'
    }

    smallestA, smallestSymbol = 361, 'N'
    for key, value in dirs.iteritems():
        if(abs(angle-key)<smallestA):
            smallestA = abs(angle-key)
            smallestSymbol = value
    return smallestSymbol

def drawGoodMorning():
    pygame.draw.rect(screen, (255,255,255), (100,150,width-200,height-400), 3)
    time = tFont70.render("Good Morning", True, fontColor, fontBackground)
    t_rect = time.get_rect()
    t_rect.centerx, t_rect.centery = width/2, 200
    screen.blit(time, t_rect)

def getWeather():
    api = "xxx"
    lat = xxx
    long = xxx

    forecast = load_forecast(api, lat, long)
    global lastWeather
    lastWeather = t.clock()
    return forecast

def update():
    #TIME
    time = tFont70.render(getTime(), True, fontColor, fontBackground)
    t_rect = time.get_rect()
    t_rect.centerx, t_rect.centery = width-140,40

    #DAY OF WEEK
    weekDay = tFont35.render(getWeekDay() + " " + getDate(), True, fontColor, fontBackground)
    w_rect = weekDay.get_rect()
    w_rect.centerx, w_rect.centery = width-140,80

    #TEMPERATURE
    if(t.clock()-lastWeather>constants.WEATHER_UPDATE):
        forecast = getWeather()
        current = forecast.currently()
        print(current.summary)
        print(current.icon)
        temp = tFont70.render(str(int(current.temperature))+u'\N{DEGREE SIGN}'+'F', True, fontColor, fontBackground)
        temp_rect = temp.get_rect()
        temp_rect.left, temp_rect.top = 25, 20
        screen.blit(temp, temp_rect)

        wind = tFont35.render("W: " + str(int(current.windSpeed))+'mph ' + getCompassDirection(current.windBearing), True, fontColor, fontBackground)
        wind_rect = wind.get_rect()
        wind_rect.left, wind_rect.top = 25, 70
        screen.blit(wind, wind_rect)

        type=""
        if(current.precipIntensity!=0):
            type = str(current.precipType)

        prec = tFont35.render("Prec: " + str(int(current.precipProbability*100)) + "% " + type, True, fontColor, fontBackground)
        prec_rect = prec.get_rect()
        prec_rect.left, prec_rect.top = 25, 100
        screen.blit(prec, prec_rect)

    #ADD TO SCREEN
    screen.blit(time, t_rect)
    screen.blit(weekDay, w_rect)

if __name__ == "__main__":
    fadeOut()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        update()
        pygame.display.flip()
        clock.tick(constants.FRAMERATE)
