#-*-coding:utf-8-*-
from re import T
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pygame
from gtts import gTTS

eng_wav = gTTS("why why why.")
eng_wav.save('eng.wav')

pygame.mixer.init()
p=pygame.mixer.Sound("ensg.wav")
p.play()

while True:
    continue

#winsound.Playsound('eng,wav')