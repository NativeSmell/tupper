import sys
import matplotlib.pyplot as plt
import numpy as np

def read_pgm(fileName = 'gitName.pbm'):
    f = open(fileName, 'rb')
    
    ext = f.readline().decode("utf-8").rstrip('\n')

    if not ext == 'P1':
        print('it\'s not PBM file!')
        sys.exit()

    width,height = f.readline().decode("utf-8").rstrip('\n').split(' ') 

    width = int(width)
    height = int(height)

    if width != 106 or height != 17:
        print('you need use a 106x17 PBM picture!')
        sys.exit()

    raster = np.zeros((height,width))
    
    for i in range(0,height):
        tmp = f.readline().decode("utf-8").rstrip('\n').split(' ')
        for j in range(0,width):
            raster[i][j] = int(tmp[j])

    f.close()
    
    return raster

def tupper(x,y,height):
    return .5 < ((y//height) // (2**(height*x + y%height))) % 2

def calculateFormulaOnPlot(K,height = 17, width = 106):

    for x in range(0,width):
        for yy in range(0,height):
            y = K + yy
            if tupper(x,y,height):
                plt.bar(left=x, bottom=yy, height=1, width=1, linewidth=0, color='black')

    plt.axis('scaled')
    
    buf = 2
    plt.xlim((-buf,width+buf))
    plt.ylim((-buf,height+buf))
    
    yticks = [ x for x in range(0,height+1,17)]

    plt.yticks(yticks, ['K']+['K + %d'%i for i in yticks][1:])
   
def calculateKFromRaster(raster = np.zeros((17,106))):
    
    bites = ''
    h,w = raster.shape

    for i in range(w-1,-1,-1):
        for j in range(0,h):
            bites += str(int(raster[j][i]))
    
    return int(bites,2) * 17 ,bites

if __name__ == '__main__':
    
    saveFlug = False
    path = 'gitName.pbm'

    if not 'path=' in sys.argv:
        print('Build plot from your image? [y/n]:', end = '')
        answer = input()

        if answer == 'y' or answer == 'Y':
            print('Enter path to your .PBM file:', end = '')
            path = input()

    K,bites = calculateKFromRaster(read_pgm(path))

    print('K: ' + str(K) + '\n')
    print('Bites: ' + bites + '\n')

    print('Show or save? [S/s]:', end = '')
    answer = input()

    if answer == 'S':
        calculateFormulaOnPlot(K)
        plt.show()

        print('Save this picture? [Y/N]:', end='')
        answer = input()

        if answer == 'Y' or answer == 'y':
            saveFlug = True

    if answer == 's' or saveFlug:
        print('How do you wanna call this picture? \'picture\' is difault name (pls don\'t write an extension):', end = '')
        name = input()
        if not name:
            name = 'picture'

        calculateFormulaOnPlot(K)
        plt.savefig(name + '.png')
