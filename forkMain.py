# -*- coding:utf-8 -*- 
#  @Time : 2018-01-09 11:15
#  @Author : Khazix
#  @File : forkMain.py
#  @Description:
#            
#   --Input:
#   --Output:
import util.search as sch
import util.ocr as ocr
import time
import os
from pyhooked import Hook, KeyboardEvent, MouseEvent
import win32gui

def main():
    # 开始计时
    start = time.time()
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png screenshot.png")
    question, answer = ocr.ocr_result('./screenshot.png')
    print('问题:%s' % question)
    score, results, counts = sch.get_search_result(question, answer)
    for i in range(len(results)):
        count = 0
        print("#####################[%s](搜索结果数目:%s)(页面词频:%s)#########################" % (answer[i], score[i], counts[i]))
        for abst in results[i]:
            print(abst.abstract)
            count = count + 1
            if (count == 2):
                break
    end = time.time()
    print('程序用时：' + str(end - start) + '秒')

# main()

def handle_events(args):
    if isinstance(args, KeyboardEvent):
        if args.current_key == 'F2' and args.event_type == 'key down':
            main()
        elif args.current_key == 'Q' and args.event_type == 'key down':
            hk.stop()
            print('辅助退出')

vm_name ="BlueStacks App Player"
if __name__ == "__main__":
    hld = win32gui.FindWindow(None, vm_name)
    if hld > 0:
        print('辅助运行中...\n题目出现的时候按F2，开启自动搜索\n')
        hk = Hook()
        hk.handler = handle_events
        hk.hook()
    else:
        print('模拟器（'+vm_name+'）未启动!')