async def test():
    await gyro_straight(degrees=940)
    await attachment_motor("black", degrees=-145, speed = 200)
    await gyro_straight(degrees=360)
    await attachment_motor("black", 170, 200)
    await gyro_straight(degrees=100, )
    await attachment_motor("tan", 120 , 70)
    await gyro_straight(degrees= 1100, forward=False)
    await attachment_motor("tan", -140 , 600)
    await gyro_straight(degrees= 270, forward=False)