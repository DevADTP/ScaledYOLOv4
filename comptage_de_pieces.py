import os

directory = "/home/adtp/Documents/Yolo_mark/x64/Release/data/img/"
nombre_de_pieces = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
cpt_tot = 0  # nombre total de pièces détouré
for filename in os.listdir(directory):  # on parcours le dossier qui contient les images
    f = os.path.join(directory, filename)  # nom du fichier
    name, extension = os.path.splitext(f)  # on split le nom de chaque fichier en nom et extension
    if extension == '.txt':
        with open(f, "r") as f_open:
            nb_line = 0
            for line in f_open:
                nb_line = nb_line + 1
                # print(line[0]) # lecture du premier caractère de chaque ligne
                nombre_de_pieces[line[0]] = nombre_de_pieces[line[0]] + 1
            f_open.close()
            cpt_tot = cpt_tot + nb_line

#remplacer l'id des pièces par leurs noms
new_dict={}
for key, value in nombre_de_pieces.items():
    if key == '0':
        new_dict['A'] = value;
    elif key == '1':
        new_dict['B'] = value;
    elif key == '2':
        new_dict['C'] = value;
    elif key == '3':
        new_dict['G'] = value;
    elif key == '4':
        new_dict['D'] = value;
    elif key == '5':
        new_dict['E'] = value;
    elif key == '6':
        new_dict['F'] = value;

#Affichage
print("nombre total : " + str(cpt_tot))
for key, value in new_dict.items():
    print(str(key) +" : " + str(value))