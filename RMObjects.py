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
        self.pixelPerMeter = 100.0
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
        return (minDist, nearObject)      # distanse and object

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
        pxIndex = 0
        for imgY in range(imageSize[1]):
            aY = -camViewAngleY/2 + camViewAngleY * (float(imgY)/imageSize[1])
            for imgX in range(imageSize[0]):
                aX = -camViewAngleX/2 + camViewAngleX * (float(imgX)/imageSize[0])
                vectorDirect = Vector3(0, 0, 1) 
                vectorDirect.rotateY(aX)
                vectorDirect.rotateEuler(curCam.roll, curCam.pitch + aY, curCam.yaw)
                # ready to let the beem
                startPoint = curCam.pos.copy()
                
                pointOfObject, nearObject = self.raymarch(startPoint, vectorDirect, self.Objects, curCam)
                if nearObject != False:   # if found
                    # calculate distance to the point
                    vectorToPoint = pointOfObject.copy()
                    vectorToPoint.sub(startPoint)
                    distToPoint = vectorToPoint.mag()     # near
                    # calculate the normal vector (gradient around the point)
                    # need test 4 point
                    eps = 0.1 # point neighborhood size
                    z0, someObject = self.getDist(Vector3(pointOfObject.x, pointOfObject.y, pointOfObject.z), self.Objects, curCam.distLimit)
                    z1, someObject = self.getDist(Vector3(pointOfObject.x + eps, pointOfObject.y, pointOfObject.z), self.Objects, curCam.distLimit)
                    z2, someObject = self.getDist(Vector3(pointOfObject.x, pointOfObject.y + eps, pointOfObject.z), self.Objects, curCam.distLimit)
                    z3, someObject = self.getDist(Vector3(pointOfObject.x, pointOfObject.y, pointOfObject.z + eps), self.Objects, curCam.distLimit)
                    gradient = Vector3(z1-z0, z2-z0, z3-z0)
                    normalVector = gradient.copy()
                    normalVector.normalize() # ready normal vector will be used in the calculation of the color
                    
                else:                      # if not found
                    distToPoint = curCam.distLimit * 2.0  # too far
                    
                pxIndex = imgY * camImage.width + imgX
                
                # progress log
                if ((pxIndex % 500) == 0) and self.ShowProgress:
                    print("Lines: "+str(imgY)+"/"+str(imageSize[1]) + "   Rays: "+str(pxIndex)+"/"+str(imageSize[0]*imageSize[1]) + "   " + str( imgY*10000/imageSize[1]/100.0) + "%")
                
                # calc point color
                if nearObject != False:
                    hitDirectionVector = vectorDirect.copy()
                    hitDirectionVector.setMag(-1.0)
                    lightDirectionVector = Vector3(0,0,1)
                    normalDirectionVector = normalVector.copy()
                    
                    # pxLight = float(curCam.lightPower/(distToPoint/self.pixelPerMeter)**2) # depth map
                    pxLight = normalDirectionVector.dot(lightDirectionVector) # return -1.0 .. 1.0 from lamp
                    # pxLight = normalDirectionVector.dot(hitDirectionVector) # return -1.0 .. 1.0 from camera
                    
                    pxLight = pxLight * 127.0 + 127.0     # soft light
                    
                    pxColor = [nearObject.color[0], nearObject.color[1], nearObject.color[2]]
                    # pxColor=[255,255,255]
                else:
                    pxColor = [255, 255, 255]
                
                camImage.pixels[pxIndex] = color( pxLight*float(pxColor[0]/255.0), pxLight*float(pxColor[1]/255.0), pxLight*float(pxColor[2]/255.0)  )
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
        self.type = "Sphere"
        self.radius = radius
        self.color = [255,255,255]
        
    def getDist(self, pointTest=Vector3(0, 0, 0)):
        distToCenter = ((pointTest.x-self.pos.x)**2 + (pointTest.y-self.pos.y)**2 + (pointTest.z-self.pos.z)**2)**0.5
        return (distToCenter - self.radius)


class PlainObject(PointObject):
    def __init__(self, pos=Vector3(0, 0, 0), roll=0, pitch=0, yaw=0):
        PointObject.__init__(self, pos)
        self.type = "Plain"
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw
        self.color = [255,255,255]
    
    def getDist(self, pointTest=Vector3(0, 0, 0)):
        _p = pointTest.copy()
        _p.sub(self.pos)
        _p.rotateEuler(-self.yaw, -self.pitch, -self.roll)
        return (_p.z - self.pos.z)


class BoxObject(PointObject):
    def __init__(self, pos=Vector3(0, 0, 0), size=Vector3(1, 1, 1), roll=0, pitch=0, yaw=0):
        PointObject.__init__(self, pos)
        self.type = "Box"
        self.size=size
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw
        self.color = [255,255,255]

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


class RoundedBoxObject(PointObject):
    def __init__(self, pos=Vector3(0, 0, 0), size=Vector3(1, 1, 1), radius=0, roll=0, pitch=0, yaw=0):
        PointObject.__init__(self, pos)
        self.type = "Box"
        self.size=size
        self.radius = radius
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw
        self.color = [255,255,255]

    def getDist(self, pointTest=Vector3(0, 0, 0)):
        _p = pointTest.copy()
        _p.sub(self.pos)
        _p.rotateEuler(-self.yaw, -self.pitch, -self.roll)
        
        _p.x = abs(_p.x)
        _p.y = abs(_p.y)
        _p.z = abs(_p.z)
        _q = _p.copy()
        _q.sub(self.size)
        
        _q.x += self.radius
        _q.y += self.radius
        _q.z += self.radius
        
        qo = _q.copy()
        qo.x = max(qo.x, 0.0)
        qo.y = max(qo.y, 0.0)
        qo.z = max(qo.z, 0.0)
        
        return qo.mag() + min(max(qo.x, qo.y, qo.z), 0.0) - self.radius
