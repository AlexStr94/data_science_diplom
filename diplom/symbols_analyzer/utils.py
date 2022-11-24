import io
import json
import cv2
import numpy as np
import pandas as pd
import pickle
from PIL import Image

from django.core.files.base import ContentFile
import tensorflow as tf

from diplom.settings import BASE_DIR
from .exceptions import BadResolution
from .models import CellImage

def create_grid(img_bin, need_shape=False):
    kernal_values = (60, 80, 100, 120)

    def _internal_grid_creator(img_bin, value):
        kernal_h = np.ones((1,value), np.uint8)
        kernal_v = np.ones((value,1), np.uint8)
        img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
        img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
        img_bin_final=img_bin_h|img_bin_v
        _, _, stats, _  = cv2.connectedComponentsWithStats(
            ~img_bin_final,
            connectivity=8,
            ltype=cv2.CV_32S
        )

        # Высчитываем среднюю площадь ячейки и удаляем ошибочно выделенные
        # сектора и внешние рамки
        mean_area = np.mean(stats[2:,4], axis=0)
        arr = np.delete(
            stats, np.where(
                (stats[:, 4] < (mean_area // 10)) | (stats[:, 4] > (mean_area * 10))
            )[0],
            axis=0
        )

        return arr

    if need_shape:
        for value in kernal_values:
            arr = _internal_grid_creator(img_bin, value)
            if arr.shape == (need_shape[0]*need_shape[1], 5):
                return arr

        raise BadResolution
    else:
        return _internal_grid_creator(img_bin, 80)


def analyze_image(image, need_shape=False):
    image = cv2.fastNlMeansDenoising(image)
    gray_scale=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    img_bin = cv2.adaptiveThreshold(
        gray_scale,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        199,
        5
    )

    arr = create_grid(img_bin, need_shape)
    
    # Вычисляем среднюю высоту ячейки и создаем новый отсортированный список
    if need_shape:
        mean_hight = np.mean(arr[:,3], axis=0)

        new_arr = [[list(arr[0])]]

        for cell in arr[1:]:
            y = cell[1]
            row_find = False
            for row in new_arr:
                first_cell_y = row[0][1]
                if abs(y-first_cell_y) < mean_hight / 2:
                    row.append(list(cell))
                    row_find = True
            if not row_find:
                new_arr.append([list(cell)])
                
        sorted_arr = sorted(new_arr, key=lambda x: x[0][1])
        for row in sorted_arr:
            row.sort()
        df = pd.DataFrame(sorted_arr)
    if need_shape:
        if df.shape == need_shape:
            return df, img_bin
        else:
            raise BadResolution
    return arr, img_bin
    
def get_grades(img_bin, df):
    df = df[1:]
    grades = []
    # model_dir = str(BASE_DIR.parent) + '/models/cfu/forest_model.sav'
    # loaded_model = pickle.load(open(model_dir, 'rb'))
    
    # for index, row in df.iterrows():
    #     grades.append([])
    #     for cell in range(2, len(row)):
    #         cell = row[cell]
    #         cell = img_bin[cell[1]+1:cell[1]+cell[3]-1, cell[0]+1:cell[0]+cell[2]-1]
    #         if np.mean(cell) < 15:
    #             grades[index-1].append('')
    #         else:
    #             resized = cv2.resize(cell, (28, 28), interpolation = cv2.INTER_AREA)
    #             resized = resized.reshape(784,) / 255
    #             pred = loaded_model.predict([resized])
    #             if pred[0] == 6.0:
    #                 pred = 'н'
    #             else:
    #                 pred = str(int(pred[0]))
    #             grades[index-1].append(pred)

    model_dir = str(BASE_DIR.parent) + '/models/cfu/nn_model.h5'
    loaded_model = tf.keras.models.load_model(model_dir)
    probability_model = tf.keras.Sequential([loaded_model, 
                                         tf.keras.layers.Softmax()])
    
    for index, row in df.iterrows():
        grades.append([])
        for cell in range(2, len(row)):
            cell = row[cell]
            cell = img_bin[cell[1]+1:cell[1]+cell[3]-1, cell[0]+1:cell[0]+cell[2]-1]
            if np.mean(cell) < 15:
                grades[index-1].append('')
            else:
                resized = cv2.resize(cell, (28, 28), interpolation = cv2.INTER_AREA)
                resized = resized / 255
                image = np.array([resized])
                prediction = probability_model.predict(image)
                prediction = np.argmax(prediction[0])
                if prediction == 6.0:
                    prediction = 'н'
                else:
                    prediction = str(int(prediction))
                grades[index-1].append(prediction)
    
    return grades

def get_row_data(img_bin, arr):
    images = []
    img_bin = ~img_bin
    for cell in arr:
        cell = img_bin[cell[1]+1:cell[1]+cell[3]-1, cell[0]+1:cell[0]+cell[2]-1]
        resized = cv2.resize(cell, (28, 28), interpolation = cv2.INTER_AREA)

        image = Image.fromarray(cell)
        print(type(image))
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG', quality=100)
        img_content = ContentFile(image_io.getvalue(), 'cell.jpg')

        resized = resized.reshape(784,) / 255
        image_array = json.dumps(np.ndarray.tolist(resized))
        

        image = CellImage(
            image=img_content,
            image_array=image_array
        )

        images.append(image)
    
    CellImage.objects.bulk_create(images)
            
