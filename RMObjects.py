from pyVector import Vector3
from RMCamera import Camera



def my_range(numStart, numEnd, step):
    while numStart < numEnd:
        yield numStart
        numStart += step



class RMWorld():
    def __init__(self):
        self.Objects=[]
        self.Cameras=[]
        self.Lights=[]
        self.pixelPerMeter = 100
        self.ShowProgress = False
        self.Debug = False

    def getDist(self, pointTest, listObjects=[], distLimit=1000.0):
        nearObject = False             # or RMObject
        minDist = distLimit * 100.0
        for i in listObjects:
            curDist = i.getDist(pointTest)
            if curDist < minDist:
                minDist = curDist
                nearObject = i
        return (minDist, i)      # distanse and object

    def raymarch(self, startPoint, vectorDirect, listObjects=[], curCam=Camera()):
        p = startPoint.copy()   # start from startpoint
        testObject = False
        for _step in range(0, curCam.stepCountLimit):
            distToObject, testObject = self.getDist(p, listObjects, curCam.distLimit)
            if (distToObject > curCam.distLimit):
                return (0, False)          
            if (distToObject < curCam.minRange):
                return (p, testObject)         # found object
            shiftVector = vectorDirect.copy()
            shiftVector.setMag(distToObject)
            p.add(shiftVector)
        return (0, False)  # if not found
        
    def scan(self, curCam, imageSize=[64,64]):
        curCam.aspectRatio = float(imageSize[0])/float(imageSize[1])
        
        camViewAngleX = curCam.viewAngle
        camViewAngleY = curCam.viewAngle / curCam.aspectRatio
        
        if self.Debug: print(imageSize)
        camImage = createImage(imageSize[0], imageSize[1], RGB)
        camImage.loadPixels()
        
        # run
        imgY = 0
        imgX = 0
        pxIndex = 0
        for aY in my_range(-camViewAngleY/2, camViewAngleY/2, camViewAngleY/float(imageSize[1])):      # rows
            imgX = 0
            for aX in my_range(-camViewAngleX/2, camViewAngleX/2, camViewAngleX/float(imageSize[0])):  # cols
                vectorDirect = Vector3(0, 0, 1) 
                vectorDirect.rotateY(aX)
                vectorDirect.rotateEuler(curCam.roll, curCam.pitch + aY, curCam.yaw)
                # ready and go
                startPoint = curCam.pos.copy()
                
                pointOfObject, nearObject = self.raymarch(startPoint, vectorDirect, self.Objects, curCam)
                if nearObject != False:   # if found
                    vectorToPoint = pointOfObject.copy()
                    vectorToPoint.sub(startPoint)
                    distToPoint = vectorToPoint.mag()
                else:                      # if not found
                    distToPoint = curCam.distLimit * 2.0   #  )
                                
                pxIndex = (imgY-1) * camImage.width + (imgX-1)
                
                if ((pxIndex % 500) == 0) and self.ShowProgress:
                    print("Lines: "+str(imgY)+"/"+str(imageSize[1]) + "   Rays: "+str(pxIndex)+"/"+str(imageSize[0]*imageSize[1]) + "   " + str( imgY*10000/imageSize[1]/100.0) + "%")
                pxColor = int(curCam.lightPower/(distToPoint/self.pixelPerMeter)**2)
                #TODO: Check array overflow
                camImage.pixels[pxIndex] = color( pxColor, pxColor, pxColor  )
                imgX +=1
            imgY +=1
        camImage.updatePixels()
        return camImage



class PointObject():
    def __init__(self, pos=Vector3(0, 0, 0)):
        self.pos=pos
        
    def getDist(self, pointTest=Vector3(0, 0, 0)):
        return ((pointTest.x-self.pos.x)**2 + (pointTest.y-self.pos.y)**2 + (pointTest.z-self.pos.z)**2)**0.5


class SphereObject(PointObject):
    def __init__(self, pos=Vector3(0, 0, 0), radius=1):
        PointObject.__init__(self, pos)
        self.radius = radius
        
    def getDist(self, pointTest=Vector3(0, 0, 0)):
        distToCenter = ((pointTest.x-self.pos.x)**2 + (pointTest.y-self.pos.y)**2 + (pointTest.z-self.pos.z)**2)**0.5
        return (distToCenter - self.radius)


class PlainObject(PointObject):
    def __init__(self, pos=Vector3(0, 0, 0), roll=0, pitch=0, yaw=0):
        PointObject.__init__(self, pos)
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw
    
    def getDist(self, pointTest=Vector3(0, 0, 0)):
        _p = pointTest.copy()
        _p.sub(self.pos)
        _p.rotateEuler(-self.yaw, -self.pitch, -self.roll)
        return (_p.z - self.pos.z)


class BoxObject(PointObject):
    def __init__(self, pos=Vector3(0, 0, 0), size=Vector3(1, 1, 1), roll=0, pitch=0, yaw=0):
        PointObject.__init__(self, pos)
        self.size=size
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw

    def getDist(self, pointTest=Vector3(0, 0, 0)):
        _p = pointTest.copy()
        _p.sub(self.pos)
        _p.rotateEuler(-self.yaw, -self.pitch, -self.roll)
        
        _p.x = abs(_p.x)
        _p.y = abs(_p.y)
        _p.z = abs(_p.z)
        _q = _p.copy()
        _q.sub(self.size)
        
        qo = _q.copy()
        qo.x = max(qo.x, 0.0)
        qo.y = max(qo.y, 0.0)
        qo.z = max(qo.z, 0.0)
        
        return qo.mag() + min(max(qo.x, qo.y, qo.z), 0.0)
