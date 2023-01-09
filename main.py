from discordrp import Presence
import time
import os

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
	activity = {
        'state': 'PC has been running for:',
        'details': "Messing with Rich Presence",
        'timestamps': {
            'start': int(time.time() - time.clock_gettime(1))
        },
		'assets': {
			'large_image': 'slime'
		}
	}
	presence.set(activity)
	
	

except Exception as e:
	print(e)
finally:
	if presence is not None:
		presence.close()
	
	if file is not None:
		file.close()