from PIL import Image
from player import APlayer,Player
import numpy 

def FromArr(arr,name):
    data = numpy.zeros((len(arr),len(arr[0]),3), dtype=numpy.uint8)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j].isCoop:
                data[i,j] = [255,255,255] #white
            else:
                try:
                    nei = arr[i][j].nei
                    if nei == 'n':
                        data[i,j] = [255,153,204] #pink
                    elif nei == 'e':
                        data[i,j] = [102,102,255] #blue
                    elif nei == 's':
                        data[i,j] = [153,255,153] #green
                    elif nei == 'w':
                        data[i,j] = [255,204,153] #orange
                    else:
                        data[i,j] = [0,0,0]
                except:
                    data[i,j] = [100,100,100] #grey

    data = numpy.repeat(numpy.repeat(data,20,axis = 0),20,axis=1)
    image = Image.fromarray(data)
    image.save(name)


if __name__ == '__main__':
    arr = []
    for i in range(40):
        tmp = []
        for j in range(40):
            if (i + j) % 5 == 0:
                tmp.append(APlayer(True,0))
            elif (i + j) % 5 == 1:
                ap = APlayer(False,0)
                ap.nei = 'n'
                tmp.append(ap)
            elif (i + j) % 5 == 2:
                ap = APlayer(False,0)
                ap.nei = 'e'
                tmp.append(ap)
            elif (i + j) % 5 == 3:
                ap = APlayer(False,0)
                ap.nei = 'w'
                tmp.append(ap)
            else:
                ap = APlayer(False,0)
                ap.nei = 's'
                tmp.append(ap)

        arr.append(tmp)
    FromArr(arr,'000.png')
