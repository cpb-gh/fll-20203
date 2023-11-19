from hub import light_matrix, port, motion_sensor, temperature
from motor import HOLD, run
import runloop
import color_sensor
import motor_pair
import motor


RUN_ONE_MOVE_FORWARD_DEGREES=1000

async def run_one():
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, RUN_ONE_MOVE_FORWARD_DEGREES, 30000, 30000, stop = motor.BRAKE, deceleration=1000)
    value = color_sensor.rgbi(port.C)
    print(value)


async def gyro_straight(degrees, forward = True, reset_yaw = True, power = 500):
    motor_pair.unpair(motor_pair.PAIR_1)
    error_history=[]
    print("in gyro straight degrees {} forward {} reset yaw {}".format(degrees, forward, reset_yaw))
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.F)
    if reset_yaw == True:
        motion_sensor.reset_yaw(0)
    if forward == False:
        speed = power
    else:
        speed = -power
    print("yaw in gyro straight:",motion_sensor.tilt_angles()[0])
    motor_pair.move_tank(motor_pair.PAIR_1,speed, speed)
    motor.reset_relative_position(5, 0)
    degrees_moved = 0
    while degrees_moved < degrees:
        degrees_moved = abs(motor.relative_position(5))
        angles = motion_sensor.tilt_angles()
        yaw = angles[0]
        #print(degrees_moved)
        error_history.append(yaw)
        correction = pid(error_history)
        right_wheel_speed = int(speed + correction)
        left_wheel_speed = int(speed - correction)
        motor_pair.move_tank(motor_pair.PAIR_1, right_wheel_speed, left_wheel_speed)
        #await runloop.sleep_ms(700)
    print("gyro straight degrees moved {}".format(degrees_moved))
    print("gyro straight error history length {}".format(len(error_history)))
    motor_pair.stop(motor_pair.PAIR_1)

async def attachment_motor(tan_black, degrees, speed):
    print("in attachment motor spinning {}, degrees {}".format(tan_black, degrees))
    if tan_black == "tan":
        which_port = port.B
    elif tan_black == "black":
        which_port = port.A
    await motor.run_for_degrees(which_port, degrees, speed)
    return

def pid(error_history,kp = 0.4, ki=0.001, kd=0.5):
    # error_history must have at least 2 entrys for pid to work
    if len(error_history) < 2: 
        return 0
    p = error_history[-1]

    i = sum(error_history)

    d = error_history[-1] - error_history[-2]

    correction = (p*kp) + (i*ki) + (d*kd)
    return correction

async def turn(degrees, direction, speed = 100):
    motor_pair.unpair(motor_pair.PAIR_1)
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.F)
    motion_sensor.reset_yaw(0)
    print("yaw in turn:",motion_sensor.tilt_angles()[0])
    # we move in decigrees
    degrees = degrees*10
    if direction == "right":
        print("turning right")
        motor_pair.move_tank(motor_pair.PAIR_1, speed, speed*-1)
    elif direction == "left":
        print("turning left")
        motor_pair.move_tank(motor_pair.PAIR_1, speed*-1, speed)
    else:
        print("Unknown direction {}".format(direction))
    yaw = motion_sensor.tilt_angles()[0]
    while abs(yaw) < degrees:
        #print(yaw)
        yaw = motion_sensor.tilt_angles()[0]
        #await runloop.sleep_ms(200)
    motor_pair.stop(motor_pair.PAIR_1)
    print(yaw)
    #motion_sensor.reset_yaw(0)


async def main():
    await gyro_straight(degrees=950)
    await attachment_motor("black", degrees=-125, speed = 200)
    await gyro_straight(degrees=360,reset_yaw=False)
    await attachment_motor("black", 150, 200)
    await gyro_straight(degrees=100, reset_yaw=False )
    await attachment_motor("tan", speed = 1000 , degrees = -100)
    #await gyro_straight(degrees= 1100, forward=False)
    #await attachment_motor("tan", -140 , 600)
    await gyro_straight(degrees= 2200, forward=False,reset_yaw=False)

async def new_main():
    light_matrix.write("camera on wheels")
    await gyro_straight(degrees = 700   )
    await gyro_straight(degrees=1000, forward=False, reset_yaw=False)

async def craft_creator():
    light_matrix.write("craft creator")
    await gyro_straight(degrees = 1000, forward= False)
    await attachment_motor(tan_black="tan", degrees= 300, speed = 400)
    #await gyro_straight(degrees = 200, forward = False)
    await gyro_straight(degrees= 800, forward= True, power = 300)
    await gyro_straight(degrees= 500, forward= True, power = 600)

async def performer():
    light_matrix.write("everything")
    await gyro_straight(degrees =  900, power=  1000)
    await gyro_straight(degrees = 700, power= 600, reset_yaw=False)
    await gyro_straight(900, forward= False, reset_yaw= False, power = 1000)
    await gyro_straight(600, forward=False, reset_yaw=False, power= 500)

async def dragon():
    light_matrix.write("dragon")
    await gyro_straight(degrees= 330, forward=False)
    await attachment_motor(tan_black= "tan", degrees =-1000, speed = 1000)
    await attachment_motor(tan_black= "tan", degrees =120, speed = 1000)
    await gyro_straight(degrees= 310)

async def camera():
    light_matrix.write("camera")
    await gyro_straight(degrees=1100, forward=False) 
    await attachment_motor(tan_black="black", degrees=130, speed=100)
    await gyro_straight(degrees=100, forward=True)
    await turn(60, direction="left")
    await attachment_motor(tan_black="black", degrees=-130, speed=100)
    await gyro_straight(degrees=0)
    await turn(60, direction="right")
    await gyro_straight(degrees=600, forward=True)

async def experimental_dragon():
    light_matrix.write("dragon")
    await gyro_straight(degrees= 360, forward=False)
    await turn(15, direction = "right", speed = 1000)
    await turn(0, direction = "left", speed = 100)
    await gyro_straight(degrees= 550, forward=True)

async def run_across():
    light_matrix.write("going across!")
    await gyro_straight(degrees=1100, forward=True, power = 800)
    await turn(degrees=40, direction="right", speed= 100)
    await gyro_straight(degrees = 200)
    await turn(degrees=50, direction="left", speed= 100)
    await gyro_straight(degrees=0)
    await gyro_straight(degrees = 2000, power = 1000)

async def music_maker():
    await gyro_straight(degrees=1200, power = 1000)
    #await attachment_motor(tan_black="black", degrees = -200, speed= 200)
    await gyro_straight(degrees=1200, forward=False)

async def mueseum():
    await gyro_straight(degrees = 2200, power = 800, forward=False)
    await gyro_straight(degrees = 400, power = 1000)

#0    craft creator(
#    make sure that the yellow gear pole is down on the black part and that the chick-pin is in place and the end of the arm is parralell with the ground )
#1 new main  
#2a performer
#2b orange person in music
#2c orange person in the middle
#2d boat
#3 run_across  
#4 experimental dragon
#5 music maker 
#6 mueseum 


runloop.run(mueseum())
