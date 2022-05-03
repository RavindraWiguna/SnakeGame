# from collections import Counter
# from snakegame.point import Point

# def getClosestFactor(num, div):
#     mod = num % div
#     ddiv  = div
#     idiv = div
#     while( mod != 0):
#         idiv +=1
#         ddiv -=1
#         imod = num % idiv
#         dmod = num % ddiv
#         if(imod < dmod):
#             mod = imod
#             div = idiv
#         else:
#             mod= dmod
#             div = ddiv

#     print(div)
#     return div

# def assertinsir(param):
#     variables = param
#     assert param > 0


# # num = int(input("input num: "))
# # div = int(input("input divisor: "))

# # getClosestFactor(num, div)

# # assertinsir(-1)

# list_of_point = [Point(0, 1), Point(0, 2)]
# list_of_int = [1,2,3,4,5,6,7,8]
# cntr = Counter(list_of_int)
# # print(cntr)
# cntrp = Counter(list_of_point)
# print(cntrp)
# if(cntr[5] >= 1):
#     print("it is")

# if(cntrp[Point(0, 2)] >= 1):
#     print("it is not")

# def iteration(items):
#     newlist = []
#     for i in range(items):
#         newlist.append(i)

# iteration(1000000)
from collections import Counter


things_avoid = [1, 2, 4, 8, 16, 32, 64, 128, 256]
avoids = Counter(things_avoid)
nlist = []
for i in range(300):
    if(avoids[i]==0):
        nlist.append(i)
