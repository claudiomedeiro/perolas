#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
- Dado um .txt com reflexões/quotations, sorteia um aleatório para o dia, 
permite pesquisar e inserir novos.
"""
__author__ = "Claudio Jorge Severo Medeiro"
__email__ = "cjinfo@gmail.com"

from time import sleep
from random import randint
from datetime import datetime
from os import system
from json import load, dumps

str_arquivo = 'perolas.txt'
str_arquivo_calendario = 'sorteadas.json'
dic_calendario = {}

def le_arquivo(str_arquivo):
	"""
	Dado o nome do arquivo, abre e devolve seu conteudo em uma lista de linhas

	>>> le_arquivo("perolas.txt")
	['Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)\\n', 'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)\\n', 'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)\\n', 'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)']
	"""
	try:
		with open(str_arquivo, 'r', encoding="utf8") as fil_perolas:
			vet_perolas = fil_perolas.readlines()
			fil_perolas.close()
	except:
		vet_perolas = []
		print("Arquivo '{}' nao encontrado.".format(str_arquivo))	
		sleep(2)

	return(vet_perolas)

def sorteia_perola():
	"""
	Abre o .txt, conta o numero de quotations, e sorteia uma delas para ser a reflexao do dia

	>>> sorteia_perola()
	'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)'
	"""
	global str_arquivo
	vet_perolas = le_arquivo(str_arquivo)
	if len(vet_perolas) > 0:
		int_random = randint(0, len(vet_perolas)-1)
		str_perola = vet_perolas[int_random].rstrip()
	else:
		str_perola = ""

	return(str_perola)

def perola_do_dia():
	"""
	- Identifica se já foi sorteada uma reflexão/pérola para o dia, e do contrário, 
	sorteia uma, e grava no arquivo. Nos dois casos devolve-a.
	"""
	global str_arquivo_calendario
	global dic_calendario

	try:
		dic_calendario = abre_json(str_arquivo_calendario)
	except:
		dic_calendario = {}
	
	if datetime.now().strftime("%Y-%m-%d") not in dic_calendario.keys():
		dic_calendario[datetime.now().strftime("%Y-%m-%d")] = sorteia_perola().replace("\"","'")
		grava_json(str_arquivo_calendario, dic_calendario)

	return(dic_calendario[datetime.now().strftime("%Y-%m-%d")])

def acrescenta_perola():
	"""
	- Solicita um texto a ser acrescentado ao banco de pérolas, exibe-o na tela, 
	pedindo confirmação, e em caso positivo acrescenta-o ao arquivo/base de dados.
	"""
	global str_arquivo
	str_texto = ""
	while True:
		system('clear') or None
		if not str_texto.rstrip() == "":
			print("Texto que você digitou: " + str_texto)
			str_funcao = aceitar_so_numeros('1 (Confirma) ou 9 (Cancelar): ')
			if int(str_funcao) == 1:
				grava_arquivo(str_arquivo, "\n"+str_texto.replace('"', "'"))
				print("Texto acrescentado ao arquivo de pérolas")
				sleep(2)
				break
			elif int(str_funcao) == 9:
				break
			else:
				print("Você precisa escolher uma das opções listadas")
				sleep(2)
		else:
			str_texto = str(input("Digite a perola: "))

def grava_arquivo(str_arquivo, str_texto, sModo='a'):
	"""
	Dado o nome de um arquivo, e um texto, acrescenta o texto ao final do arquivo
	>>> acrescentaAoArquivo("perolas.txt","texto acrescentado","a")
	"""
	try:
		with open(str_arquivo, sModo, encoding="utf8") as fil_perolas:
			fil_perolas.write(str_texto)
			fil_perolas.close()

	except FileNotFoundError:
		print("Problemas ao tentar gravar no arquivo '" + str_arquivo + "'.")	

	return

def abre_json(str_arquivo):
	"""
	- Recebe uma string com o nome do arquivo, abre o arquivo, e coloca em um 
	dicionário em que cada posicao eh uma linha.
	- Retorna no vetor e o último elemento tem um barra que depois precisa ser 
	tirado em cada processo especifico.
	"""
	try:
		with open(str_arquivo, 'r') as fil_arquivo:
			dic_arquivo = load(fil_arquivo)
			fil_arquivo.close()
	except IOError:
		dic_arquivo = {}

	return dic_arquivo

def grava_json(str_arquivo, dic_texto):
	"""
	Decebe um nome de arquivo e um dicionário, e grava esse dicionário no arquivo.
	"""
	try:
		open(str_arquivo,'w').write(dumps(dic_texto))
	except:
		pass
		print("Problemas ao tentar gravar no arquivo '{}'".format(str_arquivo)	)
	return

def aceitar_so_numeros(str_texto):
	"""
	Dado um texto, verifica se eh um numero, do contrario repete o pedido de digitacao
	"""
	while True:
		try:
			str_valor = str(input(str_texto))
			if not str_valor.replace(",",".").replace(".","").isdigit():
				raise ValueError(str_valor)
		except ValueError as e:
			print("Valor invalido:", e)
		else:
			break

	return str_valor.replace(",",".")

def reseta_perola_do_dia():
	"""
	Exclui a entrada do arquivo para o dia de hoje e coloca nova pérola no lugar.
	"""
	global dic_calendario
	
	if datetime.now().strftime("%Y-%m-%d") in dic_calendario.keys():
		dic_calendario.pop(datetime.now().strftime("%Y-%m-%d"))
		grava_json(str_arquivo_calendario, dic_calendario)
	
	return(perola_do_dia())

def palavras_mais_comuns(int_qtde=5):
	"""
		Percorre toda a base de pérolas, conta as ocorrências de cada palavra 
	com 04 ou mais caracteres, ordena decrescente pela quantidade de ocorrências
	e devolve uma string com as X (05 por default) maiores ocorrências.
	"""
	dic_perolas = {}
	vet_perolas = le_arquivo(str_arquivo)
	for perola in vet_perolas:
		vet_palavras = perola.split(' ')
		for str_palavra in vet_palavras:
			if (len(str_palavra.replace(' ','')) >= 4) and (not str_palavra.replace(' ','').isdigit()):
				if str_palavra in dic_perolas:
					dic_perolas[str_palavra] += 1
				else:
					dic_perolas[str_palavra]  = 1

	vet_quantidades = []
	vet_quantidades += dic_perolas.values()
	vet_quantidades.sort()
	vet_quantidades = vet_quantidades[::-1]
	vet_qtde = vet_quantidades[:int_qtde]
	str_palavras_mais_comuns = ""
	for int_cont in vet_qtde:
		str_palavras_mais_comuns += list(dic_perolas.keys())[list(dic_perolas.values()).index(int_cont)] + " "
		dic_perolas.pop(list(dic_perolas.keys())[list(dic_perolas.values()).index(int_cont)])

	return(str_palavras_mais_comuns)

def pesquisar_perola():
	"""
	Exibe as palavras mais comuns da base de dados, e questiona termos de busca
	"""
	global str_arquivo
	str_texto = ""
	while True:
		system('clear') or None
		print("Palavras mais comuns nas perolas cadastradas: {}\n".format(palavras_mais_comuns()))
		
		if str_texto.replace(' ', '').strip() == '9':
			break
		elif not len(str_texto.replace(' ', '').strip()) < 3:
			print("Texto que você digitou: " + str_texto)
			str_funcao = aceitar_so_numeros('1 (Confirma) ou 9 (Cancelar): ')
			if int(str_funcao) == 1:
				vet_perolas = le_arquivo(str_arquivo)
				int_cont = 0
				for perola in vet_perolas:	
					if str_texto in perola:
						int_cont+=1
						if int_cont == 1:
							print("Perola(s) encontrada(s) com os termos da sua pesquisa: '" + str_texto + "'\n")

						print((3-len(str(int_cont)))*'0'+str(int_cont))
						print(perola)
				
				if int_cont > 0:
					input("Pressione ENTER para sair: ")
					break
				else:
					print("Nao tem nenhuma perola com o texto que você digitou: '" + str_texto + "'")
					print("Voltando para a tela inicial")
					sleep(2)
					break
			elif int(str_funcao) == 9:
				break
			else:
				print("Você precisa escolhar uma das opcoes listadas")
				sleep(2)
		else:
			str_texto = str(input("Digite os termos da pesquisa (minimo 03 letras) ou 9 para sair: "))

def main():
	"""
	Aqui é o corpo principal do perolas.py
	
	01) Ao carregar vai exibir a perola do dia
	02) Vai exibir as opcoes que o usuario tem, quais sejam:
		a) resetar a perola do dia (vai rodar novamente o processo de escolha da perola do dia, e desprezar a escolha anterior)
		b) acrescentar perola
		c) pesquisar
		d) sair do programa
		
	>>> main()
	Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)
	Funcoes:
	1 Resetar a perola do dia
	2 Acrescentar texto aa relacao de perolas
	3 Pesquisar perolas
	9 Sair do programa	
	Digite o numero da funcao desejada:
	"""
	while True:
		system('clear') or None
		print("{}\n".format(perola_do_dia()))
		print('Funções:')
		print('1 Pesquisar pérolas')
		print('2 Acrescentar texto aa relação de pérolas')
		print('3 Resetar a pérola do dia')
		print('9 Sair do programa')
		str_funcao = aceitar_so_numeros('Digite o número da função desejada: ')
		if int(str_funcao) == 3:
			reseta_perola_do_dia()
		elif int(str_funcao) == 2:
			acrescenta_perola()
		elif int(str_funcao) == 1:
			pesquisar_perola()
			pass
		elif int(str_funcao) == 9:
			print("Obrigado por usar o aplicativo! Até logo!")
			break
		else:
			print("Você precisa escolhar uma das opções listadas")
			sleep(2)

	return

def _test():
	"""
	Executa os testes dos metodos que tem DOCTESTS
	"""
	import doctest, perolas
	return doctest.testmod(perolas)

if __name__ == "__main__":
	# _test()
	main()