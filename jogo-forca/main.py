# author: Rafael Muller Franco
# version: 1.0

import kivy
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from unicodedata import normalize
from random import choice
import data.lista

kivy.require('1.9.1')
palavras = data.lista.aleatorias

# GERENCIADOR DE TELAS
class ScreenManager(ScreenManager):
	pass

# TELA DE INICIO
class Inicio(Screen):
	# SORTEIA UMA PALAVRA, CHAMA A TELA DO JOGO
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
		return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

	# Realiza o sorteio da palavra
	def sortear_palavra(self):

		global palavra, certas, erros, sorteio, contador
		palavra = []
		certas = []
		erros = ['Erros:\n']
		contador = 1

		sorteio = choice(palavras).upper()
		escolha = self.tratar_acentos(sorteio)

		# Adiciona cada letra na lista palavra
		for letra in escolha:
			palavra.append(letra)

		# Para cada letra na lista palavra adiciona "_"
		for letra in range(0, len(palavra)):
			certas.append("_")

		# Inicia com a imagem da forca vazia
		self.ids.image.source = "image/1.jpg"
		# Atualiza as labels
		self.atualizar_label()

	# Letra do jogador
	def chute(self):

		chute = self.ids.txt_chute.text.upper()
		# Se a palavra possuir a letra substitui o "_"
		for letra in range(0, len(palavra)):
			if chute == palavra[letra]:
				certas[letra] = chute
		# Substituir por elif, mesmo efeito
		for letra in range(0, len(palavra)):
			if chute != palavra[letra]:
				# Se a letra não pertencer a certas
				if chute not in certas:
					# Se não é erro repetido
					if chute not in erros:
						erros.append(chute)
						self.trocar_imagem()

		self.ids.txt_chute.text = ""
		self.ids.txt_chute.focus = True
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

	# Troca a imagem do boneco
	def trocar_imagem(self):
		global contador
		if contador == 1:
			self.ids.image.source = "image/2.jpg"
		elif contador == 2:
			self.ids.image.source = "image/3.jpg"
		elif contador == 3:
			self.ids.image.source = "image/4.jpg"
		elif contador == 4:
			self.ids.image.source = "image/5.jpg"
		elif contador == 5:
			self.ids.image.source = "image/6.jpg"
		elif contador == 6:
			self.ids.image.source = "image/7.jpg"
		elif contador == 7:
			self.ids.image.source = "image/8.jpg"
			self.lbl_certas = '[color=B22222]%s[/color]'%(sorteio)
			self.lbl_tentativas = '[color=B22222]Você perdeu![/color]'
		contador += 1

	# Fecha o programa
	def sair(self):
		App.get_running_app().stop()

class ForcaApp(App):
	def build(self):
		return ScreenManager()

if __name__ == '__main__':
	ForcaApp().run()