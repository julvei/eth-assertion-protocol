#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

x_size = 10000

x = [25, 50, 75, 100]
y_1 = [243034, 252489, 261945, 271404]
y_2 = [1476380, 1487234, 1498091, 1508950]
y_3 = [1695164, 1700592, 1706020, 1711450]
y_4 = [1711576, 1717003, 1722432, 1727862]
x_s=np.arange(0,x_size)

# Array linear
## Fit model
linear_model_1=np.polyfit(x,y_1,1)
linear_model_fn_1=np.poly1d(linear_model_1)
## Print graphs
plt.scatter(x,y_1,color="red", label="Data on-chain")
plt.plot(x_s, linear_model_fn_1(x_s), color="green", label="On-chain")

# Array linear hash protcol
## Fit model
linear_model_2=np.polyfit(x,y_2,1)
linear_model_fn_2=np.poly1d(linear_model_2)
## Print graphs
plt.scatter(x,y_2,color="red", label="Data protocol")
plt.plot(x_s, linear_model_fn_2(x_s), color="blue", label="Hash")

# Array linear hash protcol - one reward
## Fit model
linear_model_3=np.polyfit(x,y_3,1)
linear_model_fn_3=np.poly1d(linear_model_3)
## Print graphs
plt.scatter(x,y_3,color="red", label="Data one")
plt.plot(x_s, linear_model_fn_3(x_s), color="yellow", label="One Reward")

# Array linear hash protcol - two rewards
## Fit model
linear_model_4=np.polyfit(x,y_4,1)
linear_model_fn_4=np.poly1d(linear_model_4)
## Print graphs
plt.scatter(x,y_4,color="red", label="Data two")
plt.plot(x_s, linear_model_fn_4(x_s), color="orange", label="Two Rewards")

"""
# Check when costs are the same
for i in range(0, 100000000):
    if linear_model_fn_1(i) >= linear_model_fn_2(i):
        print("Costs are same for array size of %d with costs %d when there is no hash and no counterexample found" % (i, linear_model_fn_1(i)))
        break
"""

# Check when costs are the same
for i in range(0, 100000000):
    if linear_model_fn_1(i) >= linear_model_fn_3(i):
        print("Costs are same for array size of %d with costs %d when there is one hash and no counterexample found" % (i, linear_model_fn_1(i)))
        break

# Check when costs are the same
for i in range(0, 100000000):
    if linear_model_fn_1(i) >= linear_model_fn_4(i):
        print("Costs are same for array size of %d with costs %d when there are two hashes and no counterexample found" % (i, linear_model_fn_1(i)))
        break

# Graph settings
plt.title("Linear Array Checking")
plt.legend()
plt.xlabel("array size")
plt.ylabel("gas")
plt.xlim([0, x_size])
plt.show()

offset1 = linear_model_fn_1(0)
plt.plot(x_s, linear_model_fn_1(x_s) - offset1, color="green", label="On-chain")
print("On-chain slope:", linear_model_1[0])
print("Array:", y_1 - offset1)
offset2 = linear_model_fn_2(0)

offset_diff = offset2 - offset1
slope_diff = linear_model_2[0] - linear_model_1[0]
array_size = offset_diff / slope_diff
print("Costs are same for array size of %d with costs %d when there is no hash and no counterexample found" % (array_size, linear_model_fn_1(array_size)))

plt.plot(x_s, linear_model_fn_2(x_s) - offset2, color="blue", label="Protocol")
print("Protocol slope:", linear_model_2[0])
print("Array:", y_2 - offset2)

offset3 = linear_model_fn_3(0)
plt.plot(x_s, linear_model_fn_3(x_s) - offset3, color="yellow", label="One Reward")
print("One slope:", linear_model_3[0])
print("Array:", y_3 - offset3)

offset4 = linear_model_fn_4(0)
plt.plot(x_s, linear_model_fn_4(x_s) - offset4, color="orange", label="Two Rewards")
print("Two slope:", linear_model_4[0])
print("Array:", y_4 - offset4)

plt.legend()
plt.title("Linear Array Checking - w/o offset")
plt.show()
