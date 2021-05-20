import serial
from collections import Counter

tab_predictions = [] 		# tableau contenant la prediction par YOLO
tab_fiche = [] 				# tableau qui va contenir la liste des pieces de la fiche de référence

#dict_pred = {"Capuchon_Plastique":[], "Rondelle":[], "vis":[], "ecrou_carre":[], "ecrou_rond":[]}
dict_fiche = {"Capuchon_Plastique":[], "Rondelle":[], "vis":[], "ecrou_carre":[], "ecrou_rond":[]}

#----------------------------------------------------------------------#

def lecture_fichier_liste_pieces(liste_pieces = "ListePieces.txt"):
	
	#Lecture du fichier de liste de pieces	
	
	print("Lecture du fichier de la liste de pieces : ")
	fichier = open(liste_pieces, "r")
	lignes = fichier.readlines()

	for ligne in lignes:
		tab_fiche = ligne
		'''print("\n--------------------------------\n")
		print(int(ligne[0]))
		print("\n--------------------------------\n")'''
		#dict_fiche[ligne[2:len(ligne)-1]].append(int(ligne[0]))
		dict_fiche[ligne[2:len(ligne) - 1]] =[int(ligne[0])]
	
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
	
def conformite_conditionnement_dict(dict_pred, fichier_pieces):
	for key, value in dict_pred.items():
		if(value == []):
			dict_pred[key]=[0]
	lecture_fichier_liste_pieces("ListePieces.txt")

	if ((dict_pred['vis'] == dict_fiche['vis']) and
	(dict_pred['Capuchon_Plastique'] == dict_fiche['Capuchon_Plastique'])and 
	(dict_pred['Rondelle'] == dict_fiche['Rondelle'])and 
	(dict_pred['ecrou_rond'] == dict_fiche['ecrou_rond'])and 
	(dict_pred['ecrou_carre'] == dict_fiche['ecrou_carre'])):
		
		print("Sachet OK") 
		port.write(b'1')
	
	else:
		print("Sachet pas OK")
		port.write(b'0')
	#print(dict_fiche)
	#print(dict_pred)
#----------------------------------------------------------------------#
def not_detected():
	port.write(b'0')


port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)

#tab_predictions = ["ecrou carre","Rondelle","vis","capuchon","ecrou ronds"] # tableau contenant la prediction par YOLO
#conformite_conditionnement(tab_predictions, "ListePieces.txt")
