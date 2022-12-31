from discordrp import Presence
import time
import os
import asyncio
import aioconsole as aio
import json
import os



file = None
try:
	file = open(os.path.dirname(__file__) + "/activity.json")
	activity = json.load(file)
except:
	print("Cannot read activity.json.")
	exit(1)
finally:
	if file is not None:
		file.close()


activity["timestamps"] = {}
activity["timestamps"]["start"] = int(time.time() - time.clock_gettime(1))


async def aloop(presence: Presence):
	i = 0
	last_time = time.time()
	update = {}
	while True:
		inp = await aio.ainput(">> ")
		match inp.split():
			case ["exit"]:
				print("Exiting...")
				break
			
			case ["textup" | "toptext", *text]:
				res = ""
				for t in text:
					res += t + ' '
				res = res[:-1]

				update.update({'details': res})
				print(f"Top text is going to be \"{res}\".")
			
			case ["textdown" | "bottomtext", *text]:
				res = ""
				for t in text:
					res += t + ' '
				res = res[:-1]

				update.update({'state': res})
				print(f"Bottom text is going to be \"{res}\".")
			
			case ["update"]:
				if len(update) < 1:
					print("There's nothing to update.")
					print(update)
					continue
					
				time_passed = time.time() - last_time
				if time_passed < 15:
					print(f"Wait for {15 - time_passed} seconds to execute a command.")
					continue
				

				activity.update(update)
				presence.set(activity)
				update.clear()
				last_time = time.time()
		
	exit()


presence = None
file = None
try:
	file = open(os.path.dirname(__file__) + "/app_id")
	presence_id = file.readline()
	
	if presence_id[-1] == '\n':
		presence_id = presence_id[:-1]
	
	if not presence_id.isdigit():
		print("App id is not valid.")
		exit(-1)

	presence = Presence(presence_id)
	presence.set(activity)

	asyncio.run(aloop(presence))
	

except Exception as e:
	print(e)
finally:
	if presence is not None:
		presence.close()
	
	if file is not None:
		file.close()