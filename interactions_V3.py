#!/usr/bin/env python3
 
import time

import anki_vector
from anki_vector.util import degrees
from anki_vector.events import Events

from anki_vector.objects import CustomObjectMarkers, CustomObjectTypes
from anki_vector.faces import Face

import json
import functools
import os


with open('markers.json', 'r') as f:
    mapping = json.load(f)

nextScan = True


def handle_object_appeared(robot, event_type, event, evt):
    global nextScan
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
#    print(f"--------- Vector started seeing an object --------- \n{evt.obj}")
    print("--------- Vector started seeing an object ---------")
    if nextScan:
        nextScan = False
        object_type = evt.obj.archetype.custom_type
        print (object_type.name)
        robot.behavior.say_text(mapping[object_type.name]["description"])
        if (object_type.name) is "CustomType00":
#            print ("sucess!")
            robot.anim.play_animation_trigger('GreetAfterLongTime')
        
        if (object_type.name) is "CustomType01":
#            print ("sucess!")
            robot.anim.play_animation_trigger('PounceWProxForward')

        if (object_type.name) is "CustomType02":
#            print ("sucess!")
            robot.anim.play_animation_trigger('BumpObjectFastGetOut')
        
        if (object_type.name) is "CustomType03":
#            print ("sucess!")
            robot.anim.play_animation_trigger('ReactToObstacle')
    
        time.sleep(1)
    
def handle_object_disappeared(event_type, event, evt):
    global nextScan
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    print("--------- Vector stopped seeing an object ---------")
    time.sleep(1)
    nextScan = True
    
    
def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(enable_custom_object_detection=True, enable_nav_map_feed=True) as robot:
        # Add event handlers for whenever Vector sees a new object
        
        robot.behavior.set_head_angle(degrees(5.0))
        robot.behavior.set_lift_height(0.0)
        on_object_appeared = functools.partial(handle_object_appeared, robot)
        robot.events.subscribe(on_object_appeared, anki_vector.events.Events.object_appeared)
        robot.events.subscribe(handle_object_disappeared, anki_vector.events.Events.object_disappeared)
        
        # define a unique cube (44mm x 44mm x 44mm) (approximately the same size as Vector's light cube)
        # with a 50mm x 50mm Circles2 image on every face. Note that marker_width_mm and marker_height_mm
        # parameter values must match the dimensions of the printed marker.
        cube_obj0 = robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType00,
                                                  marker=CustomObjectMarkers.Circles2,
                                                  size_mm=44.0,
                                                  marker_width_mm=50.0,
                                                  marker_height_mm=50.0,
                                                  is_unique=True)
        

        cube_obj1 = robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType01,
                                                  marker=CustomObjectMarkers.Circles3,
                                                  size_mm=44.0,
                                                  marker_width_mm=50.0,
                                                  marker_height_mm=50.0,
                                                  is_unique=True)
        
        
        cube_obj2 = robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType02,
                                                  marker=CustomObjectMarkers.Hexagons2,
                                                  size_mm=44.0,
                                                  marker_width_mm=20.0,
                                                  marker_height_mm=20.0,
                                                  is_unique=True)
        

        cube_obj3 = robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType03,
                                                  marker=CustomObjectMarkers.Hexagons3,
                                                  size_mm=44.0,
                                                  marker_width_mm=20.0,
                                                  marker_height_mm=20.0,
                                                  is_unique=True)
        
        
        if ((cube_obj0 is not None) and (cube_obj1 is not None) and (cube_obj2 is not None) and (cube_obj3 is not None)):
            print("All objects defined successfully!")
        else:
            print("One or more object definitions failed!")
            return

        try:
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()  
