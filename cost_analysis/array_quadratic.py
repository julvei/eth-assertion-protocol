#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

x_size = 100

x = [15, 30, 45, 60]
y_1 = [331747, 461619, 672495, 964502]
y_2 = [1550288, 1564211, 1578136, 1592194]
y_3 = [1813947, 1820909, 1827872, 1834901]
x_s=np.arange(0,x_size)

def quadratic_model(a, b, x):
    return a * np.power(x,2) + b

# Array quadratic
## Fit model
linear_model_1=np.polyfit(np.power(x,2),y_1,1)
linear_model_fn_1=np.poly1d(linear_model_1)
## Print graphs
plt.scatter(x,y_1,color="red", label="Data on-chain")
plt.plot(x_s, quadratic_model(linear_model_1[0], linear_model_1[1], x_s), color="green", label="On-chain")

# No Reward
## Fit model
linear_model_2=np.polyfit(x,y_2,1)
linear_model_fn_2=np.poly1d(linear_model_2)
## Print graphs
plt.scatter(x,y_2,color="red", label="Data no")
plt.plot(x_s, linear_model_fn_2(x_s), color="blue", label="No Reward")

# One Reward
## Fit model
linear_model_3=np.polyfit(x,y_3,1)
linear_model_fn_3=np.poly1d(linear_model_3)
## Print graphs
plt.scatter(x,y_3,color="red", label="Data one")
plt.plot(x_s, linear_model_fn_3(x_s), color="yellow", label="One Reward")

# Check when costs are the same
for i in range(0, 100000000):
    if quadratic_model(linear_model_1[0], linear_model_1[1], i) >= linear_model_fn_2(i):
        print("Costs are same for array size of %d with costs %d when there is no hash and no counterexample found" % (i, linear_model_fn_1(i)))
        break
        
for i in range(0, 100000000):
    if quadratic_model(linear_model_1[0], linear_model_1[1], i) >= linear_model_fn_3(i):
        print("Costs are same for array size of %d with costs %d when there is one hash and no counterexample found" % (i, linear_model_fn_1(i)))
        break

# Graph settings
plt.title("Quadratic Array Checking")
plt.legend()
plt.xlabel("array size")
plt.ylabel("gas")
plt.xlim([0, x_size])

plt.show()

offset1 = quadratic_model(linear_model_1[0], linear_model_1[1], 0)
plt.plot(x_s, quadratic_model(linear_model_1[0], linear_model_1[1], x_s) - offset1, color="green", label="On-chain")
print("Array:", y_1 - offset1)

offset2 = linear_model_fn_2(0)
plt.plot(x_s, linear_model_fn_2(x_s) - offset2, color="blue", label="No Reward")
print("No slope:", linear_model_2[0])
print("Array:", y_2 - offset2)

offset3 = linear_model_fn_3(0)
plt.plot(x_s, linear_model_fn_3(x_s) - offset3, color="yellow", label="One Reward")
print("One slope:", linear_model_3[0])
print("Array:", y_3 - offset3)


plt.legend()
plt.title("Quadratic Array Checking - w/o offset")
plt.show()

