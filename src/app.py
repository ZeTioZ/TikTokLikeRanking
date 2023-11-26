import json

from flask import Flask, render_template
from threads.data_thread import DataThread

config_data = {}
app = Flask(__name__, template_folder="../templates", static_folder="../static")


def config_loader() -> dict:
	with open("resources/config.json", "r+") as json_file:
		config_dict = json.load(json_file)
		config_dict["channel"] = config_dict["channel"] if config_dict["channel"] != "" else input("Enter channel name: ")
		config_dict["list_size"] = config_dict["list_size"] if config_dict["list_size"] != 0 else int(input("Enter list size: "))
		config_dict["font_size"] = config_dict["font_size"] if config_dict["font_size"] != 0 else int(input("Enter font size: "))
		config_dict["font_color"] = config_dict["font_color"] if config_dict["font_color"] != "" else input("Enter font color: ")
		json_file.seek(0)
		json.dump(config_dict, json_file, indent=2)

		config_dict["load_cache"] = True if input("Load cache? (y/n): ").lower() == "y" else False
		if not config_dict["load_cache"]:
			with open("resources/like_cache.json", "w") as cache_file:
				cache_file.truncate(0)
			config_dict["cache"] = {}
		if config_dict["load_cache"]:
			print("Loading cache...")
			with open("resources/like_cache.json", "r", encoding="utf-8") as cache_file:
				read_file = cache_file.read()
				cache_dict = json.loads(read_file) if read_file != "" else {}
				config_dict["cache"] = cache_dict
	return config_dict


@app.route('/data')
async def data():
	return data_thread.to_string()


@app.route('/')
async def index():
	return render_template('like_ranking.html',
	                       channel=config_data["channel"],
	                       list_size=config_data["list_size"],
	                       font_size=config_data["font_size"],
	                       font_color=config_data["font_color"])


if __name__ == '__main__':
	config_data = config_loader()
	print(config_data)
	data_thread: DataThread = DataThread(config_data["channel"], config_data["list_size"], config_data["cache"])
	data_thread.start()
	app.run()
