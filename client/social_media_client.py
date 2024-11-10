from abc import ABC, abstractmethod

class SocialMediaClient(ABC):
	@abstractmethod
	def init(self):
		pass


	@abstractmethod
	def create_session(self):
		pass

	@abstractmethod
	def publish(self, post, reply_post_id="", root_post_id=""):
		pass
