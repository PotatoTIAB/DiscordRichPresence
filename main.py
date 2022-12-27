from discordrp import Presence
import time
import os
import asyncio
import aioconsole


activity = {
	'details': "Messing with Rich Presence",
	'state': 'PC has been running for:',
	'timestamps': {
		'start': int(time.time() - time.clock_gettime(1))
	},
	'assets': {
		'large_image': 'slime'
	}
}

async def aloop(presence):
	i = 0
	while True:
		print(i)
		await asyncio.sleep(1)
		i += 1
		if i == 10:
			break
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