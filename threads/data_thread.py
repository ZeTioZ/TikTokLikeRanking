import json

from threading import Thread

from TikTokLive.client.client import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError, UserNotFoundError
from TikTokLive.events import LikeEvent


class DataThread(Thread):
	def __init__(self, channel, list_size, cached_data=None):
		Thread.__init__(self)
		self.daemon = True
		self.channel = channel
		self.list_size = list_size
		self.client = TikTokLiveClient(unique_id=channel)
		self.like_map = cached_data if cached_data is not None else {}

	def run(self):
		print(f"Like ranking started for {self.channel}'s live!")
		self.add_listeners()
		try:
			self.client.run()
		except UserOfflineError:
			print(f"{self.channel} is offline. Exiting...")
		except UserNotFoundError:
			print(f"{self.channel} not found or not live enabled. Exiting...")

	def update_ranking(self):
		self.like_map = dict(sorted(self.like_map.items(), key=lambda x: x[1], reverse=True))
		with open("resources/like_cache.json", "w", encoding="utf-8") as cache_file:
			json.dump(self.like_map, cache_file, ensure_ascii=False)

	def to_string(self):
		return "<br>".join([f"{user}: {self.like_map[user]}" for user in self.like_map.keys()][:self.list_size]).encode("utf8")

	def on_like(self, event: LikeEvent):
		self.like_map[event.user.nickname] = self.like_map.get(event.user.nickname, 0) + event.count
		self.update_ranking()

	def add_listeners(self):
		self.client.add_listener(LikeEvent, self.on_like)
