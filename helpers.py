# imports for helper functions
import asyncio
import websockets
from subprocess import Popen, PIPE

class Helpers:
	"""Helper functions"""
	def round_backlight_value(self, current_value: str, step: int = 5) -> str:
		"""Round the current_value to nearest lower value, according to step."""
		current_value = int(current_value)
		rounded_value = str(current_value - (current_value%step))
		return rounded_value
	
	def backlight_check(self):
		"""We get the current backlight value, then we check if the value can be divided by step (if not, we round it and set rounded value)"""
		ask_ddcutil = Popen(['ddcutil', 'get', '10', '--terse', '--sleep-multiplier', str('.03')], stdout=PIPE, stderr=PIPE)
		stdout, stderr = ask_ddcutil.communicate()
		backlight = stdout.decode().split()[3]
		rounded_backlight = self.round_backlight_value(backlight, self.step)
		if backlight != rounded_backlight:
			backlight = rounded_backlight
			asyncio.run(self.send_backlight(backlight))
		return backlight
	
	# async helpers
	async def send_backlight(self, value):
		"""Corutine to send backlight value to websocket server (if websocket server recieve value, it will set the value directly over ddcutil)"""
		async with websockets.connect(self.ws_server) as websocket:
			await websocket.send(value)
			#await websocket.recv()
		