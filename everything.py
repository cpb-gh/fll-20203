from hub import light_matrix, port, motion_sensor
from motor import HOLD
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


async def gyro_straight(degrees, forward = True, reset_yaw = True):
    motor_pair.unpair(motor_pair.PAIR_1)
    error_history=[]
    print("emptied error_history")
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.F)
    if reset_yaw == True:
        motion_sensor.reset_yaw(0)
    if forward == False:
        speed = 500
    else:
        speed = -500
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
    print(degrees_moved)
    motor_pair.stop(motor_pair.PAIR_1)

async def attachment_motor(tan_black, degrees, speed):
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

async def turn(degrees):
    motor_pair.unpair(motor_pair.PAIR_1)
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.F)
    motion_sensor.reset_yaw(0)
    motor_pair.move_tank(motor_pair.PAIR_1, 100, -100)
    yaw = motion_sensor.tilt_angles()[0]
    while abs(yaw) < degrees:
        #print(yaw)
        yaw = motion_sensor.tilt_angles()[0]
        #await runloop.sleep_ms(200)
    motor_pair.stop(motor_pair.PAIR_1)
    print(yaw)




async def main():
    await gyro_straight(degrees=940)
    await attachment_motor("black", degrees=-125, speed = 200)
    await gyro_straight(degrees=360)
    await attachment_motor("black", 150, 200)
    await gyro_straight(degrees=100, )
    await attachment_motor("tan", 120 , 70)
    await gyro_straight(degrees= 1100, forward=False)
    await attachment_motor("tan", -140 , 600)
    await gyro_straight(degrees= 270, forward=False)

async def craft_creator():
    await gyro_straight(degrees = 1000)
    await gyro_straight(degrees= 1000, forward= False)

async def performer():
    await gyro_straight(degrees =  1800)
    await gyro_straight(1700, forward= False, reset_yaw= False)

async def dragon():
    await gyro_straight(degrees= 330, forward=False)
    await attachment_motor(tan_black= "tan", degrees =-1000, speed = 300)
    await attachment_motor(tan_black= "tan", degrees =120, speed = 1000)
    await gyro_straight(degrees= 310)

runloop.run(dragon())
