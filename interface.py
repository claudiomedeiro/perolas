#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Claudio Jorge Severo Medeiro"
__email__ = "cjinfo@gmail.com"

"""Módulo que monta as interfaces do programa.
"""
import tkinter as tk
import perolas
from time import sleep

# ent_opcao = object

def identifica_escolha():
    """Recebe o texto e após avaliar se é uma opção válida, executa o 
    comando da opção.
    """

    str_opcao = ent_opcao.get()
    ent_opcao.delete(0, len(str_opcao))
    lbl_mensagens["text"] = "str_opcao: {}".format(str_opcao)

    if str_opcao == "3":
        lbl_perola_do_dia["text"] = perolas.reseta_perola_do_dia()

    elif str_opcao == "2":
        lbl_mensagens["text"] = "{} - {}".format(lbl_mensagens["text"], "acrescenta_perola()")
        # A ideia aqui é destruir o frame da inteface inicial e inserir outro em seu lugar
        # frm_interface_inicial.destroy()        
        # perolas.acrescenta_perola()

    elif str_opcao == "1":
        lbl_mensagens["text"] = "{} - {}".format(lbl_mensagens["text"], "pesquisar_perola()")
        # perolas.pesquisar_perola()
        # A ideia aqui é destruir o frame da inteface inicial e inserir outro em seu lugar
        # frm_interface_inicial.destroy()

        
    elif str_opcao == "9":
        janela.destroy()

    else:
        lbl_mensagens["text"] = "Você precisa escolhar uma das opções listadas"


if __name__ == "__main__":
    # global ent_opcao

    janela = tk.Tk()        # Instancia janela

    ### Frame da mensagem do dia (início) ###
    frm_topo_mensagem = tk.Frame(master=janela, background="red")
    frm_topo_mensagem.pack()

    # Acrescenta o label ao frame, contendo a pérola do dia
    lbl_perola_do_dia = tk.Label(master=frm_topo_mensagem, text=perolas.perola_do_dia())
    lbl_perola_do_dia.pack()
    ### Frame da mensagem do dia (fim) ###


    ### Frame do menu inical (início) ###
    frm_interface_inicial = tk.Frame(master=janela, background="green")
    frm_interface_inicial.pack()

    # Acrescenta label ao frame, contendo a lista de opções
    str_opcoes  = "Funções:"
    str_opcoes += "\n1 Pesquisar pérolas"
    str_opcoes += "\n2 Acrescentar texto aa relação de pérolas"
    str_opcoes += "\n3 Resetar a pérola do dia"
    str_opcoes += "\n9 Sair do programa"
    lbl_opcoes = tk.Label(master=frm_interface_inicial, text=str_opcoes)
    lbl_opcoes.pack()

    # Acrescenta caixa de edição ao frame, para coletar a opção
    ent_opcao = tk.Entry(master=frm_interface_inicial, text="")
    ent_opcao.pack()

    # Acrescenta o botão ao frame
    btn_enviar = tk.Button(master=frm_interface_inicial, text="Enviar", command=identifica_escolha)
    btn_enviar.pack()
    ### Frame do menu inical (fim) ###


    ### Frame das mensagens de feedback (início) ###
    frm_rodape_mensagens = tk.Frame(master=janela, background="blue")
    frm_rodape_mensagens.pack()

    lbl_mensagens = tk.Label(master=frm_rodape_mensagens, text="...")
    lbl_mensagens.pack()
    ### Frame das mensagens de feedback (fim) ###
    
    janela.mainloop()       # Roda o loop da janela