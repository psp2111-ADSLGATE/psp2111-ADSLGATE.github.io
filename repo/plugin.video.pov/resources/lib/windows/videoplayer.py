from windows import BaseDialog
# from modules.kodi_utils import logger

class VideoPlayer(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.video = kwargs['video']

	def onInit(self):
		self.player.play(self.video, windowed=True)
		self.monitor()

	def run(self):
		self.doModal()

	def onAction(self, action, controlID=None):
		if action in self.closing_actions:
			self.player.stop()
			self.exit()

	def monitor(self):
		while not self.player.isPlayingVideo(): self.sleep(1000)
		while self.player.isPlayingVideo(): self.sleep(1000)
		self.exit()

	def exit(self):
		self.sleep(500)
		self.close()

