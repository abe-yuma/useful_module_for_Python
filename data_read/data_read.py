# -*- coding: utf-8 -*-
import pandas as pd
import os

def multi_read_csv(path :str, csv_list : list): #pathはcsvが配置されているディレクトリのパス、csv_listに複数ファイルのパスを格納する
    #空のDataFrameを作成
    combined_df = pd.DataFrame()
    for csv_file in csv_list:
        csv_path = f"{path}/{csv_file}"
        if os.path.exists(csv_path):
            #CSVファイルを読み込み
            df = pd.read_csv(csv_path, encoding="utf_8",)
            #読み込んだDataFrameを結合
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        else:
            print(f"File {csv_file} does not exist.")
    return combined_df