# author: Rafael Muller Franco
# version: 1.7 - dev
# duvida: uma vez que limpe os dados, os BDs sao excluidos
# duvida: caso nao, os dados sao resetados ja que modifiquei no decorrer

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as C
from kivy.properties import StringProperty, ListProperty,DictProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from random import choice
import data.lista

import json
from kivy.storage.jsonstore import JsonStore as JS

store = JS('banco.json')

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

<MyActionBar@ActionBar>:
	background_image: 'image/normal.png'
	background_color: C("#1E90FF")
	pos_hint: {'top': 1}		

ScreenManager:

	id: scr_manager	
	Inicio:
		name: 'inicio'
	Jogo:
		name: 'jogo'
	Loja:
		name: 'loja'
		
<Inicio>:
	
	BoxLayout:
		orientation: 'vertical'

		Image:
			source: "image/logo.png"
			pos_hint: {'center_x':.5, 'center_y':.5}

		MyButton:
			text:"Inicio"
			on_press: root.jogar()

		Label:
			text: "Autor: Rafael Muller Franco"
			color: C("#1E90FF")
			pos_hint: {'x':0, 'y':0}
			size_hint: 1,.1

<Jogo>:
	on_enter: root.sortear_palavra()
	BoxLayout:
		orientation: 'vertical'

		MyActionBar
			id: menu
			ActionView:
				use_separator: True
				ActionPrevious:
					title: "Jogo da Forca"
					with_previous: False
					app_icon: "image/icon.png"
					on_press: root.manager.current='inicio'
				ActionOverflow:
				ActionButton:
					#text:  root.pontos
					text:  "Loja"
					on_press: root.abrir_loja()
				ActionButton:
					#icon: 
					text: "Reiniciar"
					on_release: root.sortear_palavra()
				ActionButton:
					text: "Sair"
					on_release: root.sair()

		Image:
			id: image
			#source: "image/1.jpg"

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


<MinhaTabela@BoxLayout>:
	orientation: 'horizontal'
	l1: ''
	l2: ''
	l3: 'base'
	spacing: 5
	padding: 15

	Image:
		source: root.l1

	Button:
		id: btn_compra
		text: "Custo: " + root.l2
		on_press: root.parent.parent.parent.parent.parent.parent.saveData('splash', root.l3)
		background_normal: ""
		background_color: C("1E90FF")
	
<Loja>:
	BoxLayout:
		orientation: 'vertical'
		
		MyActionBar:
			id: menu_loja
			ActionView:
				use_separator: True
				ActionPrevious:
					title: "Jogo da Forca"
					with_previous: False
					app_icon: "image/icon.png"
				ActionOverflow:
				ActionButton:
					text:  "Pontos: " + root.pontos

				ActionButton:
					text: "Voltar"
					on_release: root.voltar()

		Label:
			text: "LOJA"
			size_hint_y: .15
			color: C("1E90FF")

		ScrollView:
			BoxLayout:
				id: box
				orientation: 'horizontal'
				
				RecycleView:
					id: rv_func
					data: [{'l1':x,'l2':y,'l3':z}for x,y,z in root.catalogo]
					viewclass: 'MinhaTabela'
					RecycleBoxLayout:
						default_size: None, dp(180)
						default_size_hint: 1, None
						size_hint_y: None
						height: self.minimum_height
						orientation: 'vertical'
		
			#GridLayout:
			#	cols: 2
				#Image:
				#	source: 'image/base/7.jpg'
				#Button:
				#	text: "Base"
				#	on_press: root.saveData('splash','base')
				#Image:
				#	source: 'image/um/7.jpg'
				#Button:
				#	text: "Um"
				#	on_press: root.saveData('splash','um')


