# import pyyaml module
import shutil

import time
from pathlib import Path
import numpy as np
import os
import io
from PIL import Image
from keras.models import load_model
import cv2
from ultralytics import YOLO
import base64

#Базовые слои для свёрточных сетей
from keras.preprocessing.image import ImageDataGenerator # работа с изображениями
from keras.preprocessing import image #Для отрисовки изображений
import random #Для генерации случайных чисел 
import math # Для округления 


def setup(path_of_img,path_of_data_for_classify,path_of_data_for_generator,filepath):
    print(path_of_data_for_classify)
    print(path_of_data_for_generator)
    path = Path(os.getcwd())
    print("[INFO] Загрузка YOLO...")
    model_yolo = YOLO(str(path.absolute())+"/best.pt")
    print("[INFO] Загрузка классификационной нейронной сети...")
    model_class = load_model(str(path.absolute())+"/CP.h5")
    print("[INFO] Загрузка классификационной завершена")
    start_time = time.time()
    # YOLO
    # Perform object detection on an image using the model
    result = model_yolo.predict(path_of_img, conf=0.3, iou = 0.3)[0]

    img = Image.open(path_of_img)

    data_of_pic = {
      "Total": 0,
      "klikun": 0,
      "shipun": 0,
      "maliy": 0,
    }

    number_of_birds=0
    flag=0
    for i in result.boxes:
        list_of_ans_of_yolo = ['full swan', 'klikun', 'maliy', 'shipun']
        list_of_ans_of_class = ['klikun', 'maliy', 'shipun']

        boxes = i.xyxy.tolist()[0]
        conf = i.conf.tolist()[0]
        class_of_pic = int(i.cls.tolist()[0])

        print(boxes)
        print(conf)
        print(class_of_pic)
        if class_of_pic == 0:
            data_of_pic["Total"]+=1
            img = cv2.rectangle(np.array(img), (int(boxes[0]), int(boxes[1])), (int(boxes[2]), int(boxes[3])), (0, 255, 0), 2)
        else:
            im = Image.open(path_of_img)
            im_crop = im.crop((int(boxes[0]), int(boxes[1]), int(boxes[2]), int(boxes[3])))
            if not os.path.exists(path_of_data_for_classify):
                os.makedirs(path_of_data_for_classify)
            im_crop.save(path_of_data_for_classify+'/'+str(class_of_pic)+'_' + str(conf)+'.jpg', quality=95)

            #CLASSIFY
            validation_split=0
            batch_size = 32 #Размер выборки
            img_width = 192 #Ширина изображения
            img_height = 108 #Длина изображений
            datagen_1 = ImageDataGenerator(
            rescale=1. / 255, #Значения цвета меняем на дробные показания
            rotation_range=10, #Поворачиваем изображения при генерации выборки
            width_shift_range=0.1, #Двигаем изображения по ширине при генерации выборки
            height_shift_range=0.1, #Двигаем изображения по высоте при генерации выборки
            zoom_range=0.1, #Зумируем изображения при генерации выборки
            horizontal_flip=True, #Отключаем отзеркаливание изображений
            fill_mode='nearest', #Заполнение пикселей вне границ ввода
            validation_split=validation_split #Указываем разделение изображений на обучающую и тестовую выборку
            )

            demonstraition_generator = datagen_1.flow_from_directory(
            path_of_data_for_generator,
            target_size=(img_width, img_height), #Размер изображений
            batch_size=batch_size, #Размер батча
            class_mode='categorical', #Разбиение выборки по материалу
            shuffle=False, #Перемешивание выборки
            subset='training' # устанавливаем как набор для проверки
            )

            predict = model_class.predict(demonstraition_generator)
            result_of_class=np.argmax(predict, axis=1)[0]
            print(os.listdir(path=path_of_data_for_classify))
            print(predict)
            for filename in os.listdir(path_of_data_for_classify):
                file_path = os.path.join(path_of_data_for_classify, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('[INFO] Failed to delete %s. Reason: %s' % (file_path, e))

            #INTERPRETATE
            if list_of_ans_of_yolo[class_of_pic] == list_of_ans_of_class[result_of_class]:
                data_of_pic[list_of_ans_of_yolo[class_of_pic]] += 1
                img = cv2.rectangle(np.array(img), (int(boxes[0]), int(boxes[1])), (int(boxes[2]), int(boxes[3])), (255, 0, 0), 2)
                img = cv2.putText(np.array(img),
                list_of_ans_of_yolo[class_of_pic],
                (int(boxes[0]), int(boxes[1])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
            elif list_of_ans_of_yolo[class_of_pic] != list_of_ans_of_class[result_of_class]:
                if (conf+predict[0][class_of_pic-1])/2 < predict[0][result_of_class]:
                    data_of_pic[list_of_ans_of_class[result_of_class]] += 1
                    img = cv2.rectangle(np.array(img), (int(boxes[0]), int(boxes[1])), (int(boxes[2]), int(boxes[3])), (255, 0, 0), 2)
                    img = cv2.putText(np.array(img),
                    list_of_ans_of_class[result_of_class],
                    (int(boxes[0]), int(boxes[1])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                else:
                    data_of_pic[list_of_ans_of_yolo[class_of_pic]] += 1
                    img = cv2.rectangle(np.array(img), (int(boxes[0]), int(boxes[1])), (int(boxes[2]), int(boxes[3])), (255, 0, 0), 2)
                    img = cv2.putText(np.array(img),
                    list_of_ans_of_yolo[class_of_pic],
                    (int(boxes[0]), int(boxes[1])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
        print(data_of_pic)
        end_time = time.time()
        time_lapsed = end_time - start_time
        print(time_lapsed)
        #     i+=1
        # print(path_of_img + '\n' +path_of_text)
        # break
    Image.fromarray(np.uint8(img)).convert('RGB').save(filepath)
    return data_of_pic