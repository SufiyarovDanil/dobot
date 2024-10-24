move: int = 720
sub_counter: int = 0
my_1_5_cube: float = 37.5
counter: int = -1
my_1_cube: int = 18
cube_counter: int = 1
z_cube: int = 24
zcube_count: int = 1


def init_components() -> None:
    dType.SetInfraredSensor(api, 1, 2, 1)
    dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
    dType.SetHOMECmdEx(api, 0, 1)


def is_cube_detected() -> bool:
    return dType.GetInfraredSensor(api, 2)[0] == 1


def stop_conv() -> None:
    dType.SetEMotorEx(api, 0, 0, 0, 1)


def start_conv(velocity: int) -> None:
    dType.SetEMotorEx(api, 0, 1, velocity, 1)


def move_rail(pos: int) -> None:
    current_pose = dType.GetPose(api)
    dType.SetPTPWithLCmdEx(api, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], pos, 1)


def move_sentry(x: int, y: int, z: int) -> None:
    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 2, x, y, z, current_pose[3], 1)


def rotate_sentry(r: int) -> None:
    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 1, current_pose[0], current_pose[1], current_pose[2], r, 1)


def place_cube():
    global sub_counter, move, my_1_cube, cube_counter, z_cube, zcube_count, my_1_5_cube, counter

    if sub_counter > 0:
        move_rail(move + my_1_cube * cube_counter)
        rotate_sentry(-60)
        move_sentry(242, 0, 0)
        move_sentry(242, 0, -115 + z_cube * zcube_count)
        dType.SetEndEffectorSuctionCupEx(api, 0, 1)
        move_sentry(242, 0, 0)

        sub_counter -= 1
        zcube_count += 1
        cube_counter += 0.9

        if sub_counter == 0:
            zcube_count = 1
            cube_counter = 1
    else:
        move = move - my_1_5_cube
        move_rail(move)
        rotate_sentry(-60)
        move_sentry(242, 0, 0)
        move_sentry(242, 0, -115)
        dType.SetEndEffectorSuctionCupEx(api, 0, 1)
        move_sentry(242, 0, 0)

        counter += 1
        sub_counter = counter


def main() -> None:
    init_components()
    conv_vel: int = 2500
    print(conv_vel)
    start_conv(conv_vel)

    while True:
        if not is_cube_detected():
            continue

        dType.dSleep(900)
        stop_conv()
        move_rail(287)
        move_sentry(294, -4, 0)
        rotate_sentry(-60)
        dType.SetEndEffectorSuctionCupEx(api, 1, 1)
        move_sentry(294, -4, 0)
        place_cube()
        start_conv(conv_vel)

main()
