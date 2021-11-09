import serial
from collections import Counter
import os
from flask import Flask, jsonify, request

dict_fiche = {}
dict_pred={}
#----------------------------------------------------------------------#

# INitialisation du dictionnaire de prediction
def init_conform(dict_pred, liste_pieces):
	if (os.path.exists(liste_pieces)):
		fichier = open(liste_pieces, "r")
		lignes = fichier.readlines()
		for ligne in lignes:
			if(ligne[1] != " "):
				num = int(ligne[0])*10 + int(ligne[1])
				dict_pred[ligne[3:len(ligne) - 1]] = [num]
			else:
				dict_pred[ligne[2:len(ligne) - 1]] = [int(ligne[0])]

def lecture_fichier_liste_pieces(liste_pieces):

	#Lecture du fichier de liste de pieces	

	#print("Lecture du fichier de la liste de pieces : ")
	if(os.path.exists(liste_pieces)):
		fichier = open(liste_pieces, "r")
		lignes = fichier.readlines()

		for ligne in lignes:
			#dict_fiche[ligne[2:len(ligne)-1]].append(int(ligne[0]))
			if (ligne[1] != " "):
				num = int(ligne[0]) * 10 + int(ligne[1])
				dict_fiche[ligne[3:len(ligne) - 1]] = [num]
			else:
				dict_fiche[ligne[2:len(ligne) - 1]] =[int(ligne[0])]


# fonction qui permet de mettre en place un dictionnaire avec la
#quantité de chaque pièce pour envoyer une trame
def get_dict_quantity(dict_pred):
	dict_quantity ={}
	for key, value in dict_pred.items():
		dict_quantity[key] = value[0]
		dict_quantity["qty"+key] = dict_fiche[key][0]
	print(dict_quantity)
	return dict_quantity

#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

def conformite_conditionnement_dict(dict_pred, fichier_pieces, serialPort):

	for key, value in dict_pred.items():
		if(value == []):
			dict_pred[key]=[0]

	liste_pieces = fichier_pieces
	lecture_fichier_liste_pieces(liste_pieces)

	# if ((dict_pred['vis'] == dict_fiche['vis']) and
	# (dict_pred['Capuchon_Plastique'] == dict_fiche['Capuchon_Plastique'])and
	# (dict_pred['Rondelle'] == dict_fiche['Rondelle'])and
	# (dict_pred['ecrou_rond'] == dict_fiche['ecrou_rond'])and
	# (dict_pred['ecrou_carre'] == dict_fiche['ecrou_carre'])):

	if(dict_pred == dict_fiche):
		print("Sachet OK")
		#serialPort.write(b'1')
		valide = 1
	else:
		print("Sachet pas OK")
		#serialPort.write(b'0')
		valide = 0
	return valide
#----------------------------------------------------------------------#
def not_detected(serialPort):
	#serialPort.write(b'0')
	print('')

