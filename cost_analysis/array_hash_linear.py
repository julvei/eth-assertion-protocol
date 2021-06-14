#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

x_size = 3000

x = [25, 50, 75, 100]
y_1 = np.array([243034, 252489, 261945, 271404])
y_2 = np.array([1594307, 1611998, 1629699, 1647410])
y_3 = np.array([1809105, 1817951, 1826802, 1838021])
y_4 = np.array([1825517, 1834363, 1843214, 1852071])
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
plt.scatter(x,y_2,color="red", label="Data hash")
plt.plot(x_s, linear_model_fn_2(x_s), color="blue", label="Hash")

# Array linear hash protcol - one reward
## Fit model
linear_model_3=np.polyfit(x,y_3,1)
linear_model_fn_3=np.poly1d(linear_model_3)
## Print graphs
plt.scatter(x,y_3,color="red", label="Data one")
plt.plot(x_s, linear_model_fn_3(x_s), color="yellow", label="Hash One Reward")

# Array linear hash protcol - two rewards
## Fit model
linear_model_4=np.polyfit(x,y_4,1)
linear_model_fn_4=np.poly1d(linear_model_4)
## Print graphs
plt.scatter(x,y_4,color="red", label="Data two")
plt.plot(x_s, linear_model_fn_4(x_s), color="orange", label="Hash Two Rewards")

"""
# Check when costs are the same
for i in range(0, 100000000):
    if linear_model_fn_1(i) >= linear_model_fn_2(i):
        print("Costs are same for array size of %d with costs %d when there is no hash and no counterexample found" % (i, linear_model_fn_1(i)))
        break

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
"""

# Graph settings
plt.title("Linear Array Hash Checking")
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
plt.plot(x_s, linear_model_fn_2(x_s) - offset2, color="blue", label="Hash")
print("Hash slope:", linear_model_2[0])
print("Array:", y_2 - offset2)

offset3 = linear_model_fn_3(0)
plt.plot(x_s, linear_model_fn_3(x_s) - offset3, color="yellow", label="Hash One Reward")
print("Hash One slope:", linear_model_3[0])
print("Array:", y_3 - offset3)

offset4 = linear_model_fn_4(0)
plt.plot(x_s, linear_model_fn_4(x_s) - offset4, color="orange", label="Hash Two Rewards")
print("Hash Two slope:", linear_model_4[0])
print("Array:", y_4 - offset4)

plt.legend()
plt.title("Linear Array Hash Checking - w/o offset")
plt.show()
