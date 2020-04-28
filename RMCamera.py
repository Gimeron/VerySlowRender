from pyVector import Vector3

class Camera():
    def __init__(self, pos=Vector3(0,0,0), roll=0, pitch=0, yaw=0, viewAngle=PI/4, aspectRatio=1.6, stepCountLimit=100, distLimit=1000, minRange=0.25, lightPower=255):
        self.pos   = pos
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw
        self.viewAngle = viewAngle
            # ViewAngle:
            # 180 - 80  fish
            #  80 - 50  width
            #  50 - 40  normal
            #  35 - 18  tele
            #     < 18  supertele
        self.aspectRatio = aspectRatio
        
        # Render config
        self.stepCountLimit = stepCountLimit
        self.distLimit = distLimit
        self.minRange = minRange
        self.lightPower = lightPower
