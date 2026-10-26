"""
Goal :
Find raw temp (simulated) (m1) , Humidity (m2) and Actual Temp (C)
Eq: Actual Temp = m1 (Raw Temp) + m2 (humidity) + C 
Since there were 10 testing condition with 3 unknows (m1, m2 and C),
Least Square method is used to find the unknow. 

"""
import numpy as np                                  # import Library for calcuation 
import matplotlib.pyplot as plt                     # import library for ploting graph and charts
from dataCollection import data                     # import sensore reading 
from average_dataCalculation import SensorData      # import Average Temp and hum 

np.set_printoptions(precision=2, suppress=True)     # all print result will be round up to 2 decimal places


"""
======================================================
Step 1. Get the Average Data
======================================================
"""

sd = SensorData(data)   #get data from the first 2 file
sd.show_table()         #print the data as a table

actual_temp = np.array(sd.avg_temps)        #b vector 
humidity    = np.array(sd.avg_hums)         # part of A 

"""
======================================================
Step 2. Simulate The "RAW TEMP" COLUMN
THE DHT11 is reference reading, and in this step we create a "RAW Reading"  (miscalibrated senor)
Since no seneor is perfect, every senor have noise which affect the reading 
this where er assume chep snsor read the true temperature,
but humidity adda a small psoitive offest, plus some random noise.

So we compare the reference reading with this Simulated senor for find the offset
This step is very import in engineeing test.
======================================================
"""
# Assume the raw senor resing is affected by humidity 
# plus a bit of random noise (physical circuit connection)

np.random.seed(42)  # reprpoudcible random number
noise    = np.random.normal(0, 0.2, 10)     # 10 number near 0
raw_temp = actual_temp + 0.05 * humidity + noise 

# Actual temp and hum -> real reading 
# raw_temp -> Assumption

"""
=========================================
Step 3. Build maxtrix A and Vector B
=========================================
"""

n = len(actual_temp)  #row of the matrix , where n = 10

# A has three columns: RAW Temp, Humidity and 1s 
# np.vstack stack them vertically, then .T transposes the result 

A = np.vstack([raw_temp, humidity, np.ones(n)]).T #matrix A

b = actual_temp.reshape(-1, 1)  #make b a column vector 

print("\n====== Matrix A ======")
print(A) #should be (10,3) with round up 2 decimal places
print("\n====== Matrix b ======")
print(b)

"""
=========================================
Step 4. Solve the Least Squares problem
=========================================

"""
# np.linalg.lstsq = Numpy.Linear Algebra . Least square
# this function find the unknow
# x = solution vector (m1 ,m2 , c)                      | This 3 x 1 matrix
# residuals = sum of squared error ||Ax -b||^2          | A single number (or empty if rank-deficient)
# Rank = Rank of matrix A                               | Should be 3 ( all col is independent)
# s = singular values of A                                  | Shape(3,)- use for diagonsitc

# ONLY X is need for the project result , but other inform is return from numpy 

x, residuals, rank , s = np.linalg.lstsq(A,b, rcond=None)

#1. Take matrix A and b 
#2. Internally computes the best-fit solution using SVD (single Value descomposition)
#3. Return four values in a tuple
#4. Python unpack them into x, residuals, rank and s

m1 = x[0][0]    #extract m1 , x [0][0] -> row 0 & column 0 pull the first coefficient
m2 = x[1][0]    #extract m2, pull row1 & column 0 
c  = x[2][0]    #extract C,  pull row 2 & column 0 


"""
 the other way to solve the promblem is use
 x_manual = np.linalg.inv(A.T @A) @A.T @b
 same as (AᵀA)⁻¹ Aᵀ b, but this method slow in inverting a matrix , 
 Numerically unstable can fail enterly (AᵀA is singular , invers crashes)
"""

# Print out the result in Table method

sign_m2 = "+" if m2 >= 0 else "-"
sign_c  = "+" if c  >= 0 else "-"

print("\n===== CALIBRATION EQUATION=====")
print(f"Actual Temp = ({m1:.4f} x Raw Temp) {sign_m2}{abs(m2):.4f} x Humidity {sign_c}{abs(c):.4f}") 

print(f"So the value of m1, m2, and c are:")
print(f"m1 = {m1:.4f} (temperature cofficient)")
print(f"m2 = {sign_m2}{abs(m2):.4f} (per & humidity)")
print(f"c  = {sign_c}{abs(c):.4f} (°C offeset)")

"""
=========================================================
Step 5. Residuals
quality check of the project , where 
Residual = Actual - Predicted
if residual is small -> the model fits the data well
if residual is large -> the model is not accurate
==========================================================

"""

predicted   = m1* raw_temp + m2* humidity + c  # use the same eq to find the predicted result
residuals  = actual_temp - predicted          # Calculates how far off each prediction is 

#Print the resuidual in table
print("\n===== RESIDUALS ======")
print(f"{'Point':<8} {'Actual':<10} {'Predicted':<12} {'Residual':<10}")
print("-" *42)

# loop all 10 value for calcuation
for i in range(len(actual_temp)):
    print(f"{i+1:<8} {actual_temp[i]:<10.2f} {predicted[i]:<12.2f} {residuals[i]:+.4f}")

print(f"\nSum of squared residuals: {np.sum(residuals**2):.4f}")



"""
===================================================================
Step 6. Plot graph
===================================================================
"""
plt.figure(figuresize=(12,5))

#Plot 1: Data + Regression fit
plt.subplot(1, 2, 1)


