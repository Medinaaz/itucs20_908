#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

def sendmessageicon(message,icon):
    subprocess.Popen(['notify-send', '-i', icon, message])
    return

def sendmessagetitle(message,title):
    subprocess.Popen(['notify-send', title, message])
    return

def msg(message,title,icon):
    subprocess.Popen(['notify-send', title, '-i', icon, message])
    return