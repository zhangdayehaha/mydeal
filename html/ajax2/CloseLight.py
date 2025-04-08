# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT, initial=False)
GPIO.setup(17, GPIO.OUT, initial=False)

p1 = GPIO.PWM(4,50) #50HZ
p2 = GPIO.PWM(17,50) #50HZ



p1.start(10) #初始化角度

p2.start(10) #初始化角度


time.sleep(1)

p1.start(7) #初始化角度

p2.start(7) #初始化角度
time.sleep(1)
p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动



p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
