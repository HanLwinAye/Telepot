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
    #769955312  MyID
    #-359089337 FA GroupID
    
    now = dt.datetime.now()
    Hr = int(now.strftime("%H"))
    Min = int(now.strftime("%M"))
    Sec = int(now.strftime("%S"))
    if( Hr == 23 and Min == 59 and Sec >= 30 and Sec <= 40):
        bot.sendMessage(769955312,"ကောင်းသောညချမ်းပါ။")
        bot.sendMessage(-359089337,"Good Night All!!!")
    elif( Hr == 8 and Min == 00 and Sec >= 30 and Sec <= 40):
        bot.sendMessage(769955312,"မင်္ဂလာနံနက်ခင်းပါ။")
        bot.sendMessage(-359089337,"Good Morning All !!!")
    elif( Hr == 12 and Min == 00 and Sec >= 0 and Sec <= 10):
        bot.sendMessage(769955312,"Yeah !!! Lunch Time.")
        bot.sendSticker(769955312,"CAACAgIAAxkBAAKuJl68vXv3IUfRpt2sSu1-M3wSqgHbAAKAAAP3AsgPwZI7y_9qCeMZBA")
        bot.sendMessage(-359089337,"Yeah !!! Lunch Time.")
        bot.sendSticker(-359089337,"CAACAgIAAxkBAAKuJl68vXv3IUfRpt2sSu1-M3wSqgHbAAKAAAP3AsgPwZI7y_9qCeMZBA")

def openWeatherForcest(ChatId,CityInput):
    
    #Base URL variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    #complete url address
    complete_url = base_url + "appid=" + OW_API_KEY + "&q=" + CityInput + "&units=metric"
    
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
        
def sendIGPhotos(chat_id,path_in,startDate):
    files = []
    path = path_in
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file and startDate in file:
                files.append(os.path.join(r, file))
    fileCount = len(files)
    bot.sendMessage(chat_id, "Total " + str(fileCount ) + " files found")
    if fileCount > 0:
        for f in files:
            bot.sendPhoto(chat_id, photo=open(f, 'rb'))
        bot.sendMessage(chat_id, "saveIG command finished")
    else:
        bot.sendMessage(chat_id,"No photos found")
    

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
        send("ကိုမြင့်နိုင်ကြီး ဘေးမှကင်းဝေးပါစေလို. ဆုမွန်ကောင်းတောင်းလိုက်ပါတယ်")
       
    elif command.find('/light_on') != -1:
        GPIO.output(led0,1);
        send("led0 is turned on")
        
    elif command.find('/light_off') != -1:
        GPIO.output(led0,0);
        send("led0 is turned off")
    
    elif command.find('/sys_info') != -1 :
        retStr = "CPU Usage : " + str(PSU.cpu_percent()) + "%\r\n"
        retStr += str(PSU.disk_usage('/')) + "\r\n"
        retStr += str(PSU.sensors_temperatures()) + "\r\n"
        send(retStr)
    elif command.find('/love_sticker') != -1:
        index = random.randint(0,len(loveStickerIds)-1)
        bot.sendSticker(chat_id,loveStickerIds[index])
        
    elif command.find('/love_sticker_all') != -1:
        for i in range(0,len(loveStickerIds)):
            bot.sendSticker(chat_id,loveStickerIds[i])
            
    elif command.find("/weather_yangon") != -1:
        openWeatherForcest(chat_id,"Yangon")

    elif command.find("/weather_singapore") != -1:
        openWeatherForcest(chat_id,"Singapore")
    
    elif command.find('/help') != -1:
        send("/saveIG Name 01/05/2020 05/05/2020")
        send("/sendIG Name 01/05/2020")
        
    elif command.find('saveIG') != -1: #Command Format, "/saveIG Name 01/05/2020 05/05/2020"
        PROFILE = command.split()[1]   #Name
        startDate = command.split()[2] #01/05/2020
        endDate = command.split()[3]   #05/05/2020
        print("I got_"+PROFILE)
        profile = Profile.from_username(L.context, PROFILE)
        posts = profile.get_posts()
        SINCE = datetime(int(startDate.split('/')[2]),int(startDate.split('/')[1]),int(startDate.split('/')[0])) #Year, Month, Day
        UNTIL = datetime(int(endDate.split('/')[2]),int(endDate.split('/')[1]),int(endDate.split('/')[0])) #Year, Month, Day
        filtered_posts = filter(lambda p: SINCE <= p.date <= UNTIL, posts)
        send("Downloading " + PROFILE + " Instagram photos from " + startDate + " to " + endDate ) 
        for post in filtered_posts:
            L.download_post(post, PROFILE)
        send("Download Finsished")
    elif command.find('sendIG') != -1: #Command Format, "/sendIG Name 01/05/2020"
        PROFILE = command.split()[1]
        date = command.split()[2]
        #convert the day-month-year to year-month-day format
        date = date.split('/')
        date = date[2] + '-' + date[1] + '-' + date[0]
        browseLoc = '/home/pi/Desktop/Telepot/Telepot/source/' + PROFILE + '/'
        sendIGPhotos(chat_id,browseLoc,date)
           
    else:
        send("Invalid Command")

BotAPIKey = input("Enter your telegram bot API Key:")
OW_API_KEY = input("Enter Open Weather API key:")
bot = telepot.Bot(BotAPIKey)
#bot.message_loop(handle)
MessageLoop(bot,handle).run_as_thread()
print("Bot is ready")
while True:
    greeting()
    time.sleep(7)
    

