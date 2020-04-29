#!/usr/bin/env python3

import threading
import time
import functools
import anki_vector
from anki_vector.events import Events
from anki_vector.objects import CustomObjectMarkers, CustomObjectTypes
from anki_vector.util import degrees, Angle, Pose, distance_mm, speed_mmps


said_text = False

def on_robot_observed_face(robot, event_type, event, done):
        print("Vector sees a face")
        global said_text
        if not said_text:
            said_text = True
            robot1.behavior.say_text("I see a face!")
            robot2.behavior.say_text("I see a face!")
            done.set()
            
def handle_object_appeared(robot, event_type, event):
    robot1 = anki_vector.Robot('serial', show_viewer=True, enable_custom_object_detection=True, enable_nav_map_feed=True)
    robot2 = anki_vector.Robot('serial', show_viewer=True, enable_custom_object_detection=True, enable_nav_map_feed=True)
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
#    print(f"--------- Vector started seeing an object --------- \n{event.obj}")
    print("--------- Vector started seeing an object ---------")
    
    object_type = event.obj.archetype.custom_type
    print (object_type.name)
    if (object_type.name) is "CustomType00":
        robot.conn.request_control()
        time.sleep(1.5)
        print ("Vector can see marker {}".format(object_type.name))
        robot.behavior.say_text("Hey Green eyes!, pew pew pew")
        robot.anim.play_animation_trigger('FistBumpSuccess')
        
    if (object_type.name) is "CustomType01":
        robot.conn.request_control()
        time.sleep(1.5)
        robot.behavior.say_text("Hey, you wanna go get some micro chips?")
        print ("Vector can see marker {}".format(object_type.name))
        
    if (object_type.name) is "CustomType02":
        robot.conn.request_control()
        time.sleep(1.5)
        print ("Now Vector can see marker {}".format(object_type.name))
        robot.behavior.say_text("I'm circuit board! I'm going home!")
        robot.behavior.drive_on_charger()

    if (object_type.name) is "CustomType03":
        robot.conn.request_control()
        time.sleep(1.5)
        print ("Vector can see marker {}".format(object_type.name))
        robot.behavior.say_text("Attack, Attack")
        robot.anim.play_animation_trigger('PounceSuccess')
        robot.behavior.drive_straight(distance_mm(-40), speed_mmps(400))
        robot.behavior.set_lift_height(1.0)
        robot.behavior.drive_straight(distance_mm(100), speed_mmps(500))
        robot.behavior.set_lift_height(0.0)

def handle_object_disappeared(robot, event_type, event):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
#    print(f"--------- Vector stopped seeing an object --------- \n{event.obj}")
    print("--------- Vector stopped seeing an object ---------")
    robot1.conn.release_control()
    robot2.conn.release_control()

def main():
    robot1 = anki_vector.Robot('serial', show_viewer=True, enable_custom_object_detection=True, enable_nav_map_feed=True)
    robot2 = anki_vector.Robot('serial', show_viewer=True, enable_custom_object_detection=True, enable_nav_map_feed=True)
    
# Connect to the Robot
    robot1.connect()
    robot2.connect()
    
    # Add event handlers for whenever Vector sees a new object
     
    on_object_appeared = functools.partial(handle_object_appeared, robot1)
    robot1.events.subscribe(handle_object_appeared, anki_vector.events.Events.object_appeared)
    robot1.events.subscribe(handle_object_disappeared, anki_vector.events.Events.object_disappeared)
    
    on_object_appeared = functools.partial(handle_object_appeared, robot2)
    robot2.events.subscribe(handle_object_appeared, anki_vector.events.Events.object_appeared)
    robot2.events.subscribe(handle_object_disappeared, anki_vector.events.Events.object_disappeared)
    
    done = threading.Event()
    robot1.events.subscribe(on_robot_observed_face, Events.robot_observed_face, done)
    robot2.events.subscribe(on_robot_observed_face, Events.robot_observed_face, done)
    cube_obj0 = robot1.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType00,
                                              marker=CustomObjectMarkers.Circles2,
                                              size_mm=44.0,
                                              marker_width_mm=20.0,
                                              marker_height_mm=20.0,
                                              is_unique=True)


    cube_obj1 = robot1.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType01,
                                              marker=CustomObjectMarkers.Circles3,
                                              size_mm=44.0,
                                              marker_width_mm=20.0,
                                              marker_height_mm=20.0,
                                              is_unique=True)


    cube_obj2 = robot2.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType02,
                                              marker=CustomObjectMarkers.Hexagons2,
                                              size_mm=44.0,
                                              marker_width_mm=20.0,
                                              marker_height_mm=20.0,
                                              is_unique=True)


    cube_obj3 = robot2.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType03,
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

#    robot1.purple eyes
#    robot2.green eyes
    
    print("N7N9 activated!")
    robot1.behavior.say_text("N7N9 activated!")
    print("W6V9 rolling out!")
    robot2.behavior.say_text("W6V9 rolling out!")
    robot1.behavior.drive_off_charger()
    robot2.behavior.drive_off_charger()
    
    robot1.behavior.set_head_angle(degrees(5.0))
    robot2.behavior.set_head_angle(degrees(5.0))
    
    robot1.behavior.turn_in_place(degrees(-10))
    robot1.behavior.drive_straight(distance_mm(10), speed_mmps(100))
    robot1.behavior.turn_in_place(degrees(100))
    robot1.behavior.drive_straight(distance_mm(-100), speed_mmps(100))
    
    robot2.behavior.drive_straight(distance_mm(30), speed_mmps(100))
    time.sleep(5)
    
    robot1.behavior.drive_straight(distance_mm(-50), speed_mmps(100))
    
    robot2.behavior.turn_in_place(degrees(-180))
    time.sleep(5)
    
    
    robot2.behavior.turn_in_place(degrees(90))
    robot1.behavior.turn_in_place(degrees(-90))
    time.sleep(5)
    
    robot1.behavior.turn_in_place(degrees(180))
    time.sleep(5)
    
    robot1.behavior.drive_on_charger()
    robot2.behavior.drive_on_charger()

    robot1.conn.release_control()
    robot2.conn.release_control()
    
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
