"""
14:40-15:11
"""
import math


def read_target_area():
    x, y = input().replace("target area: ", "").split(", ")
    x1, x2 = (int(i) for i in x.replace("x=", "").split(".."))
    y1, y2 = (int(i) for i in y.replace("y=", "").split(".."))
    return ((x1, x2), (y1, y2))


def main_a():
    # For this one, we can ignore x. Target area's a square, so we can always
    # assume there's a valid value.
    _, (y1, y2) = read_target_area()
    max_vertical_v = -(y1 + 1)
    print("max_vertical_v:", max_vertical_v)
    # Triangular numbers
    max_height = max_vertical_v * (max_vertical_v + 1) // 2
    print("max_height:", max_height)


def hits_target_area(target_area, velocity):
    (x1, x2), (y1, y2) = target_area
    vx, vy = velocity
    x, y = 0, 0
    # print("start at:", x, y, "with velocity:", vx, vy)

    while True:
        # print("position:", x, y)
        if x >= x1 and x <= x2 and y >= y1 and y <= y2:
            return True
        if vx == 0 and x < x1:
            return False
        if y < y1:
            return False

        x += vx
        y += vy
        vx = vx - 1 if vx > 0 else 0
        vy -= 1


def inverse_triangular_number(n):
    return math.floor(math.sqrt(2 * n + 0.25) - 0.5)


def main_b():
    target_area = read_target_area()
    (x1, x2), (y1, y2) = target_area
    max_vy = -(y1 + 1)
    min_vy = y1
    max_vx = x2
    min_vx = inverse_triangular_number(x1)

    velocities = []
    for vy in range(min_vy, max_vy + 1):
        for vx in range(min_vx, max_vx + 1):
            if hits_target_area(target_area, (vx, vy)):
                velocities.append((vx, vy))

    print("velocities:", len(velocities))


if __name__ == "__main__":
    # main_a()
    main_b()
