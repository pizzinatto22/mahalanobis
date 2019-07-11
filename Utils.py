import math
import numpy as np
from PyQt4 import QtGui

def euclidean(image, samples):
    qtSamples = len(samples)

    avgRed   = 0
    avgGreen = 0
    avgBlue  = 0
    for px in samples:
        avgRed   += QtGui.qRed(px)
        avgGreen += QtGui.qGreen(px)
        avgBlue  += QtGui.qBlue(px)
    
    avgRed   /= qtSamples
    avgGreen /= qtSamples
    avgBlue  /= qtSamples

    w = image.width()
    h = image.height()
    bitmap = []
    avg    = 0

    for x in range(0, w):
        row = []
        for y in range(0, h):
            px = image.pixel(x, y)

            r = QtGui.qRed(px)
            g = QtGui.qGreen(px)
            b = QtGui.qBlue(px)

            distance = math.sqrt((r - avgRed) ** 2 + (g - avgGreen) ** 2 + (b - avgBlue) ** 2)
        
            avg += distance

            row.append(distance)

        bitmap.append(row)

    avg /= (w * h)

    return {'data': bitmap,
            'avg' : int(avg)}


def mahalanobis(image, samples):
    qtSamples = len(samples)

    avgRed   = 0
    avgGreen = 0
    avgBlue  = 0
    for px in samples:
        avgRed   += QtGui.qRed(px)
        avgGreen += QtGui.qGreen(px)
        avgBlue  += QtGui.qBlue(px)
    
    avgRed   /= qtSamples
    avgGreen /= qtSamples
    avgBlue  /= qtSamples

    rr = 0  #red   and red   [0,0]
    rg = 0  #red   and green [0,1]
    rb = 0  #red   and blue  [0,2]
    gg = 0  #green and green [1,1]
    gb = 0  #green and blue  [1,2]
    bb = 0  #blue  and blue  [2,2]

    for px in samples:
        r = QtGui.qRed(px)
        g = QtGui.qGreen(px)
        b = QtGui.qBlue(px)

        dr = r - avgRed
        dg = g - avgGreen
        db = b - avgBlue

        rr += dr ** 2
        rg += dr * dg
        rb += dr * db

        gg += dg ** 2
        gb += dg * db

        bb += db ** 2


    #inverse covariance matrix
    A = np.array([[rr, rg, rb], 
                  [rg, gg, gb], 
                  [rb, gb, bb]])

    Ainv = np.linalg.inv(A)

    w = image.width()
    h = image.height()
    bitmap = []

    avg = 0

    for x in range(0, w):
        row = []
        for y in range(0, h):
            px = image.pixel(x, y)

            r = QtGui.qRed(px)
            g = QtGui.qGreen(px)
            b = QtGui.qBlue(px)

            vector = [r - avgRed,
                      g - avgGreen,
                      b - avgBlue]

            vector1 = np.array(vector)

            vector2 = np.array([[vector[0]],
                                [vector[1]],
                                [vector[2]]])

            distance = abs(np.dot(np.dot(vector1, Ainv), vector2)[0])
            normalized = int(math.exp(-distance) * 255)

            #big distances generate small values (because exp(-x) = 1/e^x)
            #but we need big distances near to white color, and small distances near to black color,
            #so, we need to invert our normalized value
            normalized = 255 - normalized
            
            row.append(normalized)
            avg += normalized
        
        bitmap.append(row)

    avg /= (w * h)

    return {'data': bitmap,
            'avg' : int(avg)}

def generateImage(data, threshold, grey):
    w = len(data)
    h = len(data[0])

    image = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)

    for x in range(w):
        for y in range(h):
            c = data[x][y]  
            if c <= threshold:
                if grey:
                    finalColor = QtGui.QColor(c, c, c).rgb()
                else:
                    finalColor = QtGui.QColor(0, 0, 0).rgb()
            else:
                finalColor = QtGui.QColor(255, 255, 255).rgb()

            image.setPixel(x, y, finalColor)                

    return image
