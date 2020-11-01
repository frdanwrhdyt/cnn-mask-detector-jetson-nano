import playsound
import time
from numpy import load


sc= "e:/AErs/Proyek_Robot_thermal_scaning/robot/"

d = open("data.txt", "r")
file1 = sc + "Alarm4.mp3"
file2 = sc + "Alarm8.mp3"
file3 = sc + "Alarm12.mp3"

def readtime():
        i = 0
        for x in d:
            i = i+1
            if i == 6:
                return x
    
def choose():
        t = readtime()
        if t == "4":
            files = file1
        elif t == "8":
            files = file2
        elif t == "12":
            files = file3
        return files
        
def play():
        F = choose()
        while True:
            #print("run again")
            try:
                status = load(sc+ "sound.txt")
                print(status)
                if status == "0":
                    print("alarm")
            except IOError:
                print("Oops IO Error!")
            except ValueError:
                print("Oops Value Error!")
            
            time.sleep(1)

if __name__ == "__main__":
    play()