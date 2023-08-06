#!/usr/bin/env python3
import EFumi_WhlTest.variables as v
import EFumi_WhlTest.functions as f


def run():
    for i in range(v.iterations):
    # while loop:
        v.p, point_list = f.rotate(v.p)
        print(point_list)

run()
