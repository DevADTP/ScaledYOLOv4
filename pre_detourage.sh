#boucle qui permet de suprimmer les espaces et de les remplacer par des underscore
#for file in ../data_05_04_22/non_détouré/nouvel_objectif_19_05/*.jpg;do
#	mv "${file/}" "${file// /_}"
#done

#for file in ../data_05_04_22/non_détouré/nouvel_objectif_19_05/*.jpg;do
	#echo "${file##*/}"
#	python detect.py --weights ../weights/new_exp/best_exp21.pth --source ../data_05_04_22/non_détouré/nouvel_objectif_19_05/${file##*/} --img-size 640 --cfg models/yolov4-csp.yaml --save-txt
	#sleep 1
#	cp  ../data_05_04_22/non_détouré/nouvel_objectif_19_05/${file##*/} /home/adtp/Documents/Yolo_mark/x64/Release/data/img
#	cp  /home/adtp/github/adtp/ScaledYOLOv4/inference/output/*.txt /home/adtp/Documents/Yolo_mark/x64/Release/data/img
#done
	
