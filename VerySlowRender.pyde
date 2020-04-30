# Project Name: Very Slow Render
# Version: 0.0.1
# Dependencies: Processing v3.5.4 or higher
# 
# Author: Gimeron<gimeron@protonmail.com>


from pyVector import Vector3
from RMObjects import PointObject, SphereObject, PlainObject, BoxObject, RMWorld
from RMCamera import Camera


Debug = True           # Режим отладки
SaveImage = False


def my_range(numStart, numEnd, step):
    while numStart < numEnd:
        yield numStart
        numStart += step


world = RMWorld()


SceneImageWidth=192
SceneImageHeight=108

SaveImage = False

def setup():
    background(0)
    size(SceneImageWidth, SceneImageHeight)
    
    # Пополним мир объектами
    world.Objects.append( SphereObject(Vector3(-40,210,15), 40) )
    world.Objects[0].color=[240,96,32]
    world.Objects.append( BoxObject(Vector3(20,170,-25+2+8*0), Vector3(40,40,4), -0*PI/12,0,0) ) #1
    world.Objects[1].color=[0,240,0]
    world.Objects.append( BoxObject(Vector3(20,170,-25+2+8*1), Vector3(40,40,4), -1*PI/12,0,0) ) #2
    world.Objects[2].color=[80,240,0]
    world.Objects.append( BoxObject(Vector3(20,170,-25+2+8*2), Vector3(40,40,4), -2*PI/12,0,0) ) #3
    world.Objects[3].color=[160,240,0]
    world.Objects.append( BoxObject(Vector3(20,170,-25+2+8*3), Vector3(40,40,4), -3*PI/12,0,0) ) #4
    world.Objects[4].color=[240,240,0]
    world.Objects.append( BoxObject(Vector3(20,170,-25+2+8*4), Vector3(40,40,4), -4*PI/12,0,0) ) #5
    world.Objects[5].color=[240,160,0]
    world.Objects.append( BoxObject(Vector3(20,170,-25+2+8*5), Vector3(40,40,4), -5*PI/12,0,0) ) #6
    world.Objects[6].color=[240,80,0]
    world.Objects.append( BoxObject(Vector3(20,170,-25+2+8*6), Vector3(40,40,4), -6*PI/12,0,0) ) #7
    world.Objects[7].color=[240,0,0]
    # Земля
    world.Objects.append( PlainObject(Vector3(20,170,-25), 0, 0, 0) ) #8
    world.Objects[8].color=[96,240,32]
    # Камера
    world.Cameras.append( Camera(Vector3(-60, 40, 90)) )
    
    world.ShowProgress = True
    world.Debug = Debug
    
    
        
def draw():
    noLoop()
    background(0)
    
    t1=millis()
    
    mainCamera = world.Cameras[0]
    mainCamera.pitch = PI/2 + PI/6
    mainCamera.yaw = PI/6 + -PI/24
    mainCamera.viewAngle = PI/2.333
    
    mainCamera.stepCountLimit = 100
    mainCamera.minRange = 0.5
    
    
    renderImage1 = world.scan(mainCamera, [SceneImageWidth, SceneImageHeight])
    image(renderImage1,0,0)
    
    
    t2=millis()
    if Debug: print("Render time: " + str(float(t2-t1)/1000) )
    time = "" + ("0000"+str(year()))[-4:] + "." + ("00"+str(month()))[-2:] + "." + ("00"+str(day()))[-2:] + "_" + ("00"+str(hour()))[-2:] + "." + ("00"+str(minute()))[-2:] + "." + ("00"+str(second()))[-2:]
    if SaveImage == True: save( "output/render_output" + "_" + time + "_" + str(width)+"x"+str(height) + ".png" )
    
    
        
