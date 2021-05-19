from package import conforme

dict_pred = {"Capuchon_Plastique":[3], "Rondelle":[4], "vis":[9], "ecrou_carre":[3], "ecrou_rond":[5]}
#dict_fiche = {"Capuchon_Plastique":[], "Rondelle":[], "vis":[], "ecrou_carre":[], "ecrou_rond":[]}

conforme.conformite_conditionnement_dict(dict_pred,"ListePieces.txt")
#conforme.lecture_fichier_liste_pieces("ListePieces.txt")
