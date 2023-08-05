import numpy
import math
import hashlib


class Leech:

    A=numpy.array([[0,0,0,0,0,0,0,0],[4,0,0,0,0,0,0,0],[2,2,2,2,0,0,0,0],[-2,2,2,2,0,0,0,0],[2,2,0,0,2,2,0,0],[-2,2,0,0,2,2,0,0],[2,2,0,0,0,0,2,2],[-2,2,0,0,0,0,2,2],[2,0,2,0,2,0,2,0],[-2,0,2,0,2,0,2,0],[2,0,2,0,0,2,0,2],[-2,0,2,0,0,2,0,2],[2,0,0,2,2,0,0,2],[-2,0,0,2,2,0,0,2],[2,0,0,2,0,2,2,0],[-2,0,0,2,0,2,2,0]])
    T=numpy.array([[0,0,0,0,0,0,0,0],[2,2,2,0,0,2,0,0],[2,2,0,2,0,0,0,2],[2,0,2,2,0,0,2,0],[0,2,2,2,2,0,0,0],[2,2,0,0,2,0,2,0],[2,0,2,0,2,0,0,2],[2,0,0,2,2,2,0,0],[-3,1,1,1,1,1,1,1],[3,-1,-1,-1,1,-1,1,1],[3,-1,1,-1,1,1,1,-1],[3,1,-1,-1,1,1,-1,1],[3,1,1,1,1,-1,-1,-1],[3,-1,1,1,-1,1,-1,1],[3,1,-1,1,-1,1,1,-1],[3,1,1,-1,-1,-1,1,1]])
    table=numpy.array([[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],[1,0,3,2,5,4,7,6,9,8,11,10,13,12,15,14],[2,3,0,1,6,7,4,5,10,11,8,9,14,15,12,13],[3,2,1,0,7,6,5,4,11,10,9,8,15,14,13,12],[4,5,6,7,0,1,2,3,12,13,14,15,8,9,10,11],[5,4,7,6,1,0,3,2,13,12,15,14,9,8,11,10],[6,7,4,5,2,3,0,1,14,15,12,13,10,11,8,9],[7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8],[8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7],[9,8,11,10,13,12,15,14,1,0,3,2,5,4,7,6],[10,11,8,9,14,15,12,13,2,3,0,1,6,7,4,5],[11,10,9,8,15,14,13,12,3,2,1,0,7,6,5,4],[12,13,14,15,8,9,10,11,4,5,6,7,0,1,2,3],[13,12,15,14,9,8,11,10,5,4,7,6,1,0,3,2],[14,15,12,13,10,11,8,9,6,7,4,5,2,3,0,1],[15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]])

    @staticmethod
    def round(x,t):
        x=round(x)
        m=(x%t+t)%t
        if m <= t/2:
            return x-m
        else:
            return x-m+t

    @staticmethod
    def decode4D8(y,scale):
        x=[]
        for t in y:
            x.append(Leech.round(t,scale*4))

        if sum(x)%(8*scale)==0:
            return x

        mx=-1
        pos=0
        for i in range(8):
            if abs(x[i]-y[i])>mx:
                pos=i
                mx=abs(x[i]-y[i])
        if x[pos]>y[pos]:
            x[pos]-=4*scale
        else:
            x[pos]+=4*scale
        return x
    
    @staticmethod
    def decode4E8(y,scale):
        half=numpy.ones(8).astype(int)*2*scale
        x1=Leech.decode4D8(y,scale)
        x2=Leech.decode4D8(y-half,scale)+half
        if numpy.linalg.norm(x1-y)<numpy.linalg.norm(x2-y):
            return x1
        return x2
    
    @staticmethod
    def decode(y,scale):
        pre=numpy.empty((16,16,24),dtype = 'int')
        for a in range(0,16):
            for t in range(0,16):
                AT=(Leech.A[a]+Leech.T[t])*scale
                y1=y[0:8]-AT
                y2=y[8:16]-AT
                y3=y[16:24]-AT
                x1=Leech.decode4E8(y1, scale)+AT
                x2=Leech.decode4E8(y2, scale)+AT
                x3=Leech.decode4E8(y3, scale)+AT
                pre[a,t]=numpy.concatenate((x1,x2,x3))

        ans=y
        mn=2**60
        for a in range(0,16):
            for b in range(0,16):
                c=Leech.table[a][b]
                for t in range(0,16):
                    x1=pre[a,t][0:8]
                    x2=pre[b,t][8:16]
                    x3=pre[c,t][16:24]
                    x=numpy.concatenate((x1,x2,x3))
                    d=numpy.linalg.norm(x-y) 
                    if d<mn:
                        mn=d
                        ans=x 
        return ans

    @staticmethod    
    def decode_m(y,scale,m):
        out=numpy.array([]).astype(int)
        for i in range(m):
            out=numpy.append(out,Leech.decode(y[i*24:i*24+24],scale))
        return out


class SS:

    def __init__(self,n,t):
        self.n=n
        self.t=t 
        self.scale=int(t*(2**20))

    def padding(self,y):
        num=(len(y)+23)//24
        y2=numpy.zeros(num*24).astype(int)
        y2[0:len(y)]=y
        return y2

    def Gen(self,w):
        w=self.padding(w)
        v=Leech.decode_m(w,self.scale,len(w)//24)
        s=v-w
        return s

    def Rec(self,s,w_):
        w_=self.padding(w_)
        w=Leech.decode_m(w_+s,self.scale,len(w_)//24)-s
        return w[0:self.n]


class FuzzyExtractor:

    def __init__(self,n,t):
        self.ss=SS(n,t)
        self.scale=2**20
    
    def Gen(self,w): 
        w=numpy.rint(w*self.scale).astype(int)
        P=self.ss.Gen(w)
        hash=hashlib.sha256()
        hash.update(str(w).encode())
        R=hash.digest()
        return (R,P)

    def Rep(self,P,w_): 
        w_=numpy.rint(w_*self.scale).astype(int)
        w=self.ss.Rec(P,w_)
        hash=hashlib.sha256()
        hash.update(str(w).encode())
        R=hash.digest()
        return R

