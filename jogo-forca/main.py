# author: Rafael Muller Franco
# version: 1.5

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as C
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from random import choice
import data.lista

Window.clearcolor = 1,1,1,1
palavras = data.lista.aleatorias

kvcode = """
#: import C kivy.utils.get_color_from_hex
#: import FadeTransition kivy.uix.screenmanager.FadeTransition

<MyButton@Button>:
	font_size: "35sp"
	size_hint: (.4, .3)
	pos_hint: {'center_x':.5, 'center_y': .4}
	background_normal: ""
	background_color: C("#1E90FF")
	
ScreenManager:

	id: scr_manager	
	Inicio:
		name: 'inicio'
	Jogo:
		id: jogo
		name: 'jogo'
		
<Inicio>:
	
	BoxLayout:
		orientation: 'vertical'

		Image:
			source: "image/logo.png"
			pos_hint: {'center_x':.5, 'center_y':.5}
		MyButton:
			text:"Inicio"
			on_press: root.manager.current = "jogo"
			on_press: root.jogar()
		Label:
			text: "Autor: Rafael Muller Franco"
			color: C("#1E90FF")
			pos_hint: {'x':0, 'y':0}
			size_hint: 1,.1
		
<Jogo>:
	BoxLayout:
		orientation: 'vertical'

		ActionBar:
			id: menu
			background_image: 'image/normal.png'
			background_color: C("#1E90FF")
			pos_hint: {'top': 1}
			ActionView:
				use_separator: True
				ActionPrevious:
					title: "Jogo da Forca"
					with_previous: False
					app_icon: "image/icon.png"
				ActionOverflow:
				ActionButton:
					#icon: 
					text: "Reiniciar"
					on_release: root.sortear_palavra()
				ActionButton:
					text: "Sair"
					on_release: root.sair()
			
		Image:
			id: image
			source: "image/1.jpg"
			
		Label:
			text: root.lbl_tentativas
			halign: "center"
			valign: "middle"
			color: C("B22222")
			font_size: "25sp"
			size_hint: (1, .15)
			markup: True
			
		Label:
			text: root.lbl_certas
			halign: "center"
			valign: "middle"
			color: C("1E90FF")
			font_size: "40sp"
			size_hint: (1,.2)
			markup: True
			
		TextInput:
			id: txt_chute
			font_size: "40sp"
			size_hint: (.3, .2)
			pos_hint: {'center_x':.5, 'center_y':.5}
			multiline: False
			on_text_validate: root.chute()
			
		MyButton:
			id: bt_chute
			text: "Chute"
			on_release: root.chute()
			
		Label:
			size_hint: (.5, .1)
"""

# TELA DE INICIO
class Inicio(Screen):
	# Sorteia uma palavra e inicia o jogo
	def jogar(self):
		Jogo().sortear_palavra()
		self.manager.get_screen('jogo').lbl_certas = str((','.join(certas)).replace(',',' '))

# TELA DO JOGO
class Jogo(Screen):

	lbl_certas = StringProperty('')
	lbl_tentativas = StringProperty('Tentativas:')

	# Necessario para função mudar valor da label "certas".
	def __init__(self, *args, **kwargs):
		super(Jogo, self).__init__(*args, **kwargs)

	# Remover acentuação das palavras.
	def tratar_acentos(self,txt):

		s = []
		for letra in sorteio:
			if letra == 'Á' or letra == 'À' or letra == 'Ã':
				letra = 'A'
			elif letra == 'É' or letra == 'Ê':
				letra = 'E'
			elif letra == 'Í' or letra == 'Ì':
				letra = 'I'
			elif letra == 'Ó' or letra == 'Õ':
				letra = 'O'
			elif letra == 'Ú':
				letra = 'U'
			elif letra == 'Ç':
				letra = 'C'
			s.append(letra)
		return s
		
	# Realiza o sorteio da palavra
	def sortear_palavra(self):
		global palavra, certas, erros, sorteio, contador

		erros = ['Erros:\n']
		contador = -1
		# Voltar conf de inicio
		self.ids.bt_chute.background_color = C("#1E90FF")
		self.ids.menu.background_color = C("#1E90FF")
		self.ids.image.source = "image/1.jpg"
		
		# Sorteio e tratamento da palavra
		sorteio = choice(palavras).upper()
		palavra = self.tratar_acentos(sorteio)

		# Para cada letra na lista palavra adiciona "_"
		certas = ['_' for x in palavra]
		# Atualiza as labels para saber erros e acertos
		self.atualizar_label()

	# Letra do jogador
	def chute(self):
	
		chute = self.ids.txt_chute.text.upper()
		if chute != "":
			# Se a palavra possuir a letra substitui o "_"
			for letra in range(0, len(palavra)):
				if chute == palavra[letra]:
					certas[letra] = chute

			for letra in range(0, len(palavra)):
				if chute != palavra[letra]:
					# Se a letra não pertencer a certas
					if chute not in certas:
						# Se não é erro repetido
						if chute not in erros:
							erros.append(chute)
							self.trocar_imagem()

			self.ids.txt_chute.text = ""
			self.atualizar_label()

	# Atualiza as Labels para saber os erros e acertos
	def atualizar_label(self):
		global contador
		if contador <= 7:
			self.lbl_certas = str((','.join(certas)).replace(',',' '))
			self.lbl_tentativas = str((','.join(erros)).replace(',', ' '))

			# Condição de vitória
			if "_" not in certas:
				self.ids.image.source = "image/1.jpg"
				self.lbl_certas = '[color=008000]%s[/color]'%(sorteio)
				self.lbl_tentativas = '[color=008000]Você acertou![/color]'
				self.ids.bt_chute.background_color = C("#1E90FF")
				self.ids.menu.background_color = C("#1E90FF")
				
	# Troca a imagem do boneco
	def trocar_imagem(self):
		global contador

		imagens = [
			"image/2.jpg", "image/3.jpg", "image/4.jpg",
			"image/5.jpg", "image/6.jpg", "image/7.jpg", 
			"image/8.jpg"
		]
		cores = [
			"#1E90FF", "#1E90FF", "#4682B4", "#778899",
			"#808080", "#696969", "#000000", "#B22222"
		]
		
		contador += 1
		if contador == 7:
			self.lbl_certas = '[color=B22222]%s[/color]'%(sorteio)
			self.lbl_tentativas = '[color=B22222]Você perdeu![/color]'
		else:
			self.ids.image.source = imagens[contador]
			self.ids.bt_chute.background_color = C(cores[contador])
			self.ids.menu.background_color = C(cores[contador])
			
	# Fecha o programa
	def sair(self):
		App.get_running_app().stop()

class ForcaApp(App):

	def build(self):
		main_widget = Builder.load_string(kvcode)
		return main_widget

if __name__ == '__main__':
	ForcaApp().run()
