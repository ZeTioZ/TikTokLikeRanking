import json

from threading import Thread
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import LikeEvent


class DataThread(Thread):
	def __init__(self, channel, list_size, use_cache=False, cached_data=None):
		Thread.__init__(self)
		self.daemon = True
		self.channel = channel
		self.use_cache = use_cache
		self.list_size = list_size
		self.client = TikTokLiveClient(unique_id=channel)
		self.like_map = cached_data if cached_data is not None else {}

	def run(self):
		print(f"Like ranking started for {self.channel}'s live!")
		self.add_listeners()
		self.client.run()

	def update_ranking(self):
		self.like_map = dict(sorted(self.like_map.items(), key=lambda x: x[1], reverse=True))
		if self.use_cache:
			with open("resources/like_cache.json", "w", encoding="utf-8") as cache_file:
				json.dump(self.like_map, cache_file, ensure_ascii=False)

	def to_string(self):
		return "<br>".join([f"{user}: {self.like_map[user]}" for user in self.like_map.keys()][:self.list_size]).encode("utf8")

	def on_like(self, event: LikeEvent):
		self.like_map[event.user.nickname] = self.like_map.get(event.user.nickname, 0) + event.likes
		self.update_ranking()

	def add_listeners(self):
		self.client.add_listener("like", self.on_like)
