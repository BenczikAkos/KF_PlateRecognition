Ezen a repon alapul az egész ami itt van: https://github.com/alitourani/yolo-license-plate-detection

Ez egy YOLOv3-as kész, kőbe vésett modell rendszámtáblák felismeréséhez. A .weights ezen a linken elérhető: https://drive.google.com/file/d/1vXjIoRWY0aIpYfhj3TnPUGdmJoHnWaOc/edit az z object_detection_yolo.py-tel kell egy szinten lennie. 

Az object_detection_yolo.py-t kell futtatni, kötelező argumentum az --input_dir, ahol az összes fájlt megpróbálja majd rendszámfelismerni. A többi argumentum opcionális, azt lehet megadni hogy hova mentse a croppolt képeket, a label txt-ket, azokat a képeket amiken nem talált rendszámot. A --done_dir ami default-ból a croppolt rendszámok mappája azért jó mert ha többször lefuttatod módosított confidence thresholddal akkor amiket már megtalált előzőleg, azokat kihagyja. 

Motorok és kamionok elég rosszul mennek neki.

A label-ek olyan txt-k amikkel lehet majd fine-tuningolni egy másik YOLO modellt, ami talán ezek alapján jobban rátanul a rendszámokra és felismeri azokat is amit ez a modell nem tudott. A labelek felépítése: class_id center_x center_y bbox_width bbox_height ahol a class_id mindig 0, mert csak LP-kre tanítjuk, xywh pedig normalizált (0-1). 