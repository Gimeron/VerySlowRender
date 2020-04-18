class Vector3():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return str([self.x, self.y, self.z])
        
    def copy(self):
        return Vector3(self.x, self.y, self.z)
    
    def mag(self):
        return ((self.x)**2 + (self.y)**2 + (self.z)**2)**0.5
    
    def magSq(self):
        return ((self.x)**2 + (self.y)**2 + (self.z)**2)
    
    def dist(self, vectB):
        return ((vectB.x - self.x)**2 + (vectB.y - self.y)**2 + (vectB.z - self.z)**2)**0.5
    
    def normalize(self):
        vectLen = self.mag()
        self.x /= vectLen
        self.y /= vectLen
        self.z /= vectLen
        return
    
    def setMag(self, newMag=0):
        self.normalize()
        self.mult(newMag)
        return
    
    def limit(self, maxLen):
        vectLen = self.mag()
        if maxLen < vectLen:
            self.setMag(maxLen)
        return
    
    def lerp(self, vectB, amt=0.0):
        self.x = (1-amt)*self.x + amt*vectB.x
        self.y = (1-amt)*self.y + amt*vectB.y
        self.z = (1-amt)*self.z + amt*vectB.z
        return
    
    def add(self, vectB):
        self.x += vectB.x
        self.y += vectB.y
        self.z += vectB.z
        return
        
    def sub(self, vectB):
        self.x -= vectB.x
        self.y -= vectB.y
        self.z -= vectB.z
        return
        
    def mult(self, scalar=1):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return

    def div(self, scalar=1):
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return
    
    def dot(self, vectB):
        '''
        dot = x1*x2 + y1*y2 + z1*z2
        '''
        return (self.x*vectB.x + self.y*vectB.y + self.z*vectB.z)
    
    def cross(self, vectB):
        '''
               |  i,  j,  k |
        newV = | x1, y1, z1 | = | (y1*z2 - y2*z1)*i,  (z1*x2 - z2*x1)*j,  (x1*y2 - x2*y1)*k |
               | x2, y2, z2 |
        '''
        vectCross = Vector3( (self.y*vectB.z - vectB.y*self.z), (self.z*vectB.x - vectB.z*self.x), (self.x*vectB.y - vectB.x*self.y) )
        return vectCross
    
    def angleBetween(self, vectB):
        '''
        V1.normalize()  dot  V2.normolize()         EQ cos(angle)
        V1.normalize() cross V2.normolize()     len EQ sin(angle)
        '''
        v1 = self.copy()
        v2 = vectB.copy()
        v1.normalize()
        v2.normalize()
        cosA = v1.dot(v2) # cos(a)
        return acos(cosA)
    
    def rotateX(self, angle=0):
        # rotate in YZ (X fixed)
        M = [[1,          0,           0],
             [0, cos(angle), -sin(angle)],
             [0, sin(angle),  cos(angle)]]
        x = self.x*M[0][0] + self.y*M[1][0] + self.z*M[2][0]
        y = self.x*M[0][1] + self.y*M[1][1] + self.z*M[2][1]
        z = self.x*M[0][2] + self.y*M[1][2] + self.z*M[2][2]
        self.x = x
        self.y = y
        self.z = z
        return 0
    
    def rotateY(self, angle=0):
        # rotate in ZX (Y fixed)
        M = [[ cos(angle), 0, sin(angle)],
             [          0, 1,          0],
             [-sin(angle), 0, cos(angle)]]
        x = self.x*M[0][0] + self.y*M[1][0] + self.z*M[2][0]
        y = self.x*M[0][1] + self.y*M[1][1] + self.z*M[2][1]
        z = self.x*M[0][2] + self.y*M[1][2] + self.z*M[2][2]
        self.x = x
        self.y = y
        self.z = z
        return 0
    
    def rotateZ(self, angle=0):
        # rotate in XY (Z fixed)
        M = [[cos(angle), -sin(angle), 0],
             [sin(angle),  cos(angle), 0],
             [         0,           0, 1]]
        x = self.x*M[0][0] + self.y*M[1][0] + self.z*M[2][0]
        y = self.x*M[0][1] + self.y*M[1][1] + self.z*M[2][1]
        z = self.x*M[0][2] + self.y*M[1][2] + self.z*M[2][2]
        self.x = x
        self.y = y
        self.z = z
        return 0
    
    def rotateEuler(self, roll, pitch, yaw):
        # Roll, Pitch, Yaw
        self.rotateZ(roll)
        self.rotateX(pitch)
        self.rotateZ(yaw)
        return 0
    
