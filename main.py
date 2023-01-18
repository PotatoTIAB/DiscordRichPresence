try:
	from discordrp import Presence
	import time
	import os
	import asyncio
	import aioconsole as aio
	import json
	import os
except ModuleNotFoundError as error:
	print(f"Warning module \"{error.name}\" not found. Please install required modules to use.")
	exit(2)



path = os.path
CONFIG_PATH = os.path.dirname(__file__) + "/config/"
IMAGES_PATH = CONFIG_PATH + "images"
APP_ID_PATH = CONFIG_PATH + "app_id"
ACTIVITY_PATH = CONFIG_PATH + "activity.json"
APP_ID_TEMP = "[insert app id here]"
IMAGES_TEMP = "Here you can have image whitelist in case you accidentally try to set an image that doesn't exist."
ACTIVITY_TEMP = "{}"

helps = [
	"help: Shows this menu.",
	"exit: Quits program.",
	"toptext (text): Changes the first line.",
	"bottomtext (text): Changes the second line.",
	"limage (image): Switchs large image.",
	"simage (image): Switchs small image.",
	"litext (text): Changes hover text of large image",
	"sitext (text): Changes hover text of small image",
	"update: Commits all changes."
]



def check_folder():
	if path.exists(CONFIG_PATH):
		return True
	
	print("Config folder can't be found, creating a new one.")
	try:
		os.mkdir(CONFIG_PATH)
		os.mknod(IMAGES_PATH)
		os.mknod(APP_ID_PATH)
		os.mknod(ACTIVITY_PATH)
	except:
		print("Couldn't create the folder, make sure this file is not in a write protected folder.")
		exit(3)
	
	
	print("Created the folder, filling with templates.")
	
	imfile = None
	appfile = None
	actfile = None
	try:
		appfile = open(APP_ID_PATH, 'w')
		appfile.write(APP_ID_TEMP)
	except Exception as e:
		print("Error while generating in app_id template:\n" + str(e))
	finally:
		if appfile is not None:
			appfile.close()
	
	try:
		imfile = open(IMAGES_PATH, 'w')
		imfile.write(IMAGES_TEMP)
	except Exception as e:
		print("Error while generating in images template:\n" + str(e))
	finally:
		if imfile is not None:
			imfile.close()

	try:
		actfile = open(ACTIVITY_PATH, 'w')
		actfile.write(ACTIVITY_TEMP)
	except Exception as e:
		print("Error while generating in activity.json template:\n" + str(e))
	finally:
		if actfile is not None:
			actfile.close()
	

	print("Config generation done, remember to put your application id in 'app_id'.")
	return False



def read_images():
	file = None
	try:
		file = open(IMAGES_PATH)
		data = file.read()

		if data == IMAGES_TEMP:
			print("Template detected.")
			data = ""

		if data is not None and len(data) > 0:
			images = data.split()
		else:
			print("Warning, no images found. Make sure to check 'images' in config.")
			images = []
	except:
		print("Cannot read images file.")
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
		file = open(ACTIVITY_PATH)
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



def get_app_id():
	try:
		file = open(APP_ID_PATH)
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
	update = {"assets": {}}
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
				print(f"Unknown command: {' '.join(any)}\nType \"help\" for commands.")
		
	exit()

if not check_folder():
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
	print(e)
finally:
	if presence is not None:
		presence.close()
	
	if file is not None:
		file.close()