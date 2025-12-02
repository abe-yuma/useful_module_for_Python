# -*- coding: utf-8 -*-
import psutil
import os
import threading
import time

class PeakMemoryTracker:
    #実行中のプロセスのピークメモリ使用量 (RSS) を別スレッドで監視し、追跡するクラス。
    def __init__(self, interval=0.05): #0.05秒置きに監視
        self._max_rss = 0  #バイト単位で記録
        self._interval = interval
        self._is_running = False
        self._thread = None
        self._pid = os.getpid()

    def _monitor(self):
        #監視スレッドで実行される関数
        try:
            process = psutil.Process(self._pid)
        except psutil.NoSuchProcess:
            print("警告: 対象プロセスが見つかりません。")
            return
            
        while self._is_running:
            try:
                #物理メモリ使用量 (RSS: Resident Set Size) をバイト単位で取得
                current_rss = process.memory_info().rss
                
                #最大値を更新
                self._max_rss = max(self._max_rss, current_rss)
                time.sleep(self._interval)
            except psutil.NoSuchProcess:
                #プロセスが終了した場合は停止
                break
            except Exception as e:
                #その他のエラー処理
                print(f"監視エラー: {e}")
                break

    def start(self):
        #監視スレッドを開始する
        if not self._is_running:
            self._is_running = True
            #デーモンスレッドとして起動し、メインスレッド終了時に強制終了させる
            self._thread = threading.Thread(target=self._monitor, daemon=True)
            self._thread.start()
            print(f"メモリ監視スレッドを開始しました (PID: {self._pid})。")

    def stop(self):
        #監視スレッドを停止する
        if self._is_running:
            self._is_running = False
            if self._thread and self._thread.is_alive():
                self._thread.join()
            print("メモリ監視スレッドを停止しました。")

    def get_peak_memory_mb(self):
        #記録された最大メモリ使用量 (RSS) をMB単位で返す
        return self._max_rss / (1024 * 1024)

    def __enter__(self):
        #withステートメント開始時の処理
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #withステートメント終了時の処理
        self.stop()