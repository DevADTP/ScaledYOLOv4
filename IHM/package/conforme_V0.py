import serial
from collections import Counter

tab_predictions = [] 		# tableau contenant la prediction par YOLO
tab_fiche = [] 				# tableau qui va contenir la liste des pieces de la fiche de référence

dict_pred = {"Capuchon_Plastique":[3], "Rondelle":[4], "vis":[9], "ecrou_carre":[3], "ecrou_rond":[5]}
dict_fiche = {"Capuchon_Plastique":[3], "Rondelle":[4], "vis":[9], "ecrou_carre":[3], "ecrou_rond":[5]}

def conformite_conditionnement_dict():
	if ((dict_pred['vis'] == dict_fiche['vis']) and 
	(dict_pred['Capuchon_Plastique'] == dict_fiche['Capuchon_Plastique'])and 
	(dict_pred['Rondelle'] == dict_fiche['Rondelle'])and 
	(dict_pred['ecrou_rond'] == dict_fiche['ecrou_rond'])and 
	(dict_pred['ecrou_carre'] == dict_fiche['ecrou_carre'])):
		print("Sachet OK") 
	else:
		print("Sachet pas OK")
	
#----------------------------------------------------------------------#
#fonction qui permet l'affichage d'un tableau

def affichage_tableau(tab):
	
	#print("Affichage de la liste  : ")
	for i in range(len(tab)):
		print(tab[i])

#----------------------------------------------------------------------#
#Remplissage d'une liste avec les elements d'un fichier texte

def remplissage_tableau(nom_fichier, tab):
	with open(nom_fichier, 'r') as fichier:
		for line in fichier:
			tab.append(line.strip())

#----------------------------------------------------------------------#
#Comparaison de deux listes

def comparaison_listes(liste1, liste2):
	res = False
	if (liste1 == liste2):
		res = True
	else:
		res = False
	return res

#----------------------------------------------------------------------#
#Affichage en mode lecture du fichier de la liste des predictions 
					
def lecture_fichier_liste_pieces(liste_pieces = "ListePieces.txt"):
	#Lecture du fichier de liste de pieces	
	print("Lecture du fichier de la liste de pieces : ")
	fichier = open(liste_pieces, "r")
	lignes = fichier.readlines()
	compteur = 0
	for ligne in lignes:
		tab_fiche = ligne
		compteur= compteur+1
		#(ligne)
		#print(compteur)

#----------------------------------------------------------------------#
#Affiche une phrase en fonction du resultat de la similitude de deux listes
		
def affichage_validation(liste1,liste2):
	resultat = comparaison_listes(liste1, liste2)
	if  resultat == True:
		print("Sachet OK")
		port.write(b'1')
		 
		
	else:
		print("Sachet pas OK")
		port.write(b'0')

#----------------------------------------------------------------------#
#fonction qui permet de verifier la conformite du conditionnement

def conformite_conditionnement(tab_predictions, liste_pieces ):
	tab_predictions_triee = []			#initialisation d'une liste qui va contenir les predictions triees issues de l'algorithme
	tab_fiche_triee =[] 
	lecture_fichier_liste_pieces(liste_pieces)
	print('\n')
	print("Affichage de la liste de predictions : ")
	affichage_tableau(tab_predictions)					#affichage de la liste tab_predictions 
	remplissage_tableau(liste_pieces, tab_fiche)		#la liste tab_fiche est rempli a partir des elements du fichier texte
	print('\n')
	tab_predictions_triee = sorted(tab_predictions)		#la liste de predictions est triée
	tab_fiche_triee = sorted(tab_fiche)					#la liste de la fiche de référence est triée	
	
	print("Affichage la liste de pieces : ")
	print(tab_fiche)
	print('\n')
	print("Affichage de la liste de predictions trie : ")
	print(tab_predictions)
	print('\n')
	
	manquant = Counter(tab_fiche_triee)-Counter(tab_predictions_triee)	#pieces manquante lors de la prediction
	print("manquant..........")
	print(manquant)
	print("EnTrop..........")
	EnTrop = Counter(tab_predictions_triee)-Counter(tab_fiche_triee) 	#pieces en trop lors de la prediction
	print(EnTrop)
	
	affichage_validation(tab_fiche_triee, tab_predictions_triee)  #comparaison des deux listes de predictions puis affichage du resultat
	tab_fiche_triee[:] = []		#la liste tab_fiche est vide
	#ligne ci-dessous a commenter si le tab_prediction est initalise manuellement
	tab_predictions[:] = []			#la liste tab_predictions est vide
			

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)

#tab_predictions = ["ecrou carre","Rondelle","vis","capuchon","ecrou ronds"] # tableau contenant la prediction par YOLO
#conformite_conditionnement(tab_predictions, "ListePieces.txt")
