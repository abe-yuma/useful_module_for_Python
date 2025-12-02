# -*- coding: utf-8 -*-
import time

class Timer:#withステートメントを使用して実行時間を計測するクラス。計測開始時に時間を記録し、終了時に経過時間を出力する。
    def __init__(self, name=None):#name: 計測対象の名前。出力メッセージに使用される。
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
    
    def start(self):
        #withブロックに入ったときに実行される（計測開始）
        self.start_time = time.perf_counter() #精度の高い時間を記録
        if self.name:
            print(f"--- [START] {self.name} ---")
        return self

    def stop(self):
        #withブロックを抜けたときに実行される（計測終了と結果出力）
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        print(f"--- [STOP] {self.name} ---")

    def __enter__(self):
        #withステートメント開始時の処理
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #withステートメント終了時の処理
        self.stop()

    def get_elapsed_time(self):
         #計測された経過時間（秒単位）を取得する
         #単位を決定し、分かりやすくする
        if self.elapsed_time < 0.001:
            display_time = self.elapsed_time * 1000000
            unit = "μs"  #マイクロ秒
        elif self.elapsed_time < 1.0:
            display_time = self.elapsed_time * 1000
            unit = "ms"  #ミリ秒
        else:
            display_time = self.elapsed_time
            unit = "s"   #秒

        message = ""
        if self.name:
            message += f"--- [END] {self.name} "
        elapsed_time_message = f"{message}経過時間: {display_time:.4f} {unit} ---"
        return elapsed_time_message