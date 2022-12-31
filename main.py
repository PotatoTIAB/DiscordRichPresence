from discordrp import Presence
import time
import os
import asyncio
import aioconsole as aio
import json
import os


try:
	file = open(os.path.dirname(__file__) + "/activity.json")
	activity = json.load(file)
except:
	print("can't read from the file")
	exit(1)

activity["timestamps"] = {}
activity["timestamps"]["start"] = int(time.time() - time.clock_gettime(1))


async def waita():
	for i in range(15, -1, -1):
		print(f"\rWait for {i} seconds for next command.", end='')
		await asyncio.sleep(1)
		print("\r                                       ", end='')
	print('\r', end='')

async def aloop(presence: Presence):
	i = 0
	await waita()
	while True:
		update = False

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

				activity['details'] = res
				update = True
				print(f"Changed top text to \"{res}\".")
			case ["textdown" | "bottomtext", *text]:
				res = ""
				for t in text:
					res += t + ' '
				res = res[:-1]

				activity['state'] = res
				update = True
				print(f"Changed bottom text to \"{res}\".")
		
		if update:
			presence.set(activity)
			await waita()
		
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