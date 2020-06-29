from PIL import Image, ImageDraw, ImageFont
from player import APlayer,Player
import numpy
import sys, os
from pathlib import Path


def FromArr_png(arr,name):
    data = numpy.zeros((arr.shape[0],arr.shape[1],3), dtype=numpy.uint8)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if not arr[i,j].isCoop:
                data[i,j] = [100,100,100] #grey
            else:
                try:
                    nei = arr[i,j].nei
                    if nei == 'n':
                        data[i,j] = [255,221,238] #pink
                    elif nei == 'e':
                        data[i,j] = [188,188,255] #blue
                    elif nei == 's':
                        data[i,j] = [210,255,210] #green
                    elif nei == 'w':
                        data[i,j] = [255,233,210] #orange
                    else:
                        data[i,j] = [0,0,0]

                    if not arr[i,j].strD:
                        data[i,j] = [255,255,255] #white

                except:
                    data[i,j] = [255,255,255] #white 

    data = numpy.repeat(numpy.repeat(data,20,axis = 0),20,axis=1)
    image = Image.fromarray(data)

    textimg = Image.new('RGB',(image.width,50),color = 'white')
    d = ImageDraw.Draw(textimg)
    fnt = ImageFont.truetype('arial.ttf', size = 35)

    towrite = name.split('/')[-1]
    d.text((100,10),towrite,font = fnt, fill = (0,0,0))
    wholeimg = Image.new('RGB',(image.width,image.height + textimg.height))
    wholeimg.paste(image,(0,0))
    wholeimg.paste(textimg,(0,image.height))

    if name.find('/') > -1:
        Path(name.split('/')[0]).mkdir(parents=True, exist_ok=True)
    
    wholeimg.save(name + '.png')

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
    FromArr_png(numpy.array(arr),'000')
