
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

from templates.functions import clicked_button


font = cv2.FONT_HERSHEY_SIMPLEX
# FILE_PNG_AB = 'qrcode_AB.png'



def main():
    st.title("バーコード読み込み")

    upload_file = st.file_uploader("ファイルアップロード", type = ["jpeg", "jpg", "BMP"], accept_multiple_files=True)
    # print(upload_file)
    # upload_file = st.file_uploader("ファイルアップロード", type = ["jpeg", "jpg", "BMP"], accept_multiple_files=False)

    # 画像表示用のボタン
    checkbox = st.checkbox("選択した画像の表示")
    # Image display
    if checkbox == True:
        if upload_file is not None:
            if upload_file != []:
                if type(upload_file) != list:
                    image = Image.open(upload_file)
                    image_array = np.array(image)
                    st.image(image_array, use_column_width=True)

                else:
                    cols = st.columns(len(upload_file))
                    for i in range(len(upload_file)):
                        with cols[i]:
                            image = Image.open(upload_file[i])
                            image_array = np.array(image)
                            st.image(image_array, use_column_width=True)
            else:
                st.write("画像を選択してください")
        else:
            st.write("画像を選択してください")


    if st.button("クリックしてください"):
        qr_data_all = clicked_button(upload_file)
        # print("¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥")
        # print(qr_data_all)
        # print("¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥")

        # 画像からバーコードを読み込む
        # 1次元コードの読み込み
        if upload_file is not None:
            if upload_file != []:
                st.write("読み込んだ画像からデータをデータを読み込みました")
                
                if type(upload_file) != list:
                    file_names = upload_file.name
                    df_data_list = pd.DataFrame()
                    df_data_list["ファイル名"] =  [file_names]
                    df_data_list["機種名"] = qr_data_all[0]
                    df_data_list["ロット"] = qr_data_all[1]
                    df_data_list.set_index("ファイル名")
                    st.dataframe(df_data_list)
                else:
                    file_names = [ upload_file[i].name for i in range(len(upload_file))]
                    # df_data_list = pd.DataFrame(np.random.randn(len(file_names), 2), columns=["機種名", "ロット"], index=file_names)
                    print(type(qr_data_all))
                    df_data_list = pd.DataFrame(qr_data_all, columns=["機種名", "ロット"], index=file_names)
                    st.dataframe(df_data_list)

                    # ファイルの出力
                csv = df_data_list.to_csv()
                today = str(datetime.date.today())
                st.download_button("csvダウンロード", data = csv, file_name= today + ".csv")



if __name__ == "__main__":
    main()