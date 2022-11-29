#Importing numpy
import numpy as np

statefiles = ["test1.out","test2.out","test3.out","test4.out","test5.out"]
#We will create an 1D array
arr1 = np.array([7, 24, 63, 121, 4, 64])
arr2 = np.array([100, 7, 9, 23, 31, 90])
arr3 = np.array([1, 8, 200, 3, 50, 20])

avg = np.average(arr1)

p1 = 20
p2 = 60
p3 = 5

diff1 = (arr1 - p1)**2
diff2 = (arr2 - p2)**2
diff3 = (arr3 - p3)**2

score = diff1 + diff2 + 0.5*diff3

i = np.argmin(score)

#Now we will print index of min value of this array
print("Winning statefile is " + statefiles[i])