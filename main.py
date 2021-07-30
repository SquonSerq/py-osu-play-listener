import requests, time, datetime, os

s = requests.Session()

statusCode = 5
songString = ""
songStartTime = datetime.datetime.now()
playedTime = -123123123
mapHits = ""

def writeToFile(songData):
	todayDate = datetime.datetime.now().date()
	if os.path.isdir("./plays data") != True:
		os.mkdir("./plays data")
	f = open(f"./plays data/{todayDate}.txt", "a")
	f.write(songData)
	f.close()

writeToFile("New session! \n")
print("Program started!")

while True:
	try:
		r = s.get("http://localhost:24050/json").json()
	except:
		print("Error getting request! Try opening Gosumemory")
		continue

	if r['menu']['state'] == 0:
		continue
	
	if r['menu']['state'] != statusCode:
		currentStatus = r['menu']['state']
		
		if currentStatus == 2:
			songData = r['menu']['bm']['metadata']
			songString = f"https://osu.ppy.sh/b/{r['menu']['bm']['id']} | {songData['artist']} - {songData['title']} {songData['difficulty']} | {r['menu']['mods']['str']}"
			songStartTime = datetime.datetime.now()
			playedTime = r['menu']['bm']['time']['current']

		if currentStatus == 7:
			songEndTime = datetime.datetime.now()
			songString += f" | Time played: {songEndTime-songStartTime} | ENDED | {mapHits} \n"
			print(songString) 
			writeToFile(songString)

		if currentStatus == 5 and statusCode != 7:
			songEndTime = datetime.datetime.now()
			songString += f" | Time played: {songEndTime-songStartTime} | LEAVE | {mapHits} \n"
			print(songString) 
			writeToFile(songString)

	if playedTime > r['menu']['bm']['time']['current'] and statusCode == 2:
		songEndTime = datetime.datetime.now()
		if datetime.timedelta(seconds=2) < songEndTime-songStartTime:
			songString += f" | Time played: {songEndTime-songStartTime} | RETRY | {mapHits} \n"
			print(songString) 
			writeToFile(songString)
			playedTime = r['menu']['bm']['time']['current']
			statusCode = 0
			continue

	mapHits = f"{r['gameplay']['hits']['300']}-{r['gameplay']['hits']['100']}-{r['gameplay']['hits']['50']}-{r['gameplay']['hits']['0']}"
	playedTime = r['menu']['bm']['time']['current']
	statusCode =	r['menu']['state'] 

