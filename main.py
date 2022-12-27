from discordrp import Presence
import time

presence = None
try:
	presence = Presence("1014098359616819241")
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