# Project Name: Very Slow Render
# Version: 0.0.1
# Dependencies: Processing v3.5.4 or higher
# 
# Author: Gimeron<gimeron@protonmail.com>


from pyVector import Vector3
from RMObjects import PointObject, SphereObject, PlainObject, BoxObject, RoundedBoxObject, RMWorld
from RMCamera import Camera


Debug = True           # Режим отладки


def my_range(numStart, numEnd, step):
    while numStart < numEnd:
        yield numStart
        numStart += step


world = RMWorld()


SceneImageWidth=int(192*1)
SceneImageHeight=int(108*1)

SaveImage = True

def setup():
    background(0)
    size(SceneImageWidth, SceneImageHeight)
    
    # Пополним мир объектами
    world.Objects.append( SphereObject(Vector3(-40,210,15), 40) )
    world.Objects[0].color=[240,120,60]
    world.Objects.append( RoundedBoxObject(Vector3(20,170,-25+2+8*0), Vector3(40,40,4), 2, -0*PI/12,0,0) ) #1
    world.Objects[1].color=[255,255,255]
    world.Objects.append( RoundedBoxObject(Vector3(20,170,-25+2+8*1), Vector3(40,40,4), 2, -1*PI/12,0,0) ) #2
    world.Objects[2].color=[240,80,240]
    world.Objects.append( RoundedBoxObject(Vector3(20,170,-25+2+8*2), Vector3(40,40,4), 2, -2*PI/12,0,0) ) #3
    world.Objects[3].color=[80,80,240]
    world.Objects.append( RoundedBoxObject(Vector3(20,170,-25+2+8*3), Vector3(40,40,4), 2, -3*PI/12,0,0) ) #4
    world.Objects[4].color=[80,240,240]
    world.Objects.append( RoundedBoxObject(Vector3(20,170,-25+2+8*4), Vector3(40,40,4), 2, -4*PI/12,0,0) ) #5
    world.Objects[5].color=[80,240,80]
    world.Objects.append( RoundedBoxObject(Vector3(20,170,-25+2+8*5), Vector3(40,40,4), 2, -5*PI/12,0,0) ) #6
    world.Objects[6].color=[240,240,80]
    world.Objects.append( RoundedBoxObject(Vector3(20,170,-25+2+8*6), Vector3(40,40,4), 2, -6*PI/12,0,0) ) #7
    world.Objects[7].color=[240,80,80]
    # Земля
    world.Objects.append( PlainObject(Vector3(20,170,-25), 0, 0, 0) ) #8
    world.Objects[8].color=[80,120,60]
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
    mainCamera.viewAngle = PI/2.333/1.0
    
    mainCamera.stepCountLimit = 200
    mainCamera.minRange = 0.25
    
    
    renderImage1 = world.scan(mainCamera, [SceneImageWidth, SceneImageHeight])
    image(renderImage1,0,0)
    
    
    t2=millis()
    if Debug: print("Render time: " + str(float(t2-t1)/1000) )
    time = "" + ("0000"+str(year()))[-4:] + "." + ("00"+str(month()))[-2:] + "." + ("00"+str(day()))[-2:] + "_" + ("00"+str(hour()))[-2:] + "." + ("00"+str(minute()))[-2:] + "." + ("00"+str(second()))[-2:]
    if SaveImage == True: save( "output/render_output" + "_" + time + "_" + str(width)+"x"+str(height) + ".png" )
    
    
        
