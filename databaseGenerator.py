import pathlib
import csv 
import random

path = pathlib.Path('db/data/')
hash = "pbkdf2:sha256:260000$MOIs1KeH1QXaKRfI$b15f8d6e19a23a46afe367488e2f4aa460994d4ab0a6273cc88ae48537beb3c5"

eloRows = []
def writeToFile(filename, rows):
  
  fpath = (path / filename).with_suffix('.csv')
  with fpath.open(mode='a') as csvfile:
    writer = csv.writer(csvfile)
   
    writer.writerows(rows)

def generateRows(rowFunction): 
  rows = []
  for i in range(26, 5000): 
      rows.append(rowFunction(i))
  return rows

def activityRow(i): 
  return ["fakeactivity{num}".format(num = i),"People"] 

def eventRow(i):
  year = random.randint(2000, 2021)
  month = random.randint(1,12)
  day = random.randint(1, 28)
  randomDate = "{}-{:02d}-{:02d}".format(year, month, day)
  randomActivity = "fakeactivity{num}".format(num = i)
  randomEvent = "Fake Event {num}".format(num = i)
  return [i, randomEvent, randomActivity, randomDate, random.randint(300, 1000), random.randint(500, 2000)]

def leagueRow(i):
  return [i, "fake league{num}".format(num = i), "fake name{num}".format(num = i)]

def participatesRow(i): 
  return [i, "fakeactivity{num}".format(num = i), random.randint(200, 2000)]

def ELORow(i, userID, activity, matchID): 
  return [i, userID, activity, random.randint(200, 2000), matchID]

def memberRow(i):
  return ["fakeleague{num}".format(num =i), "fakeemail{num}@email.com".format(num = i), "member"]
  
def rankableRow(i): 
  return [i, "fakeemail{num}@email.com".format(num = i), hash, "fake name{num}".format(num = i), "People", "About" ]

def matchRow(i): 
  global eloRows
  year = random.randint(2000, 2020)
  month = random.randint(1,12)
  day = random.randint(1, 28)

  activities = ['spikeball', 'soccer', 'frisbee',
'chess',
'foosball',
'volleyball',
'basketball',
'tennis',
'smash',
'mariokart']

  timestamp = "{}-{:02d}-{:02d}".format(year, month, day)
  users = random.sample(range(0, 9), 2)

  p = random.random()
  q = random.random()
  accepted = False
  score1 = None
  score2 = None
  if p < 0.9:
    score1 = random.randint(0, 21)
    score2 = random.randint(0, 21)
    if q < 0.9:
      accepted = True
  
  randomActivity = activities[random.randint(0, 9)]
  eloRows.append(ELORow(i, users[0], randomActivity, i))
  #return [activities[random.randint(0, 9)], i, users[0],  users[1],  random.randint(0, 21),  random.randint(0, 21), timestamp, True]
  return [randomActivity, i, users[0],  users[1],  score1,  score2, timestamp, accepted]

print("test")
writeToFile("Matches", generateRows(matchRow)) 
writeToFile("ELOHistory", eloRows)
#writeToFile("Activity", generateRows(activityRow))

#writeToFile("ParticipatesIn", generateRows(participatesRow))
#writeToFile("ELOHistory", generateRows(ELORow))
#writeToFile("Rankables", generateRows(rankableRow))
#writeToFile("Member_of", generateRows(memberRow))