import numpy as np
import copy
import math
import random
import pylab as pl


#DEB Dataset
class Individual():
    def __init__(self,x):
        self.x=x
        self.NumX=len(x)

        f1=float(x[0]/10000)
        h=float(1+x[1]/1000)
        f2=h*(1-(f1/h)**2-(f1/h)*np.sin(8*np.pi*f1))
        self.f=[f1,f2]    #multiobjective function
def Initial(N):
    #initialize the population and the weight vector lambda list
    P=[]
    Lamb=[]
    for i in range(N):
        temp=[]
        P.append(Individual([random.random()*10000,random.random()*10000]))
        temp.append(float(i)/(N))
        temp.append(1.0-float(i)/(N))
        Lamb.append(temp)

    return P,Lamb


#cal x dominated y or not
def Dominate(x,y,min=True):
    if min:

        for i in range(len(x.f)):
            if x.f[i]>y.f[i]:
                return False


        return True
    else:
        for i in range(len(x.f)):
            if x.f[i]<y.f[i]:
                return False
        return True
def Tchebycheff(x,lamb,z):
    #Tchebycheff approach operator

    temp=[]
    for i in range(len(x.f)):
        temp.append(np.abs(x.f[i]-z[i])*lamb[i])
    return np.max(temp)
def Neighbor(Lamb,T):
    #Lambda list,numbers of neighbors is T
    B=[]
    for i in range(len(Lamb)):
        temp=[]
        for j in range(len(Lamb)):
            distance=np.sqrt((Lamb[i][0]-Lamb[j][0])**2+(Lamb[i][1]-Lamb[j][1])**2)
            temp.append(distance)
        l=np.argsort(temp)
        B.append(l[:T])
    return B
def BestValue(P):
    #get the bestvalues of each function,which used as the reference point
    #if goal for function is minimazaton,z is the minimize values
    #P:population
    best=[]
    for i in range(len(P[0].f)):
        best.append(P[0].f[i])
    for i in range(1,len(P)):
        for j in range(len(P[i].f)):
            if P[i].f[j]<best[j]:
                best[j]=P[i].f[j]

    return best

def integerToString(numero,numero2):
    '''
        int numbers transformed to Binary as String

    '''
    cadenas = []
    cadenas.append(bin(numero))
    cadenas.append(bin(numero2))
    #Limpiar las cadenas
    cadenas[0] = cadenas[0].replace("0b","")
    cadenas[1] = cadenas[1].replace("0b","")
    if (len(cadenas[0]) > len(cadenas[1])):
        cadenas[1] = ("0"*(len(cadenas[0])-len(cadenas[1]))) + cadenas[1]
    else:
        cadenas[0] = ("0"*(len(cadenas[1])-len(cadenas[0]))) + cadenas[0]
    return cadenas[0], cadenas[1]

def stringToInteger(cadena):
    '''
       transformed Binary to Integer
       the two functions are used for genetic operation
                '''
    decimal = 0
    for i,v in enumerate(cadena):
        if(v == '1'):
            decimal = decimal + math.pow(2,len(cadena)-1-i)
    return decimal
def GeneticOperaton(a,b):
    #genetic operation to a and b,including crossover and muate
    tempx=[]
    for i in range(len(a.x)):
        str1,str2=integerToString(int(a.x[i]),int(b.x[i]))
        R = random.randint(0, len(str1) - 1)
        new_x=stringToInteger(str1[:R] + str2[R:])
        if new_x>10000:
            new_x=10000
        tempx.append(new_x)
    r=random.random()
    if r>0.5:
        return muate(a),Individual(tempx)
    else:

        return muate(b),Individual(tempx)
def muate(c):
    l=len(c.x)
    r=random.randint(0,l-1)
    str1, str2 = integerToString(int(c.x[r]), int(c.x[r]))
    R = random.randint(0, len(str1) - 1)
    if str1[R]=='0':
        str1=str1[:R]+'1'+str1[R+1:]
    else:
        str1=str1[:R]+'0'+str1[R+1:]

    new_x=stringToInteger(str1)
    if new_x>10000:
        c.x[r]=10000
    else:
        c.x[r]=new_x
    return Individual(c.x)




def MOEAD(N,T):
    #the main algorithm
    #N:population numbers
    #T:the number of neighborhood of each weight vector
    p,Lamb=Initial(N)
    B=Neighbor(Lamb,T)
    z=BestValue(p)
    EP=[]
    t=0
    while(t<20):
        t+=1
        print 'PF number:',len(EP)
        for i in range(N):
            k = random.randint(0, T - 1)
            l = random.randint(0, T - 1)
            y1,y2 = GeneticOperaton(p[B[i][k]], p[B[i][l]])
            if Dominate(y1,y2):
                y=y1
            else:
                y=y2
            for j in range(len(z)):
                if y.f[j] < z[j]:
                    z[j] = y.f[j]
            for j in range(len(B[i])):
                Ta = Tchebycheff(p[B[i][j]], Lamb[B[i][j]], z)
                Tb = Tchebycheff(y, Lamb[B[i][j]], z)
                if Tb < Ta:
                    p[B[i][j]] = y
            if EP == []:
                EP.append(y)
            else:
                dominateY = False
                rmlist=[]
                for j in range(len(EP)):
                    if Dominate(y, EP[j]):
                        rmlist.append(EP[j])
                    elif Dominate(EP[j], y):
                        dominateY = True

                if dominateY == False:
                    EP.append(y)
                    for j in range(len(rmlist)):
                        EP.remove(rmlist[j])

    x = []
    y = []
    for i in range(len(EP)):
        x.append(EP[i].f[0])
        y.append(EP[i].f[1])
    pl.plot(x, y, '*')
    pl.xlabel('f1')
    pl.ylabel('f2')
    pl.show()

if __name__ == '__main__':
    MOEAD(1500,10)




















