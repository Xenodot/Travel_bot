import json, time
import urllib.request

wunderground_key = 'b11d489d04091824'
google_time_zone_key = 'AIzaSyAKPWjvEUM1EGdRZYT9LxCnJf5M7DC1HWY'
sky_scanner_key = 'prtl6749387986743898559646983194'

def only_upper(s):
    upper_chars = ''
    for i in s:
        if i.isupper():
            upper_chars += i
    return upper_chars

def weather():
    a = input('Do you want to input a location manually or should Travel_Bot acquire location automatically? ("m" for manual, "a" for automatic)')
    if a.lower() == 'm':
        address = input("What is your postal code/city?").lower()
        for i in "!@#$%^&*() ":
            address.replace(i, '')
    elif a.lower() == 'a':
        address = 'autoip'
    url = 'http://api.wunderground.com/api/'+wunderground_key+'/geolookup/conditions/q/'+address+'.json'
    f = urlopen(url)
    print("Looking up weather...")
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
    print('Weather in '+city+', '+state+': '+weather.lower()+'. The temperature is '+temp+', but it feels like '+feelslike+". ")
    print('Wind: '+wind.lower()+', Precipitation: '+precip.lower()+'.')
    f.close()

def time_zone():
    url = 'http://api.wunderground.com/api/'+wunderground_key+'/geolookup/conditions/q/autoip.json'
    f = urlopen(url)
    print("Getting current location...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    latitude = parsed_json['current_observation']['observation_location']['latitude']
    longitude = parsed_json['current_observation']['observation_location']['longitude']
    f.close()
    url = 'https://maps.googleapis.com/maps/api/timezone/json?location='+latitude+','+longitude+'&timestamp=1331161200&key=AIzaSyAKPWjvEUM1EGdRZYT9LxCnJf5M7DC1HWY'
    f = urlopen(url)
    print("Getting current time zone...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    tz_name = parsed_json['timeZoneName']
    utc_offset = parsed_json['rawOffset']
    dst_offset = parsed_json['dstOffset']
    total_offset = int(utc_offset)-int(dst_offset)
    if dst_offset != '0':
        a = input("With or without DST offset?(with/without)")
        if a == 'without':
            total_offset -= dst_offset
            tz_name = tz_name.replace("Daylight", "Standard")
    f.close()
    url = 'http://api.timezonedb.com/v2/get-time-zone?key=YUWVWUHQIFLX&format=json&fields=formatted&by=zone&zone='+only_upper(tz_name)
    f = urlopen(url)
    print("Getting current time...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    f_time = parsed_json['formatted']
    f.close()
    print("The current time zone is: "+tz_name+", Time:"+str(f_time)+", and the UTC offset is: "+str(total_offset/3600)+".")

def hotel_suggest():
    location = input("Where are you currently?")
    url = 'http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2/CA/CAD/en-US/'+location+'?apikey='+sky_scanner_key
    request = urllib.request.Request(url, headers = {'Accept':'application/json'})
    f = urllib.request.urlopen(request)
    print("Searching for "+location+"...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    p_location = parsed_json['results'][0]
    place_id = p_location['individual_id']
    print(place_id)
    f.close()
    chkin = input('Please enter your check-in date.')
    chkout = input('Please enter your check-out date.')
    ppl = input('Please enter the amount of guests.')
    rooms = input('Please enter the amount of rooms desired.')
    url = 'http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/CA/CAD/en-US/'+place_id+'/'+chkin+'/'+chkout+'/'+ppl+'/'+rooms+'?apiKey='+sky_scanner_key
    request = urllib.request.Request(url, headers = {'Accept':'application/json'})
    f = urllib.request.urlopen(request)
    print("Finding hotels in "+ location +"...")
    time.sleep(3)
    json_str = f.read()
    parsed_json = json.loads(json_str)
    print(parsed_json)
    f.close()
    
weather()
time_zone()
hotel_suggest()

    
    