"""

import sys, os
def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
	#	return os.path.join(sys._MEIPASS, relative_path)
		return os.path.join(sys._MEIPASS)
	#return os.path.join(os.path.abspath("."), relative_path)
	return os.path.join(os.path.abspath("."))

# resource_path('data/lista.py')
# resource_path('image/base/')
# resource_path('image/um/')
# resource_path('image/')
# resource_path('image/logo.png')
# resource_path('image/normal.png')
# resource_path('image/splash.jpg')
# resource_path('banco.json')



global imagens
bas_imagens = [
	"2.jpg", "3.jpg", "4.jpg",
	"5.jpg", "6.jpg", "7.jpg", 
	"8.jpg"
]
imagens = [x for x in bas_imagens]

# TELA DE INICIO
class Inicio(Screen):
	# Sorteia uma palavra e inicia o jogo
	def jogar(self):
		self.manager.current = "jogo"
		certas = 'Chute uma letra:'
		self.manager.get_screen('jogo').lbl_certas = str((','.join(certas)).replace(',',' '))
		self.manager.get_screen('jogo').ids.image.source = 'image/'+store['jogador']['splash']+'/1.jpg'
		
# TELA DO JOGO
class Jogo(Screen):

	path_splash = StringProperty('base')
	pontos = StringProperty('')
	data = DictProperty({})
	lbl_certas = StringProperty('')
	lbl_tentativas = StringProperty('Tentativas:')

	# Necessario para função mudar valor da label "certas".
	def __init__(self, *args, **kwargs):
		super(Jogo, self).__init__(*args, **kwargs)
		self.path_splash = store['jogador']['splash']+"/"

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
		contador = 0
		# Voltar conf de inicio
		self.ids.bt_chute.background_color = C("#1E90FF")
		self.ids.menu.background_color = C("#1E90FF")
		self.ids.image.source = 'image/'+self.path_splash+"1.jpg"

		# Sorteio e tratamento da palavra
		sorteio = choice(palavras).upper()
		palavra = self.tratar_acentos(sorteio)

		# Para cada letra na lista palavra adiciona "_"
		certas = ['_' for x in palavra]
		# Atualiza as labels para saber erros e acertos
		self.atualizar_label()
		self.loadData()

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
		if contador <= 6:
			self.lbl_certas = str((','.join(certas)).replace(',',' '))
			self.lbl_tentativas = str((','.join(erros)).replace(',', ' '))

			# Condição de vitória
			if "_" not in certas:
				self.ids.image.source = 'image/'+self.path_splash+"1.jpg"
				self.lbl_certas = '[color=008000]%s[/color]'%(sorteio)
				self.lbl_tentativas = '[color=008000]Você acertou![/color]'
				self.ids.bt_chute.background_color = C("#1E90FF")
				self.ids.menu.background_color = C("#1E90FF")
				self.saveData('vitoria')
				
	# Troca a imagem do boneco
	def trocar_imagem(self):
		global imagens
		cores = [
			"#1E90FF", "#1E90FF", "#4682B4", "#778899",
			"#808080", "#696969", "#000000"
		]
		global contador
		
		if contador == 6:
			self.ids.image.source = imagens[contador]
			self.ids.menu.background_color = C(cores[contador])
			self.lbl_certas = '[color=B22222]%s[/color]'%(sorteio)
			self.lbl_tentativas = '[color=B22222]Você perdeu![/color]'
		elif contador <= 6:
			self.ids.image.source = imagens[contador]
			self.ids.bt_chute.background_color = C(cores[contador])
			self.ids.menu.background_color = C(cores[contador])
		contador += 1

	def selecionar_imagem(self, splash):

		global imagens, bas_imagens
		if splash == 'um':
			self.path_splash = 'um/'
		else:
			self.path_splash = 'base/'

		c = 0
		for x in bas_imagens:
			imagens[c] = 'image/'+self.path_splash + x
			c += 1

	def loadData(self):
		self.data = store['jogador']
		self.selecionar_imagem(self.data['splash'])
	
	def saveData(self, condicao):
		#self.pontos = "Pontos "+str(self.data['pontos'])
		try:
			if condicao == 'vitoria':
				self.data['pontos'] += 1
				store['jogador'] = self.data
		except:
			print("Erro Func saveData()")
			pass

	# Fecha o programa
	def sair(self):
		App.get_running_app().stop()

	def abrir_loja(self):
		#self.ids.imagem.source = 'image/'+self.path_splash+"1.jpg"
		self.manager.current='loja'	

class Loja(Screen):

	dados = DictProperty({})
	data = DictProperty({})
	pontos = StringProperty('')
	catalogo = ListProperty([])

	def __init__(self, *args, **kwargs):
		super(Loja, self).__init__(*args, **kwargs)
		self.loadData()

	def saveData(self, condicao, variavel):

		valor = store['loja'][variavel][1]
		if int(self.pontos) >= int(valor):
			npontos = int(self.pontos) - int(valor)
			self.pontos = str(npontos)
			store['loja'][variavel][1] = '0'
			store['jogador']['pontos'] = self.pontos
			self.loadData()
		# armazenar splash atual
		self.data = store['jogador']
		self.data['splash'] = variavel
		# self.data[condicao] = variavel
		# salva no banco de dados
		store['jogador'] = self.data

	def loadData(self):

		# evita carregar em duplicidade
		self.catalogo = []
		# carregar dados loja
		self.dados = store['loja']
		for x in self.dados:
			self.catalogo.append(self.dados[x])

		# carregar dados salvos jogador 
		self.data = store['jogador']
		self.pontos = str(self.data['pontos'])

	def voltar(self):
		self.manager.current = 'inicio'
		self.manager.get_screen('jogo').path_splash = self.data['splash']
	
class ForcaApp(App):

	def build(self):
		main_widget = Builder.load_string(kvcode)
		return main_widget

if __name__ == '__main__':
	kivy.resources.resource_add_path(resourcePath())
	ForcaApp().run()
