#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Dado um .txt com reflexões/quotations, sorteia um aleatório para o dia, permite 
pesquisar e inserir novos.
"""
__author__ = "Claudio Jorge Severo Medeiro"
__email__ = "cjinfo@gmail.com"

from time import sleep
from random import randint
from datetime import datetime
import os

sArquivo = 'perolas.txt'
sArquivoCalendario = 'calendario.txt'

def leArquivo(sArquivo):
	"""
	Dado o nome de um arquivo, abre e devolve seu conteudo em uma lista de linhas

	>>> leArquivo("perolas.txt")
	['Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)\\n', 'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)\\n', 'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)\\n', 'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)']
	"""
	try:
		with open(sArquivo, 'r', encoding="utf8") as fPerolas:
			vetPerolas = fPerolas.readlines()
			fPerolas.close()
	except:
		vetPerolas = []
		print("Arquivo '{}' nao encontrado.".format(sArquivo))	
		sleep(2)

	return(vetPerolas)

def sorteiaPerola():
	"""
	Abre o .txt, conta o numero de quotations, e sorteia uma delas para ser a reflexao do dia

	>>> sorteiaPerola()
	'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)'
	"""
	global sArquivo
	vetPerolas = leArquivo(sArquivo)
	if len(vetPerolas) > 0:
		iRandom = randint(0, len(vetPerolas)-1)
		sPerola = vetPerolas[iRandom].rstrip()
	else:
		sPerola = ""

	return(sPerola)

def perolaDoDia():
	"""
	Identifica se ja nao foi sorteada uma perola para o dia e a exibe, do contrario, invoca o sorteiaPerola e grava a resultante como a perola do dia

	>>> perolaDoDia()
	'Comedimento no Comer e no Beber, Modo de Vida Aristocratico, e Serenidade expressa pela Consciencia, Presenca e Generosidade (Reflexoes Pitagoricas)'
	"""
	global sArquivo
	global sArquivoCalendario

	vetCalendario = leArquivo(sArquivoCalendario)
	
	sPerola = ""
	for lCalendario in vetCalendario:	#procura pelo do dia de hoje
		if lCalendario.split("|")[0] == datetime.now().strftime("%Y-%m-%d"):
			sPerola = lCalendario.split("|")[1]
			break

	if sPerola == "":
		sPerola = sorteiaPerola()
		if not sPerola == "":
			sTexto = datetime.now().strftime("%Y-%m-%d") + "|" + sPerola + "\n"			
			gravaArquivo(sArquivoCalendario, sTexto)
	
	return(sPerola.rstrip())

def acrescentaPerola():
	"""
		Solicita um texto a ser acrescentado ao banco de pérolas, exibe-o na tela, 
	pedindo confirmação, e em caso positivo acrescenta-o ao arquivo/base de dados.
	"""
	global sArquivo
	sTexto = ""
	while True:
		os.system('clear') or None
		if not sTexto.rstrip() == "":
			print("Texto que você digitou: " + sTexto)
			sFuncao = aceitarSoNumeros('1 (Confirma) ou 9 (Cancelar): ')
			if int(sFuncao) == 1:
				gravaArquivo(sArquivo, "\n"+sTexto.replace('"', "'"))
				print("Texto acrescentado ao arquivo de pérolas")
				sleep(2)
				break
			elif int(sFuncao) == 9:
				break
			else:
				print("Você precisa escolher uma das opções listadas")
				sleep(2)
		else:
			sTexto = str(input("Digite a perola: "))

def gravaArquivo(sArquivo, sTexto, sModo='a'):
	"""
	Dado o nome de um arquivo, e um texto, acrescenta o texto ao final do arquivo
	>>> acrescentaAoArquivo("perolas.txt","texto acrescentado","a")
	"""
	try:
		with open(sArquivo, sModo, encoding="utf8") as fPerolas:
			fPerolas.write(sTexto)
			fPerolas.close()

	except FileNotFoundError:
		print("Problemas ao tentar gravar no arquivo '" + sArquivo + "'.")	

	return

def aceitarSoNumeros(sTexto):
	"""
	Dado um texto, verifica se eh um numero, do contrario repete o pedido de digitacao
	"""
	while True:
		try:
		    sValor = str(input(sTexto))
		    if not sValor.replace(",",".").replace(".","").isdigit():
		        raise ValueError(sValor)
		except ValueError as e:
		    print("Valor invalido:", e)
		else:
		    break

	return sValor.replace(",",".")

def resetaPerolaDoDia():
	"""
	Identifica a entrada do arquivo para o dia de hoje e coloca nova perola no lugar
	"""
	global sArquivo
	global sArquivoCalendario

	vetCalendario = leArquivo(sArquivoCalendario)
	
	sPerola = ""
	for lCalendario in vetCalendario:	#procura pelo do dia de hoje
		if lCalendario.split("|")[0] == datetime.now().strftime("%Y-%m-%d"):
			sPerola = lCalendario.split("|")[1]
			break

	if not sPerola == "":
		sPerola = sorteiaPerola()
		if not sPerola == "":
			sTexto = datetime.now().strftime("%Y-%m-%d") + "|" + sPerola + "\n"
			gravaArquivo(sArquivoCalendario, sTexto, 'w')

	if sPerola == "":
		sPerola = perolaDoDia()
		
	return(sPerola.rstrip())

def palavrasMaisComuns(iQtde=5):
	"""
		Percorre toda a base de pérolas, conta as ocorrências de cada palavra 
	com 04 ou mais caracteres, ordena decrescente pela quantidade de ocorrências
	e devolve uma string com as X (05 por default) maiores ocorrências.
	"""
	dPerolas = {}
	vetPerolas = leArquivo(sArquivo)
	for lPerola in vetPerolas:
		vetPalavras = lPerola.split(' ')
		for sPalavra in vetPalavras:
			if (len(sPalavra.replace(' ','')) >= 4) and (not sPalavra.replace(' ','').isdigit()):
				if sPalavra in dPerolas:
					dPerolas[sPalavra] += 1
				else:
					dPerolas[sPalavra]  = 1

	vetQuantidades = []
	vetQuantidades += dPerolas.values()
	vetQuantidades.sort()
	vetQuantidades = vetQuantidades[::-1]
	vetQtde = vetQuantidades[:iQtde]
	sPalavrasMaisComuns = ""
	for iCont in vetQtde:
		sPalavrasMaisComuns += list(dPerolas.keys())[list(dPerolas.values()).index(iCont)] + " "
		dPerolas.pop(list(dPerolas.keys())[list(dPerolas.values()).index(iCont)])

	return(sPalavrasMaisComuns)

def pesquisarPerola():
	"""
	Exibe as palavras mais comuns da base de dados, e questiona termos de busca
	"""
	global sArquivo
	sTexto = ""
	while True:
		os.system('clear') or None
		print("Palavras mais comuns nas perolas cadastradas: {}\n".format(palavrasMaisComuns()))
		
		if sTexto.replace(' ', '').strip() == '9':
			break
		elif not len(sTexto.replace(' ', '').strip()) < 3:
			print("Texto que você digitou: " + sTexto)
			sFuncao = aceitarSoNumeros('1 (Confirma) ou 9 (Cancelar): ')
			if int(sFuncao) == 1:
				vetPerolas = leArquivo(sArquivo)
				iCont = 0
				for lPerola in vetPerolas:	
					if sTexto in lPerola:
						iCont+=1
						if iCont == 1:
							print("Perola(s) encontrada(s) com os termos da sua pesquisa: '" + sTexto + "'\n")

						print((3-len(str(iCont)))*'0'+str(iCont))
						print(lPerola)
				
				if iCont > 0:
					input("Pressione ENTER para sair: ")
					break
				else:
					print("Nao tem nenhuma perola com o texto que você digitou: '" + sTexto + "'")
					print("Voltando para a tela inicial")
					sleep(2)
					break
			elif int(sFuncao) == 9:
				break
			else:
				print("Você precisa escolhar uma das opcoes listadas")
				sleep(2)
		else:
			sTexto = str(input("Digite os termos da pesquisa (minimo 03 letras) ou 9 para sair: "))

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
		os.system('clear') or None
		print("{}\n".format(perolaDoDia()))
		print('Funções:')
		print('1 Pesquisar pérolas')
		print('2 Acrescentar texto aa relação de pérolas')
		print('3 Resetar a pérola do dia')
		print('9 Sair do programa')
		sFuncao = aceitarSoNumeros('Digite o número da função desejada: ')
		if int(sFuncao) == 3:
			resetaPerolaDoDia()
		elif int(sFuncao) == 2:
			acrescentaPerola()
		elif int(sFuncao) == 1:
			pesquisarPerola()
			pass
		elif int(sFuncao) == 9:
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
	_test()
	main()