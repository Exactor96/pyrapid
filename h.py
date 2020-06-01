# https://codeforces.com/group/b4WyyjFAzh/contest/242499/problems

"""
2
0 0 1
0 1 1
1 1
1 0
----------
1
---------
2
0 0 1
0 1 1
1 1
2 1
---------
2
--------
2
0 0 1
5 0 1
5 12
10 12
---------
13.000000
---------
2
0 0 2
5 0 1
5 12
10 12
--------
12.000000
-------
4
78 520 5
827 239 5
620 200 7
809 269 7
986 496
754 745
772 375
44 223
-------
68.452426
-----
"""

def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


iters = int(input())

rocks_arr = []
point_arr = []

for itr in range(iters):
    rocks_arr.append(
        [int(i) for i in input().split()]
    )
for itr in range(iters):
    point_arr.append(
        [int(i) for i in input().split()]
    )

len_list = []
from math import sqrt

for i in range(iters):
    for j in range(iters):
        len_list.append(max(
            [sqrt((point_arr[i][0] - rocks_arr[j][0]) ** 2 + (point_arr[i][1] - rocks_arr[j][1]) ** 2) / rocks_arr[j][
                2]]
        ))

print(len_list)
answ_list = []



chks = [i for i in chunks(len_list, iters)]
for each in chunks(len_list, iters):
    answ_list.append(min(each))

print(answ_list)
print(max(answ_list))

