import os
import argparse
import time

if len(os.listdir('/home/adtp/Documents/Yolo_mark/x64/Release/data/img/')) != 0: # ON verifie si le répértoire est vide
    os.system('rm /home/adtp/Documents/Yolo_mark/x64/Release/data/img/*')  # On vide le dossier img de Yolo mark

parser = argparse.ArgumentParser()
parser.add_argument('--path', nargs='+', type=str, help='path od data')
parser.add_argument('--rename', nargs='+', type=str, help='do you want to rename files that contain special caracters? (yes/no)')
opt = parser.parse_args()
directory = str(opt.path[0])#nom du dossier qui contient les photos : ../data_05_04_22/non_détouré/nouvel_objectif_19_05/


for filename in os.listdir(directory): # on parcours le dossier qui contient les images
    f = os.path.join(directory, filename) # nom du fichier
    name, extension = os.path.splitext(f) # on split le nom de chaque fichier en nom et extension
    if extension == '.jpg': # on verifie les fichier qui sont des images
        #Permet de ramplacer les caractère spéciaux
        if str(opt.rename[0]) == "yes":
            f_copy = f
            char_to_replace = {' ': '__',
                               '(': '',
                               ')': ''}
            # Iterate over all key-value pairs in dictionary
            for key, value in char_to_replace.items():
                # Replace key character with value character in string
                f_copy = f_copy.replace(key, value)

            os.rename(f,f_copy)

        #On lance la detection
        command = 'python detect.py --weights ../weights/new_exp/best_exp21.pth --source '+ f +' --img-size 640 --cfg models/yolov4-csp.yaml --save-txt'
        os.system(command)
        time.sleep(1)
        os.system('cp '+ f + ' /home/adtp/Documents/Yolo_mark/x64/Release/data/img')
        os.system('cp  /home/adtp/github/adtp/ScaledYOLOv4/inference/output/*.txt /home/adtp/Documents/Yolo_mark/x64/Release/data/img')
