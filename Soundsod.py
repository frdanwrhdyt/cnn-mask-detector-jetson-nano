from playsound import playsound
import time
from numpy import load


sc= "/home/btp/Documents/SocialDistancing/test/cnn-mask-detector-jetson-nano/music/"


file1 = sc + "masker.wav"
file2 = sc + "menjauh.wav"


def play():
        while True:
            F = open("sound.txt","r")
            #print("run again")
            try:
                status = F.read()
                if status == "0":
                    playsound(file1)
                elif status == "2":
                    playsound(file2)
            except IOError:
                print("Oops IO Error!")
            except ValueError:
                print("Oops Value Error!")
            F.close()
            del status
if __name__ == "__main__":
    play()