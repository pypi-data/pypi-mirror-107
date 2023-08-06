import EFumi_WhlTest.variables as v


def rotate(mtr):
    x = v.rotM @ mtr
    points = [[v.r * x[0][0], v.r * x[1][0]],
              [v.r * x[0][1], v.r * x[1][1]],
              [v.r * x[0][2], v.r * x[1][2]],
              [v.r * x[0][3], v.r * x[1][3]]]
    return x, points
