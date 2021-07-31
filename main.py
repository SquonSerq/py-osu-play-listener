import requests, time, datetime, os

s = requests.Session()

songString = ""
previousStatus = 5
songStartTime = datetime.datetime.now()
playedTime = 0

def writeToFile(songData):
	todayDate = datetime.datetime.now().date()
	if os.path.isdir("./plays data") != True:
		os.mkdir("./plays data")
	f = open(f"./plays data/{todayDate}.txt", "a")
	f.write(songData)
	f.close()

def makeStartStr(songInfo):
	songData = songInfo['menu']['bm']['metadata']
	return f"{datetime.datetime.now()} | https://osu.ppy.sh/b/{songInfo['menu']['bm']['id']} | {songData['artist']} - {songData['title']} {songData['difficulty']} | {r['menu']['mods']['str']}"

def makeEndStr(stStr, endStatus, timePlayed, mapHits):
	res = stStr + f" | Time played: {timePlayed} | {endStatus} | {mapHits} \n"
	return res

writeToFile("New session! \n")
print("Program started!")

while True:
	try:
		r = s.get("http://localhost:24050/json").json()
	except:
		print("Error getting request! Try opening Gosumemory")
		continue

	currentStatus = r['menu']['state']

	if previousStatus != 2 and currentStatus == 2:
		songString = makeStartStr(r)
		songStartTime = datetime.datetime.now()
		playedTime = r['menu']['bm']['time']['current']

	if previousStatus == 2 and currentStatus == 5:
		timePlayed = datetime.datetime.now() - songStartTime
		songString = makeEndStr(songString, "LEAVE", timePlayed, mapHits)
		writeToFile(songString)
		print(songString)
		previousStatus = r['menu']['state']
		continue

	if previousStatus == 2 and currentStatus == 7:
		timePlayed = datetime.datetime.now() - songStartTime
		songString = makeEndStr(songString, "ENDED", timePlayed, mapHits)
		writeToFile(songString)
		print(songString)
		previousStatus = r['menu']['state']
		continue

	if playedTime > r['menu']['bm']['time']['current'] and previousStatus == 2:
		songEndTime = datetime.datetime.now()
		if datetime.timedelta(seconds=5) < songEndTime-songStartTime:
			songString = makeEndStr(songString, "RETRY", songEndTime-songStartTime, mapHits)
			writeToFile(songString)
			print(songString)
			playedTime = r['menu']['bm']['time']['current'] 
			previousStatus = 228
			continue
	
	playedTime = r['menu']['bm']['time']['current'] 
	mapHits = f"{r['gameplay']['hits']['300']}-{r['gameplay']['hits']['100']}-{r['gameplay']['hits']['50']}-{r['gameplay']['hits']['0']}"
	previousStatus = r['menu']['state']



