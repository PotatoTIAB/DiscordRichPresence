try:
	from discordrp import Presence
	import time
	import os
	import asyncio
	import aioconsole as aio
	import json
except ModuleNotFoundError as error:
	print(f"Warning module \"{error.name}\" not found. Please install required modules to use.")
	exit(2)


helps = [
	"help: Shows this menu.",
	"exit: Quits program.",
	"toptext (text): Changes the first line.",
	"bottomtext (text): Changes the second line.",
	"limage (image): Switchs large image.",
	"simage (image): Switchs small image.",
	"litext (text): Changes hover text of large image",
	"sitext (text): Changes hover text of small image",
	"update: Commits all changes.",
	"save: Saves current activity to 'activity.json'."
]


def read_images():
	file = None
	try:
		file = open(os.path.dirname(__file__) + "/config/images")
		data = file.read()
		if data is not None and len(data) > 0:
			images = data.split()
		else:
			print("Warning, no images found. Make sure to check 'images' in config.")
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
		file = open(os.path.dirname(__file__) + "/config/activity.json")
		activity.update(json.load(file))
		activity_check_image(activity)
	except:
		print("Cannot read activity.json.")
	finally:
		if file is not None:
			file.close()
		return activity


def write_activity(act):
	act = act.copy()
	file = None
	success = False
	del act["timestamps"]
	try:
		file = open(os.path.dirname(__file__) + "/config/activity.json", 'w')
		json.dump(act, file, indent=4, sort_keys=True)
		success = True
	finally:
		if file is not None:
			file.close()
		return success



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



def get_app_id():
	try:
		file = open(os.path.dirname(__file__) + "/config/app_id")
	except FileNotFoundError:
		print("Warning \"app_id\" not found, please create one in the same folder with \"main.py\".")
		return ""
	
	presence_id = file.readline()


	if presence_id == "":
		print("Warning empty string in \"app_id\" detected.")
		return ""


	if presence_id[-1] == '\n':
		presence_id = presence_id.strip('\n')


	if presence_id == "[insert app id here]":
		print("Please insert your app id to file \"app_id\".")
		return ""


	if not presence_id.isdigit():
		print("Your app id must only consist from digits.")
		return ""
	

	return presence_id


async def aloop(presence: Presence):
	i = 0
	last_time = time.time()
	update = {}
	assets = {}
	while True:
		inp = await aio.ainput(">> ")
		match inp.split():
			case ["exit"]:
				print("Exiting...")
				break

			case["help"]:
				for line in helps:
					print(line)
			
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
					assets.update({"large_image": image})
					print(f"Large image is going to be \"{image}\".")
			
			case ["simage", image]:
				if check_image(image):
					assets.update({"small_image": image})
					print(f"Small image is going to be \"{image}\".")
			
			case ["litext", *text]:
				text = ' '.join(text)
				assets.update({"large_text": text})
				print(f"Large image text is going to be \"{text}\".")
			
			case ["sitext", *text]:
				text = ' '.join(text)
				assets.update({"small_text": text})
				print(f"Small image text is going to be \"{text}\".")
			
			case ["update"]:
				if len(update) < 1 and len(assets) < 1:
					print("There's nothing to update.")
					continue
					
				time_passed = time.time() - last_time
				if time_passed < 15:
					print(f"Wait for {15 - time_passed:.1f} seconds to execute a command.")
					continue
				

				activity.update(update)
				activity["assets"].update(assets)
				presence.set(activity)
				update.clear()
				last_time = time.time()
			
			case ["save"]:
				if write_activity(activity):
					print("Saved successfully!")
				else:
					print("Saving failed.")
			
			case [*any]:
				print(f"Unknown command: {' '.join(any)}\nType \"help\" for commands.")
		
	exit()


images = read_images()
activity = read_activity()
set_time(activity)


presence = None
file = None
try:
	presence_id = get_app_id()
	if presence_id == "":
		print("App id is not valid. Exiting...")
		exit(1)

	presence = Presence(presence_id)
	presence.set(activity)

	asyncio.run(aloop(presence))
	

except Exception as e:
	raise e
finally:
	if presence is not None:
		presence.close()
	
	if file is not None:
		file.close()