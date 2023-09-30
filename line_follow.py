async def line_follow(degrees, white_left = True, desired_rgb = 750):
    motor_pair.unpair(motor_pair.PAIR_1)
    error_history=[]
    print("emptied error_history")
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.F)
    speed = -200
    motor_pair.move_tank(motor_pair.PAIR_1,speed, speed)
    motor.reset_relative_position(5, 0)
    degrees_moved = 0
    while degrees_moved < degrees:
        degrees_moved = abs(motor.relative_position(5))
        colors = color_sensor.rgbi(port.D)
        average_rgb = (colors[0] + colors[1] + colors[2])/3
        error = (average_rgb - desired_rgb )/10
        #print(error)
        #print(colors, average_rgb)
        try:
            error_history.append(int(error))
        except:
            print(len(error_history))
            raise
        correction = pid(error_history)
        right_wheel_speed = int(speed + correction)
        left_wheel_speed = int(speed - correction)
        motor_pair.move_tank(motor_pair.PAIR_1, right_wheel_speed, left_wheel_speed)
        #await runloop.sleep_ms(700)
    print(degrees_moved)
    motor_pair.stop(motor_pair.PAIR_1)
    
