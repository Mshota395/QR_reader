
from typing import List
import cv2
import re
import numpy as np
from numpy.lib.shape_base import column_stack
import pandas as pd
import streamlit as st
from PIL import Image
import datetime 
from pyzbar.pyzbar import decode

font = cv2.FONT_HERSHEY_SIMPLEX




# クリックした時の動作画像からピックアップして
def clicked_button(upload_file):
    qr_data_all = []
    if upload_file is not None:
        if upload_file != []:
            if type(upload_file) != list:
                image = Image.open(upload_file)
                # image_array_BGR = np.array(image)
                # img_BGR = cv2.imread(image_array_BGR, cv2.IMREAD_COLOR)
                qr_data_list = function_qrdec_pyzbar(image)
                qr_data_all.append(qr_data_list)


            else:
                cols = st.columns(len(upload_file))
                for i in range(len(upload_file)):
                    with cols[i]:
                        image = Image.open(upload_file[i])
                        # image_array_BGR = np.array(image)
                        # img_BGR = cv2.imread(image_array_BGR, cv2.IMREAD_COLOR)
                        # function_qrdec_pyzbar(image)
                        qr_data_list = function_qrdec_pyzbar(image)
                        # print("aaa:")
                        # print(qr_data_list)
                        qr_data_all.append(qr_data_list)
            
    return qr_data_all
    #     else:
    # else:


# バーコード読み込み関数
def function_qrdec_pyzbar(img_bgr):
    
    # QRコードデコード
    value = decode(img_bgr)
    print(value)

    if value:
        # qr_data_all = []
        qr_data_list = []
        for qrcode in value:
            if qrcode.type == "QRCODE":
                # print("init:")
                # print(qr_data_list)
                qr_data_list = []
                # QRコード座標取得
                x, y, w, h = qrcode.rect
                qr_data = qrcode.data

                # QRコードデータ
                dec_inf = qrcode.data.decode('utf-8')
                # print('dec :', dec_inf)
                qr_dec = re.split(" +", dec_inf)
                global qr_data_model, qr_data_lot
                qr_data_model = qr_dec[0]
                qr_data_lot = qr_dec[1]
                qr_data_list = [qr_data_model, qr_data_lot]
                # qr_data_all.append(qr_data_list)
                # print("model :", qr_data_model)
                # print("lot :", qr_data_lot)
                # print("¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥")
                img_bgr = np.array(img_bgr)
                img_bgr_text = cv2.putText(img_bgr, text = dec_inf, org = (x, y - 6), fontFace = font, fontScale = 2.0, color = (255, 0, 0), thickness = 1, lineType = cv2.LINE_AA)

                # バウンディングボックス
                img_bc = cv2.rectangle(img_bgr_text, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # image = Image.open(upload_file)
                image_array_bc = np.array(img_bc)
            else:
                if qr_data_list ==[]:
                    # image_array_bc = np.array(img_bgr)
                    image_array_bc = img_bgr
                    qr_data_list = ["QR読み込めない",""]
        
        # print("last")
        # print(qr_data_list)
    else:
        # print("nothing")
        image_array_bc = img_bgr
        qr_data_list = ["QR読み込めない",""]
    
    st.image(image_array_bc, use_column_width=True)
    
    return qr_data_list