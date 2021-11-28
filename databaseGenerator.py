import pathlib
import csv 
import random

path = pathlib.Path('db/data/')

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

def ELORow(i): 
  return [i,random.randint(0, 9), "fakeactivity{num}".format(num = i), random.randint(200, 2000), i + 20]

  
def rankableRow(i): 
  return [i, "People", "fake name{num}".format(num = i)]

def matchRow(i): 
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


  #return [activities[random.randint(0, 9)], i, users[0],  users[1],  random.randint(0, 21),  random.randint(0, 21), timestamp, True]
  return [activities[random.randint(0, 9)], i, users[0],  users[1],  score1,  score2, timestamp, accepted]

#writeToFile("Activity", generateRows(activityRow))
#writeToFile("Matches", generateRows(matchRow))
#writeToFile("ParticipatesIn", generateRows(participatesRow))
writeToFile("ELOHistory", generateRows(ELORow))
#writeToFile("Events", generateRows(eventRow))