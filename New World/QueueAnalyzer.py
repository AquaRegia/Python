import os
from datetime import datetime, timezone, timedelta

def formatTime(s):
    h = s // 3600
    s -= h * 3600
    
    m = s // 60
    s -= m * 60
    
    return f"{h:02}:{m:02}:{s:02}"

gameLogPath = os.path.join(os.getenv("LOCALAPPDATA"), "AGS", "New World", "Game.log")
gameLog = open(gameLogPath, "r").read().splitlines()

playerName = ""
inQueue = False
positions = []

#for log in gameLog:
    #print(log)

for log in gameLog:
    if "Connect: playerName = " in log:
        playerName = log.split("= ")[1]
    elif "[GameConnection] Queuing login" in log:
        inQueue = True
    elif "[GameConnection] Waiting in login queue" in log:
        positions.append({"time": datetime.fromisoformat(log[1:].split(">")[0]), 
                          "position": int(log.split("Position (")[1].split(")")[0])})
                          
if not inQueue and len(positions) > 0:
    print("Currently not in queue")
else:
    positionStart = positions[0]
    positionNow = positions[-1]
    position30 = positionStart
    position5 = positionStart
    
    for p in positions:
        if p["time"] < (positionNow["time"] - timedelta(minutes=30)):
            position30 = p
        else:
            break
            
    for p in positions:
        if p["time"] < (positionNow["time"] - timedelta(minutes=5)):
            position5 = p
        else:
            break
            
    timeLeftStart = formatTime(int(positionNow["position"] / ((positionStart["position"] - positionNow["position"]) / (positionNow["time"] - positionStart["time"]).seconds)))
    timeLeft30 = formatTime(int(positionNow["position"] / ((position30["position"] - positionNow["position"]) / (positionNow["time"] - position30["time"]).seconds)))
    timeLeft5 = formatTime(int(positionNow["position"] / ((position5["position"] - positionNow["position"]) / (positionNow["time"] - position5["time"]).seconds)))
            
    print(f"Queueing with {playerName} for {formatTime((datetime.utcnow() - positionStart['time']).seconds)}")
    print("---")
    print(f"Position at start: {positionStart['position']}")
    print(f"Position (up to) 30 minutes ago: {position30['position']}")
    print(f"Position (up to) 5 minutes ago: {position5['position']}")
    print(f"Position now: {positionNow['position']}")
    print("---")
    print(f"Time left (all time): {timeLeftStart}")
    print(f"Time left (30 minutes): {timeLeft30}")
    print(f"Time left (5 minutes): {timeLeft5}")
