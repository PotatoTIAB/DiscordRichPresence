from discordrp import Presence
import time
import os
import asyncio
import aioconsole as aio
import json
import os


def read_images():
	file = None
	try:
		file = open(os.path.dirname(__file__) + "/images")
		data = file.read()
		if data is not None and len(data) > 0:
			images = data.split()
		else:
			print("Warning, no images found. Make sure to check './images'.")
			images = []
	except:
		print("Cannot read activity.json.")
		exit(1)
	finally:
		if file is not None:
			file.close()
	return images
	



def read_activity():
	file = None
	activity = {}
	activity["assets"] = {}
	try:
		file = open(os.path.dirname(__file__) + "/activity.json")
		activity.update(json.load(file))
		activity_check_image(activity)
	except:
		print("Cannot read activity.json.")
	finally:
		if file is not None:
			file.close()
		return activity



def set_time(act):
	act["timestamps"] = {}
	act["timestamps"]["start"] = int(time.time() - time.clock_gettime(1))



def check_image(image):
	if not image in images:
		print(f"Image {image} not in images file.")
		return False
	return True



def activity_check_image(activity):
	ass: dict = activity["assets"]
	res = []
	if "small_image" in ass.keys() and not check_image(ass["small_image"]):
		res.append(ass["small_image"])
		del activity["assets"]["small_image"]
	if "large_image" in ass.keys() and not check_image(ass["large_image"]):
		res.append(ass["large_image"])
		del activity["assets"]["large_image"]
	
	if len(res) > 0:
		print(f"Image(s) {', '.join(res)} are removed.")
	


images = read_images()
activity = read_activity()
set_time(activity)


async def aloop(presence: Presence):
	i = 0
	last_time = time.time()
	update = {"assets": {}}
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
			
			case ["limage", image]:
				if check_image(image):
					update["assets"].update({"large_image": image})
					print(f"Large image is going to be \"{image}\".")
			
			case ["simage", image]:
				if check_image(image):
					update["assets"].update({"small_image": image})
					print(f"Small image is going to be \"{image}\".")
			
			case ["litext", *text]:
				text = ' '.join(text)
				update["assets"].update({"large_text": text})
				print(f"Large image text is going to be \"{text}\".")
			
			case ["sitext", *text]:
				text = ' '.join(text)
				update["assets"].update({"small_text": text})
				print(f"Small image text is going to be \"{text}\".")
			
			case ["update"]:
				if len(update["assets"]) < 1:
					del update["assets"]
				
				if len(update) < 1:
					print("There's nothing to update.")
					update.update({"assets": {}})
					continue
					
				time_passed = time.time() - last_time
				if time_passed < 15:
					print(f"Wait for {15 - time_passed:.1f} seconds to execute a command.")
					continue
				

				activity.update(update)
				presence.set(activity)
				update.clear()
				update.update({"assets": {}})
				last_time = time.time()
			
			case [*any]:
				print(f"Unknown command: " + ' '.join(any))
		
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