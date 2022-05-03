from collections import Counter


things_avoid = [1, 2, 4, 8, 16, 32, 64, 128, 256]
avoids = Counter(things_avoid)
nlist = [i for i in range(300) if(avoids[i]==0)]