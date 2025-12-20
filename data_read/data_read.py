# -*- coding: utf-8 -*-
import pandas as pd
import os

def multi_read_csv(path :str, list_csv : list): #pathはcsvが配置されているディレクトリのパス、csv_listに複数ファイルのパスを格納する
    #空のDataFrameを作成
    df_combined = pd.DataFrame()
    for csv_file in list_csv:
        csv_path = f"{path}/{csv_file}"
        if os.path.exists(csv_path):
            #CSVファイルを読み込み
            df = pd.read_csv(csv_path, encoding="utf_8",)
            #読み込んだDataFrameを結合
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        else:
            print(f"File {csv_file} does not exist.")
    return df_combined