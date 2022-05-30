#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from gtts import gTTS
from playsound import playsound



eng_wav = gTTS("손목 보호대와 연결되었습니다.", lang = 'ko')
eng_wav.save('eng.wav')

playsound('eng.wav')

#winsound.Playsound('eng,wav')