import json, time,easygui
import urllib.request

wunderground_key = 'b11d489d04091824'
google_time_zone_key = 'AIzaSyAKPWjvEUM1EGdRZYT9LxCnJf5M7DC1HWY'
sky_scanner_key = 'prtl6749387986743898559646983194'

running = True

class hotel:
    def __init__(self, name, h_id):
        self.name = name
        self.h_id = h_id
    def name(self):
        return self.name
    def h_id(self):
        return self.h_id

def only_upper(s):
    upper_chars = ''
    for i in s:
        if i.isupper():
            upper_chars += i
    return upper_chars

def removestr(s):
    s1 = s.replace(' ', '_')
    s2 = s1.replace('{', '')
    s3 = s2.replace('}', '')
    return s3

def replace_brk(s):
    s1 = s.replace('{', '')
    s2 = s1.replace('}', '')
    return s2

def weather():
    mode = easygui.buttonbox('Do you want to input a location manually or should Travel_Bot acquire location automatically?', choices=("Manual", "Auto(less accurate)"))
    if mode == 'Manual':
        address = easygui.enterbox("What is your postal code/city?").lower()
        for i in "!@#$%^&*(){}: ":
            address.replace(i, '')
    elif mode == 'Auto(less accurate)':
        address = 'autoip'
    url = 'http://api.wunderground.com/api/'+wunderground_key+'/geolookup/conditions/q/'+address+'.json'
    f = urllib.request.urlopen(url)
    easygui.msgbox("Looking up weather...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    city = parsed_json['location']['city']
    state = parsed_json['location']['state']
    weather = parsed_json['current_observation']['weather']
    wind = parsed_json['current_observation']['wind_string']
    temp = parsed_json['current_observation']['temperature_string']
    feelslike = parsed_json['current_observation']['feelslike_string']
    precip = parsed_json['current_observation']['precip_today_string']
    easygui.msgbox('Weather in '+city+', '+state+': '+weather.lower()+'. The temperature is '+temp+', but it feels like '+feelslike+". ")
    easygui.msgbox('Wind: '+wind.lower()+', Precipitation: '+precip.lower()+'.')
    f.close()

def time_zone():
    url = 'http://api.wunderground.com/api/'+wunderground_key+'/geolookup/conditions/q/autoip.json'
    f = urllib.request.urlopen(url)
    easygui.msgbox("Getting current location...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    latitude = parsed_json['current_observation']['observation_location']['latitude']
    longitude = parsed_json['current_observation']['observation_location']['longitude']
    f.close()
    url = 'https://maps.googleapis.com/maps/api/timezone/json?location='+latitude+','+longitude+'&timestamp=1331161200&key=AIzaSyAKPWjvEUM1EGdRZYT9LxCnJf5M7DC1HWY'
    f = urllib.request.urlopen(url)
    easygui.msgbox("Getting current time zone...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    tz_name = parsed_json['timeZoneName']
    utc_offset = parsed_json['rawOffset']
    dst_offset = parsed_json['dstOffset']
    total_offset = int(utc_offset)-int(dst_offset)
    if dst_offset != '0':
        dst = easygui.buttonbox("With or without DST offset?(with/without)", choices = ('with', 'without'))
        if dst == 'without':
            total_offset -= dst_offset
            tz_name = tz_name.replace("Daylight", "Standard")
    f.close()
    url = 'http://api.timezonedb.com/v2/get-time-zone?key=YUWVWUHQIFLX&format=json&fields=formatted&by=zone&zone='+only_upper(tz_name)
    f = urllib.request.urlopen(url)
    easygui.msgbox("Getting current time...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    f_time = parsed_json['formatted']
    f.close()
    easygui.msgbox("The current time zone is: "+tz_name+", Time:"+str(f_time)+", and the UTC offset is: "+str(total_offset/3600)+".")

def hotel_suggest():
    global chkin, chkout, ppl, rooms, h_id
    location = easygui.enterbox("Please enter your location (City+State/Province)")
    location1 = removestr(location)
    url = 'http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2/CA/CAD/en-US/'+location1+'?apikey='+sky_scanner_key
    request = urllib.request.Request(url, headers = {'Accept':'application/json'})
    f = urllib.request.urlopen(request)
    easygui.msgbox("Searching for "+location+"...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    p_location = parsed_json['results'][0]
    place_id = p_location['individual_id']
    f.close()
    chkin = easygui.enterbox('Please enter your check-in date.(yyyy-mm-dd)')
    chkout = easygui.enterbox('Please enter your check-out date.(yyyy-mm-dd)')
    ppl = easygui.enterbox('Please enter the amount of guests.')
    rooms = easygui.enterbox('Please enter the amount of rooms desired.')
    url = 'http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/CA/CAD/en-US/'+place_id+'/'+chkin+'/'+chkout+'/'+ppl+'/'+rooms+'?apiKey='+sky_scanner_key
    request = urllib.request.Request(url, headers = {'Accept':'application/json'})
    f = urllib.request.urlopen(request)
    easygui.msgbox("Finding hotels in "+ location +"...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    hotels=parsed_json['hotels']
    hotel1 = hotels[0]
    hotel1_name = hotel1['name']
    hotel1_id = hotel1['hotel_id']
    hotel2 = hotels[1]
    hotel2_name = hotel2['name']
    hotel2_id = hotel2['hotel_id']
    hotel3 = hotels[2]
    hotel3_name = hotel3['name']
    hotel3_id = hotel3['hotel_id']
    hotel_1 = hotel(hotel1_name, hotel1_id)
    hotel_2 = hotel(hotel2_name, hotel2_id)
    hotel_3 = hotel(hotel3_name, hotel3_id)
    choice = easygui.buttonbox((replace_brk(str(hotel_1.name))+', '+replace_brk(str(hotel_2.name))+', '+replace_brk(str(hotel_3.name))), choices=('1','2','3'))
    if choice == '1':
        hotel_choice = hotel_1
    elif choice == '2':
        hotel_choice = hotel_2
    elif choice == '3':
        hotel_choice = hotel_3
    easygui.msgbox("Fetching details for {!s}...".format(hotel_choice.name))
    h_id = hotel_choice.h_id
    f.close()

def hotel_details():
    url = 'http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/CA/CAD/en_US/'+str(h_id)+'/'+chkin+'/'+chkout+'/'+ppl+'/'+rooms+'?apiKey='+sky_scanner_key
    request = urllib.request.Request(url, headers = {'Accept':'application/json'})
    f = urllib.request.urlopen(request).info()
    new_url = f['location']
    time.sleep(2)
    url = 'http://partners.api.skyscanner.net'+new_url
    f = urllib.request.urlopen(url).info()
    url = 'http://partners.api.skyscanner.net'+new_url+'&hotelIds='+str(h_id)
    f = urllib.request.urlopen(url).info()
    new_url = f['location']
    time.sleep(2)
    url = 'http://partners.api.skyscanner.net'+new_url
    f = urllib.request.urlopen(url)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    name = parsed_json['hotels'][0]['name']
    availability = parsed_json['hotels'][0]['tag']
    star_rating = parsed_json['hotels'][0]['star_rating']
    long = parsed_json['hotels'][0]['longitude']
    lat = parsed_json['hotels'][0]['latitude']
    easygui.msgbox("Results for your search: \n Name:{!s} \n Availability: {!s} \n Star Rating: {!s} \n Latitude/Longitude: {!s}/{!s}".format(name, availability, star_rating, lat, long))
    f.close()
    

print("#####################################################")
time.sleep(0.3)
print("###      WELCOME    TO    TRAVEL_BOT v1.0         ###")
time.sleep(0.3)
print("#####################################################")
print('')
print("Booting......")
easygui.msgbox("Welcome to Travel_bot, your trusty travel assistant.")
while running == True:
    action = easygui.buttonbox("How may I be of assistance?", choices=("Current weather", "Time zone/current time", "Hotel service", "Exit"))
    if action == "Current weather":
        weather()
    elif action == "Time zone/current time":
        time_zone()
    elif action == "Hotel service":
        hotel_suggest()
        hotel_details()
    elif action == "Exit":
        running = False
        easygui.msgbox("Thank you for using Travel_bot. Have a safe trip!")



    
    
