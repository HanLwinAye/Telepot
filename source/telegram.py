import telepot
from telepot.loop import MessageLoop
import picamera
import RPi.GPIO as GPIO
import psutil as PSU
import time
import random
import datetime as dt
import requests, json #for openweather
from itertools import islice
from math import ceil
from itertools import dropwhile, takewhile
from datetime import datetime
from instaloader import Instaloader, Profile
import os

led0 = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led0, GPIO.OUT)

L = Instaloader(download_videos=False, download_video_thumbnails=False, download_geotags=False, download_comments=False, save_metadata=False)

loveStickerIds = ( "CAACAgIAAxkBAAKhD168DBcckcMgYxD7lw-3l23VZGTlAALZAgAC8-O-C5aWAeDAzy8iGQQ", \
                   "CAACAgIAAxkBAAKhBF68C5-3BFWLjGSo-9IcGzX6FTS0AAIgAAOc_jIwtdxzHomqKuAZBA", \
                   "CAACAgIAAxkBAAKhUV68D4ezCor7Nfm6fOqodMVuHYpuAAILAAOWn4wOm5UfezCz9rsZBA" , \
                   "CAACAgIAAxkBAAKhVV68D6dUvHER3am88J610VxspMUeAALSAANWnb0KDgVyNnWDNYoZBA", \
                   "CAACAgIAAxkBAAKhWV68D89gkxUPwHYvydWJbgoETdXgAAKhCQACeVziCagm3C4FTvQFGQQ",\
                   "CAACAgIAAxkBAAKhXV68D_QkHpHUaJgyzgPxvd-tapthAAIZAAPANk8T0EOA9iBXFEsZBA",\
                   "CAACAgIAAxkBAAKhYV68EBgfPXsgW3I9ONcwiDyQtgX5AAJmAwACfvLFDKrILLBImiE9GQQ",\
                   "CAACAgIAAxkBAAKhZV68EDcsjDYBf5OyvqclSeZMEeknAAIwAAPBnGAML87fE0wKZ5wZBA",\
                   "CAACAgIAAxkBAAKhbV68EGELWRV3Zod9nmUxta4sJyFCAAJ_AANYqsQHSmY0LgyOboUZBA",\
                   "CAACAgIAAxkBAAKhdF68EJAxOjzHA0FBdYjgSim1y00dAAJMAQACFkJrCob_LAlLlqcnGQQ")

def greeting():
    #769955312
    #-359089337
    
    now = dt.datetime.now()
    Hr = int(now.strftime("%H"))
    Min = int(now.strftime("%M"))
    Sec = int(now.strftime("%S"))
    if( Hr == 23 and Min == 59 and Sec >= 30 and Sec <= 40):
        bot.sendMessage(769955312,"ကောင်းသောညချမ်းပါ။")
        bot.sendMessage(-359089337,"ကောင်းသောညချမ်းပါ။")
    elif( Hr == 8 and Min == 00 and Sec >= 30 and Sec <= 40):
        bot.sendMessage(769955312,"မင်္ဂလာနံနက်ခင်းပါ။")
        bot.sendMessage(-359089337,"မင်္ဂလာနံနက်ခင်းပါ။")
    elif( Hr == 12 and Min == 00 and Sec >= 0 and Sec <= 10):
        bot.sendMessage(769955312,"Yeah !!! Lunch Time.")
        bot.sendSticker(769955312,"CAACAgIAAxkBAAKuJl68vXv3IUfRpt2sSu1-M3wSqgHbAAKAAAP3AsgPwZI7y_9qCeMZBA")
        bot.sendMessage(-359089337,"Yeah !!! Lunch Time.")
        bot.sendSticker(-359089337,"CAACAgIAAxkBAAKuJl68vXv3IUfRpt2sSu1-M3wSqgHbAAKAAAP3AsgPwZI7y_9qCeMZBA")

