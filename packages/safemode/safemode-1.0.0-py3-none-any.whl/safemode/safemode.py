#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import Thread
import sys, tty, termios
import os

if 'SAFEMODE_GRACE_PERIOD' in os.environ:
    SAFEMODE_GRACE_PERIOD = os.environ['SAFEMODE_GRACE_PERIOD']
else:
    SAFEMODE_GRACE_PERIOD = 5


def configure_tty():
    old_settings = termios.tcgetattr(sys.stdin.fileno())
    tty.setraw(sys.stdin.fileno())
    return old_settings


def restore_tty(old_settings):
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)


def capture_key():
    global key_pressed
    key_pressed = sys.stdin.read(1)


def launch_shell():
    os.execv('/bin/sh', (' ', ))


print(f'[safemode] To start a shell, press any key before {SAFEMODE_GRACE_PERIOD} seconds...')
old_settings = configure_tty()
key_pressed = False
thread = Thread(target=capture_key, daemon=True).start()
for _ in range(SAFEMODE_GRACE_PERIOD):
    if key_pressed:
        restore_tty(old_settings)
        launch_shell()
    time.sleep(1)
restore_tty(old_settings)
print(f'[safemode] Starting up normally...')
