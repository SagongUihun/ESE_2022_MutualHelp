#-*-coding:utf-8-*-
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

import pygame
#from playsound import playsound 셋, 넷, 다섯, 여섯, 일곱, 여덟, 아홉, 열
from gtts import gTTS
count = ["하나", "둘","셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉", "열","열하나","열둘","열셋","열네","열다섯","열여섯","열일곱","열여덟","열아홉","스물"]
# for i in range(20):

#     eng_wav = gTTS(str(count[i]),lang='ko')
#     eng_wav.save(str(i+1)+'.wav')
#     os.system("mpg123 "+str(i+1)+".wav")
# pygame.mixer.init()
# p=pygame.mixer.Sound("ensg.wav")
# p.play()
voice = "손목보호대와 연결되었습니다!"
filename = "connectbt"

eng_wav = gTTS(voice,lang='ko')
eng_wav.save(filename+'.wav')
os.system("mpg123 "+filename+".wav")

#playsound("eng.wav")
#os.system("mpg123 3.wav")
# while True:
#     continue

#winsound.Playsound('eng,wav')