def openWeatherForcest(ChatId,CityInput):
    api_key = "7ed86e61050b114fb3b19148cc5b0d99"
    
    #Base URL variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    #complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + CityInput + "&units=metric"
    
    # get method of requests module
    # return response object
    response = requests.get(complete_url)
    
    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()
    
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        # store the value of "main"
        # key in variable y
        y = x["main"]
        
        current_temperature = y["temp"]
        current_realFeel = y["feels_like"]
        current_tempMax = y["temp_max"] 
        current_tempMin = y["temp_min"] 
        current_pressure = y["pressure"] 
        current_humidity = y["humidity"]
        
        z = x["weather"] 
        weather_description = z[0]["description"] 
        retStr = "Weather information at " + CityInput + "\r\n" \
                 + " Temperature (deg Celsius) = " + str(current_temperature) + "\r\n"\
                 + " Min Temperature (deg Celsius) = " + str(current_tempMin) + "\r\n"\
                 + " Max Temperature (deg Celsius) = " + str(current_tempMax) + "\r\n"\
                 + " Real feel Temperature (deg Celsius) = " + str(current_realFeel) + "\r\n"\
                 + " Atmospheric Pressure (hPa) = " + str(current_pressure) + "\r\n"\
                 + " Humidity (%) = " + str(current_humidity) + "\r\n"\
                 + " Description = " + str(weather_description)
        bot.sendMessage(ChatId, retStr)
        
    else:
        bot.sendMessage(ChatId,"City Not Found")
        
def sendIGPhotos(chat_id,path_in):
    files = []
    path = path_in
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))
    for f in files:
        bot.sendPhoto(chat_id, photo=open(f, 'rb'))
    bot.sendMessage(chat_id, "Photos sending finished")
    

def send(messageIn):
    bot.sendMessage(chat_id,messageIn);

def handle(msg):
    global chat_id
    
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print("Message received from " + str(chat_id))
    print("Message received " + command)
           
    if command == '/start' or command == '/Start':
        send("Welcome to Linn Bot")
        send("နေကောင်းလား")
       
    elif command == '/light_on' or command == "/light_on@Linn_0001_bot_for_Pi3BPlus_bot" :
        GPIO.output(led0,1);
        send("led0 is turned on")
        
    elif command == '/light_off' or command == "/light_off@Linn_0001_bot_for_Pi3BPlus_bot" :
        GPIO.output(led0,0);
        send("led0 is turned off")
    
    elif command == '/sys_info'or command == "/sys_info@Linn_0001_bot_for_Pi3BPlus_bot":
        retStr = "CPU Usage : " + str(PSU.cpu_percent()) + "%\r\n"
        retStr += str(PSU.disk_usage('/')) + "\r\n"
        retStr += str(PSU.sensors_temperatures()) + "\r\n"
        send(retStr)
    elif command == '/love_sticker' or command == '/love_sticker@Linn_0001_bot_for_Pi3BPlus_bot':
        index = random.randint(0,len(loveStickerIds)-1)
        bot.sendSticker(chat_id,loveStickerIds[index])
        
    elif command == '/love_sticker_all' or command == '/love_sticker_all@Linn_0001_bot_for_Pi3BPlus_bot':
        for i in range(0,len(loveStickerIds)):
            bot.sendSticker(chat_id,loveStickerIds[i])
            
    elif command == "/weather_yangon" or command == '/weather_yangon@Linn_0001_bot_for_Pi3BPlus_bot':
        openWeatherForcest(chat_id,"Yangon")

    elif command == "/weather_singapore" or command == '/weather_singapore@Linn_0001_bot_for_Pi3BPlus_bot':
        openWeatherForcest(chat_id,"Singapore")
        
    elif command.find('saveIG') != -1:
        PROFILE = command.split()[1]
        print("I got_"+PROFILE)
        profile = Profile.from_username(L.context, PROFILE)
        posts = profile.get_posts()
        SINCE = datetime(2020, 5, 1)
        UNTIL = datetime(2020, 5, 17)
        filtered_posts = filter(lambda p: SINCE <= p.date <= UNTIL, posts)
        send("Downloading " + PROFILE + " Instagram photos since 01/May/2020")
        for post in filtered_posts:
            L.download_post(post, PROFILE)
        send("Download Finsished")
    elif command.find('sendIG') != -1:
        PROFILE = command.split()[1]
        browseLoc = '/home/pi/Desktop/Telepot/Telepot/source/' + PROFILE + '/'
        sendIGPhotos(chat_id,browseLoc)
           
    else:
        send("Invalid Command")

       
bot = telepot.Bot('1213614546:AAH3pP__AD7TCNoha3HyB6hK0eSQdPDgQDI')
#bot.message_loop(handle)
MessageLoop(bot,handle).run_as_thread()
print("Bot is ready")
while True:
    greeting()
    time.sleep(7)
    

