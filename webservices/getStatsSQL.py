#! /usr/env python

import mysql.connector
from sets import Set
from bottle import route, run, request, hook, response
from collections import defaultdict, OrderedDict
import math

# Allowing Cross-Origin Resource Sharing for content returned by all URLs
@hook('before_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

# Defining functions for all endpoints
@route('/1K')
def queries_1K():
	# Connecting to MySQL Database and initializing cursor
	cnx = mysql.connector.connect(user='root', password='mysql', database='273project')
	cursor = cnx.cursor()

	# Getting track name from the query part
	traname = request.query.traname

	# Executing query
	query = 'SELECT DISTINCT temptable.userid, temptable.gender, temptable.age, temptable.country FROM (SELECT profile_1k.userid, profile_1k.gender,profile_1k.age,profile_1k.country FROM profile_1k INNER JOIN main_1k ON profile_1k.userid=main_1k.userid and main_1k.traname=\"' + str(traname) + '\") as temptable'
	cursor.execute(query)
	userCount = 0

	# Initialising lists
	genderList = []
	ageList = []
	countryList = []	
	weekdayList = []
	hourList = []
	#artistList = []
        #trackList = []

	# Building lists
	for userid,gender,age,country in cursor:
		userCount += 1
		genderList.append(str(gender))
		ageList.append(str(age))
		countryList.append(str(country))

	# Building dictionary to return
	returnDict = {}
	if userCount >= 1:
		returnDict["status"] = "OK"
	else:
		returnDict["status"] = "NORESULTS"
		return returnDict
	returnDict["usercount"] = userCount
	
	# Aggregating gender values and adding to returnDict
	tempDict = defaultdict(int)
	for each in genderList:
		tempDict[each] += 1
	doThis = tempDict.pop('',None) # Removing the NULL values count. If no NULL values, return None
	returnDict["gender"] = dict(tempDict)
	tempDict.clear()
	
	# Aggregating age values and adding to returnDict
	for each in ageList:
		tempDict[each] += 1
	doThis = tempDict.pop("0",None)
	returnDict["age"] = dict(tempDict)
	tempDict.clear()

	# Aggregating country values and adding to returnDict
	for each in countryList:
		tempDict[each] += 1
	doThis = tempDict.pop('',None)
	# Begin section to combine latitude, longitude pairs from allcountryDict
	exceptionCount = 0
	countryDict = dict(tempDict)
	modifiedDict = {}
	modifiedDict = OrderedDict(modifiedDict)
	global allcountryDict
	for each in countryDict:
	# Handling exception if key does not exist. Ignoring that country.
		try:
			modifiedDict[each] = {}
			modifiedDict[each]["latitude"] = allcountryDict[each][0]
			modifiedDict[each]["value"] = countryDict[each]
			modifiedDict[each]["longitude"] = allcountryDict[each][1]
		except KeyError:
                        exceptionCount += 1
                        print exceptionCount,each
	returnDict["country"] = modifiedDict
	tempDict.clear()
	# End section

#	returnDict["country"] = dict(tempDict)
#	tempDict.clear()

	# Second query to get timestamp related data
	query = 'SELECT DAYNAME(timestamp), HOUR(timestamp) from main_1k WHERE main_1k.traname=\"' + traname + '\"'
	cursor.execute(query)
	timestampCount = 0

	# Building Lists
	for weekday,hour in cursor:
                timestampCount += 1
                weekdayList.append(str(weekday))
                hourList.append(str(hour))
	returnDict["timestampcount"] = timestampCount

	# Aggregating weekday values and adding to returnDict
	for each in weekdayList:
		tempDict[each] += 1
	doThis = tempDict.pop('',None)
	weekdayDict = {}
        weekdayDict = OrderedDict(weekdayDict)
	try:
		weekdayDict["Monday"] = tempDict["Monday"]
		weekdayDict["Tuesday"] = tempDict["Tuesday"]
		weekdayDict["Wednesday"] = tempDict["Wednesday"]
		weekdayDict["Thursday"] = tempDict["Thursday"]
		weekdayDict["Friday"] = tempDict["Friday"]
		weekdayDict["Saturday"] = tempDict["Saturday"]
		weekdayDict["Sunday"] = tempDict["Sunday"]
	except KeyError:
		print "KeyError occured"
	returnDict["weekday"] = weekdayDict
	tempDict.clear()

	# Aggregating hour values and adding to returnDict
	for each in hourList:
		tempDict[each] += 1
	doThis = tempDict.pop('',None)
	returnDict["hour"] = dict(tempDict)
	tempDict.clear()

	# Third query to get track information
	#query = 'SELECT DISTINCT artname, traname FROM main_1k WHERE traname=\"' + traname + '\"'
	#cursor.execute(query)
	#for artist, track in cursor:
	#	artistList.append(artist)
	#	trackList.append(track)
	#returnDict["artist"] = artistList
	#returnDict["traname"] = trackList

	# Close the cursor, connection to MySQL and return the returnDict
	cursor.close()
	cnx.close()
	return returnDict


@route('/360K')
def queries_360K():
	# Connecting to MySQL Database and initializing cursor
	cnx = mysql.connector.connect(user='root', password='mysql', database='273project')
	cursor = cnx.cursor()

	# Getting artist name from the query part
	artname = request.query.artname

	# Executing query
	query = 'SELECT profile_360k.gender, profile_360k.age, profile_360k.country FROM profile_360k INNER JOIN main_360k ON profile_360k.usersha1=main_360k.usersha1 and artname="' + str(artname) + '\"'
	cursor.execute(query)
	userCount = 0

	# Initialising lists
	genderList = []
	ageList = []
	countryList = []	

	# Building lists
	for gender,age,country in cursor:
		userCount += 1
		genderList.append(str(gender))
		ageList.append(str(age))
		countryList.append(str(country))

	# Building dictionary to return
	returnDict = {}
	if userCount >= 1:
		returnDict["status"] = "OK"
	else:
		returnDict["status"] = "NORESULTS"
		return returnDict
	returnDict["usercount"] = userCount
	
	# Aggregating gender values and adding to returnDict
	tempDict = defaultdict(int)
	for each in genderList:
		tempDict[each] += 1
	doThis = tempDict.pop('',None) # Removing the NULL values count. If no NULL values, return None
	returnDict["gender"] = dict(tempDict)
	tempDict.clear()
	
	# Aggregating age values and adding to returnDict
	for each in ageList:
		tempDict[each] += 1
	doThis = tempDict.pop("0",None)
	returnDict["age"] = dict(tempDict)
	tempDict.clear()

	# Aggregating country values and adding to returnDict
	for each in countryList:
		tempDict[each] += 1
	doThis = tempDict.pop('',None)
        # Begin section to combine latitude, longitude pairs from allcountryDict
        exceptionCount = 0
        countryDict = dict(tempDict)
        modifiedDict = {}
        modifiedDict = OrderedDict(modifiedDict)
        global allcountryDict
        for each in countryDict:
        # Handling exception if key does not exist. Ignoring that country.
                try:   
                        modifiedDict[each] = {}
                        modifiedDict[each]["latitude"] = allcountryDict[each][0]
                        modifiedDict[each]["value"] = countryDict[each]
                        modifiedDict[each]["longitude"] = allcountryDict[each][1]
                except KeyError:
                        exceptionCount += 1
                        print exceptionCount,each
        returnDict["country"] = modifiedDict
        tempDict.clear()
        # End section
	
	#returnDict["country"] = dict(tempDict)
	#tempDict.clear()

	# Close the cursor, connection to MySQL and return the returnDict
	cursor.close()
	cnx.close()
	return returnDict
	
@route('/usersimilarity')
def queries_usersimilarity():
	# Connecting to MySQL Database and initializing cursor
        cnx = mysql.connector.connect(user='root', password='mysql', database='273project')
        cursor = cnx.cursor()	

	# Getting user1 and user2 from the query part
	user1 = request.query.user1
	user2 = request.query.user2

	# Initializing sets to store users' top artists and lists to store plays
        user1Artists = Set([])
        user2Artists = Set([])
        user1Dict = {}
        user2Dict = {}
        user1Plays = []
        user2Plays = []

	# Initializing the returnDict
        returnDict = {}

	# Getting profiles of user1 and user2
        userCount = 0
        query = 'SELECT usersha1, gender, age, country, registered FROM profile_360k WHERE usersha1="' + str(user1) + '\"'
        cursor.execute(query)
        for usersha1, gender, age, country, registered in cursor:
                userCount += 1
                returnDict["user1"] = usersha1
                returnDict["gender1"] = gender
                returnDict["age1"] = age
                returnDict["country1"] = country
                returnDict["registered1"] = registered

        if userCount != 1:
                returnDict["status"] = "WRONG USER1"
                return returnDict

        query = 'SELECT usersha1, gender, age, country, registered FROM profile_360k WHERE usersha1="' + str(user2) + '\"'
        cursor.execute(query)
        for usersha1, gender, age, country, registered in cursor:
                userCount += 1
                returnDict["user2"] = usersha1
                returnDict["gender2"] = gender
                returnDict["age2"] = age
		returnDict["country2"] = country
                returnDict["registered2"] = registered

        if userCount != 2:
                returnDict["status"]= "WRONG USER2"
                return returnDict
        returnDict["status"] = "OK"
	
	# Getting top artists for user1 and user2
        query = 'SELECT artname,plays FROM main_360k WHERE usersha1="' + str(user1) + '\"'
        cursor.execute(query)
        for artname,plays in cursor:
                user1Artists.add(artname.encode('utf-8'))
                user1Dict[artname] = plays
        query = 'SELECT artname,plays FROM main_360k WHERE usersha1="' + str(user2) + '\"'
        cursor.execute(query)
        for artname,plays in cursor:
                user2Artists.add(artname.encode('utf-8'))
                user2Dict[artname] = plays

	# Adding common artists to returnDict
	returnDict["common"] = ['None'] # Initializing with 'None', i.e. no common artists
	intersect = user1Artists.intersection(user2Artists)
	if len(intersect) > 0:
		returnDict["common"].pop()
		for each in list(intersect):
			returnDict["common"].append(each)

	# Calculating Cosine Similarity
        intersect = user1Artists.intersection(user2Artists)
        if len(intersect) > 0:
                for each in intersect:
                        user1Plays.append(user1Dict[each])
                        user2Plays.append(user2Dict[each])
                sumxx,sumyy,sumxy = 0,0,0 
                for i in range(len(user1Plays)):
                        x=user1Plays[i]
                        y=user2Plays[i]
                        sumxx += x*x
                        sumyy += y*y
                        sumxy += x*y
                cosineSimilarity = sumxy/math.sqrt(sumxx*sumyy)
                returnDict["similarity"] = cosineSimilarity
        else:
                returnDict["similarity"] = 0

        # Close the cursor, connection to MySQL and return the returnDict
        cursor.close()
        cnx.close()
        return returnDict

if __name__ == "__main__":
	allcountryDict = {'Canada': [60.0, -95.0], 'Libyan Arab Jamahiriya': [25.0, 17.0], 'Sao Tome and Principe': [1.0, 7.0], 'Guernsey': [49.28, -2.35], 'Iran, Islamic Republic of': [32.0, 53.0], 'Lithuania': [56.0, 24.0], 'Saint Pierre and Miquelon': [46.5, -56.2], 'Macao': [22.1, 113.33], 'Aruba': [12.3, -69.58], 'Swaziland': [-26.3, 31.3], 'Belize': [17.15, -88.45], 'Argentina': [-34.0, -64.0], 'Bolivia': [-17.0, -65.0], 'Cameroon': [6.0, 12.0], 'Burkina Faso': [13.0, -2.0], 'Turkmenistan': [40.0, 60.0], 'Ghana': [8.0, -2.0], 'Saudi Arabia': [25.0, 45.0], 'Togo': [8.0, 1.1], 'Cape Verde': [16.0, -24.0], 'Cocos (Keeling) Islands': [-12.3, 96.5], 'Faroe Islands': [62.0, -7.0], 'Guatemala': [15.3, -90.15], 'Asia & Pacific': [0.0, 0.0], 'Bosnia and Herzegovina': [44.0, 18.0], 'Kuwait': [29.3, 45.45], 'Russian Federation': [60.0, 100.0], 'Germany': [51.0, 9.0], 'Saint Barthelemy': [17.9, -62.85], 'Spain': [40.0, -4.0], 'Australia': [-27.0, 133.0], 'Liberia': [6.3, -9.3], 'Maldives': [3.15, 73.0], 'Armenia': [40.0, 45.0], 'Jamaica': [18.15, -77.3], 'Oman': [21.0, 57.0], 'Christmas Island': [-10.3, 105.4], 'Gabon': [-1.0, 11.45], 'Niue': [-19.02, -169.52], 'Monaco': [43.44, 7.24], 'Wallis and Futuna': [-13.18, -176.12], 'New Zealand': [-41.0, 174.0], 'Yemen': [15.0, 48.0], 'European Union': [50.1021, 9.9], 'Jersey': [49.15, -2.1], 'Pakistan': [30.0, 70.0], 'Greenland': [72.0, -40.0], 'Samoa': [-13.35, -172.2], 'Ethiopia': [8.0, 38.0], 'Norfolk Island': [-29.02, 167.57], 'United Arab Emirates': [24.0, 54.0], 'Guam': [13.28, 144.47], 'India': [20.0, 77.0], 'Azerbaijan': [40.3, 47.3], "Cote D'Ivoire": [8.0, -5.0], 'Svalbard': [78.0, 20.0], 'Saint Vincent and the Grenadines': [13.15, -61.12], 'Kenya': [1.0, 38.0], 'Congo Republic': [-1.0, 15.0], 'Turkey': [39.0, 35.0], 'Afghanistan': [33.0, 65.0], 'Northern Mariana Islands': [15.12, 145.45], 'Andorra': [42.3, 1.3], 'Eritrea': [15.0, 39.0], 'Solomon Islands': [-8.0, 159.0], 'Turks and Caicos Islands': [21.45, -71.35], 'Saint Lucia': [13.53, -60.58], 'Hungary': [47.0, 20.0], 'San Marino': [43.46, 12.25], 'French Polynesia': [-15.0, -140.0], 'France': [46.0, 2.0], 'Bermuda': [32.2, -64.45], 'Slovakia': [48.4, 19.3], 'Somalia': [10.0, 49.0], 'Peru': [-10.0, -76.0], 'Vanuatu': [-16.0, 167.0], 'Brazil': [-10.0, -55.0], 'Nauru': [-0.32, 166.55], 'Norway': [62.0, 10.0], 'Malawi': [-13.3, 34.0], 'Cook Islands': [-21.14, -159.46], 'Benin': [9.3, 2.15], 'Korea, Republic of': [37.0, 127.3], 'Congo, the Democratic Republic of the': [0.0, 25.0], 'Cuba': [21.3, -80.0], 'Montenegro': [42.3, 19.18], 'Saint Kitts and Nevis': [17.2, -62.45], 'British Indian Ocean Territory': [-6.0, 71.3], 'Virgin Islands': [18.2, -64.5], 'China': [35.0, 105.0], 'Micronesia, Federated States of': [6.55, 158.15], 'Antigua and Barbuda': [17.03, -61.48], 'Dominican Republic': [19.0, -70.4], 'Heard Island and McDonald Islands': [-53.06, 72.31], 'Ukraine': [49.0, 32.0], 'Bahrain': [26.0, 50.33], 'Tonga': [-20.0, -175.0], 'Indonesia': [-5.0, 120.0], 'Western Sahara': [24.3, -13.0], 'Finland': [64.0, 26.0], 'Central African Republic': [7.0, 21.0], 'Mauritius': [-20.17, 57.33], 'Tajikistan': [39.0, 71.0], 'Sweden': [62.0, 15.0], 'Viet Nam': [16.1, 107.5], 'British Virgin Islands': [18.3, -64.3], 'Mali': [17.0, -4.0], 'Cambodia': [13.0, 105.0], 'Bulgaria': [43.0, 25.0], 'United States': [38.0, -97.0], 'Romania': [46.0, 25.0], 'Angola': [-12.3, 18.3], 'French Southern Territories': [-37.5, 77.32], 'Portugal': [39.3, -8.0], 'South Africa': [-29.0, 24.0], 'Tokelau': [-9.0, -172.0], 'Fiji': [-18.0, 175.0], 'Liechtenstein': [47.16, 9.32], 'Qatar': [25.3, 51.15], 'Malaysia': [2.3, 112.3], 'Senegal': [14.0, -14.0], 'Mozambique': [-18.15, 35.0], 'Uganda': [1.0, 32.0], 'Japan': [36.0, 138.0], 'Niger': [16.0, 8.0], 'Isle of Man': [54.15, -4.3], 'Saint Martin': [18.05, -63.57], 'Pitcairn': [-25.04, -130.06], 'Guinea': [11.0, -10.0], 'Panama': [9.0, -80.0], 'Costa Rica': [10.0, -84.0], 'Luxembourg': [49.45, 6.1], 'American Samoa': [-14.2, -170.0], 'Bahamas': [24.15, -76.0], 'Gibraltar': [36.08, -5.21], 'Ireland': [53.0, -8.0], 'Italy': [42.5, 12.5], 'Nigeria': [10.0, 8.0], 'Ecuador': [-2.0, -77.3], 'Czech Republic': [49.45, 15.3], 'Belarus': [53.0, 28.0], "Korea, Democratic People's Republic of": [40.0, 127.0], 'Algeria': [28.0, 3.0], 'Slovenia': [46.07, 14.49], 'El Salvador': [13.5, -88.55], 'Tuvalu': [-8.0, 178.0], 'Marshall Islands': [9.0, 168.0], 'Chile': [-30.0, -71.0], 'Puerto Rico': [18.15, -66.3], 'Belgium': [50.5, 4.0], 'Kiribati': [1.25, 173.0], 'Haiti': [19.0, -72.25], 'Iraq': [33.0, 44.0], 'Hong Kong': [22.15, 114.1], 'Sierra Leone': [8.3, -11.3], 'Georgia': [42.0, 43.3], "Lao People's Democratic Republic": [18.0, 105.0], 'Gambia': [13.28, -16.34], 'Poland': [52.0, 20.0], 'Moldova': [47.0, 29.0], 'Morocco': [32.0, -5.0], 'Albania': [41.0, 20.0], 'Croatia': [45.1, 15.3], 'Mongolia': [46.0, 105.0], 'Guinea-Bissau': [12.0, -15.0], 'Thailand': [15.0, 100.0], 'Switzerland': [47.0, 8.0], 'Grenada': [12.07, -61.4], 'Bangladesh': [24.0, 90.0], 'Seychelles': [-4.35, 55.4], 'Tanzania, United Republic of': [-6.0, 35.0], 'Chad': [15.0, 19.0], 'Estonia': [59.0, 26.0], 'Uruguay': [-33.0, -56.0], 'Equatorial Guinea': [2.0, 10.0], 'Lebanon': [33.5, 35.5], 'Uzbekistan': [41.0, 64.0], 'Tunisia': [34.0, 9.0], 'Falkland Islands (Malvinas)': [-51.45, -59.0], 'Rwanda': [-2.0, 30.0], 'Timor-Leste': [-8.5, 125.55], 'Dominica': [15.25, -61.2], 'Colombia': [4.0, -72.0], 'Burundi': [-3.3, 30.0], 'Taiwan': [23.3, 121.0], 'Cyprus': [35.0, 33.0], 'Barbados': [13.1, -59.32], 'Madagascar': [-20.0, 47.0], 'Palau': [7.3, 134.3], 'Denmark': [56.0, 10.0], 'Bhutan': [27.3, 90.3], 'Sudan': [15.0, 30.0], 'Nepal': [28.0, 84.0], 'Malta': [35.5, 14.35], 'Brunei Darussalam': [4.3, 114.4], 'Comoros': [-12.1, 44.15], 'Netherlands': [52.3, 5.45], 'Suriname': [4.0, -56.0], 'Lesotho': [-29.3, 28.3], 'Anguilla': [18.15, -63.1], 'Venezuela': [8.0, -66.0], 'Holy See (Vatican City State)': [41.54, 12.27], 'Saint Helena Ascension and Tristan da Cunha': [-15.57, -5.42], 'Israel': [31.3, 34.45], 'Bouvet Island': [-54.26, 3.24], 'Iceland': [65.0, -18.0], 'Zambia': [-15.0, 30.0], 'Austria': [47.2, 13.2], 'Papua New Guinea': [-6.0, 147.0], 'Trinidad and Tobago': [11.0, -61.0], 'Zimbabwe': [-20.0, 30.0], 'Jordan': [31.0, 36.0], 'Cayman Islands': [19.3, -80.3], 'Kazakhstan': [48.0, 68.0], 'Philippines': [13.0, 122.0], 'Djibouti': [11.3, 43.0], 'Mauritania': [20.0, -12.0], 'Kyrgyzstan': [41.0, 75.0], 'Mayotte': [-12.5, 45.1], 'Montserrat': [16.45, -62.12], 'New Caledonia': [-21.3, 165.3], 'Macedonia': [41.5, 22.0], 'Sri Lanka': [7.0, 81.0], 'Latvia': [57.0, 25.0], 'Guyana': [5.0, -59.0], 'Syria': [35.0, 38.0], 'Honduras': [15.0, -86.3], 'Myanmar': [22.0, 98.0], 'Mexico': [23.0, -102.0], 'Egypt': [27.0, 30.0], 'Nicaragua': [13.0, -85.0], 'Singapore': [1.22, 103.48], 'Serbia': [44.0, 21.0], 'Botswana': [-22.0, 24.0], 'United Kingdom': [54.0, -2.0], 'Antarctica': [-90.0, 0.0], 'Netherlands Antilles': [12.12, -68.15], 'Greece': [39.0, 22.0], 'Paraguay': [-23.0, -58.0], 'Namibia': [-22.0, 17.0], 'Palestinian Territory, Occupied': [31.25, 34.2]}
	# Running the web service
	run(host='0.0.0.0', port=80)
