from kivy.app import App
from kivy.lang import Builder

kvcode = """
FloatLayout:

	Image:
		source: 'logo.png'
	Image:
		source: 'icon.png'
"""
class AplicativoTeste(App):
	def build(self):
		main_widget = Builder.load_string(kvcode)
		return main_widget
AplicativoTeste().run()