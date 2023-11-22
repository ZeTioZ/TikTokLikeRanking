from flask import Flask, render_template
from data_thread import DataThread

channel: str = input("Enter the channel name:\n")
font_size: int = int(input("Enter the font size:\n"))
font_color: str = input("Enter the font color:\n")
list_size: int = int(input("Enter the list size:\n"))
app = Flask(__name__)


@app.route('/data')
async def data():
	return data_thread.to_string()


@app.route('/')
async def index():
	return render_template('like_ranking.html', channel=channel, list_size=list_size, font_size=font_size, font_color=font_color)


if __name__ == '__main__':
	data_thread: DataThread = DataThread(channel, list_size)
	data_thread.start()
	app.run()
