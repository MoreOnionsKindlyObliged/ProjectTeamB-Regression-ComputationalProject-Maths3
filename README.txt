There is 5 file for data, and only 1 for execute

There are all data file, 
dataCollection.py -> sensor reading
average_dataCalculation.py -> only to claculate the average Temp and Hum
leastSquare(Script).py -> find the unknow value using least square ( you can igno this)
leastSquare(Class).py -> same as least Square but origranse in Classes
                        good for extracting data to plot or future analyse
plotting.py-> plot all the result and value from leastsquare.py calculation

main.py -> front , where the to run the program 

Least square calculation 
Goal :
Find raw temp (simulated) (m1) , Humidity (m2) and Actual Temp (C)
Eq: Actual Temp = m1 (Raw Temp) + m2 (humidity) + C 
Since there were 10 testing condition with 3 unknows (m1, m2 and C),
Least Square method is used to find the unknow. 

Calculation 
Actual Temp = m1 (Raw Temp 1) + m2 (humidity 1) + C 
Actual Temp = m1 (Raw Temp 2) + m2 (humidity 2) + C 
                    ...
                    ...
                    ...
Actual Temp = m1 (Raw Temp 10) + m2 (humidity 10) + C                     

Matrix Form: 
    Ax = b  
    
    (where A : 10 x 3 matrix)
    [Raw1 H1 1]
    [Raw2 H2 1]
    [Raw3 H3 1]
     ...
     ...
     ...
    [Raw10 H10 1]

    x (3 x 1 column vector of unknow):
    [m1]
    [m2]
    [c]
    
    b (10x 1 column vector of actual temperatures)

    x = (A^T A)^-1 (A^T)b

    in python (np.linalg.lstsq(A,b)) will do all the calcualtion 

Result: 
=======================================================
Step 1: Average raw sensor data
=======================================================
===== Average Data =====
Condtition           Temp (°C)    Humidity (%)
---------------------------------------------
Room (desk)          20.30        57.17       
In hand              30.35        95.00       
Laptop vent          22.41        47.46       
Bedroom Window       21.03        51.29       
Bedroom Floor        19.05        55.61       
Pocket               25.28        47.42       
Kitchen bench        22.11        50.48       
Hot drink            31.61        29.50       
Cold drink           17.52        52.21       
Blow in to sensor    28.12        95.00       

=======================================================
STEP 2: Least Squares Calibration
=======================================================

====== Matrix A ======
[[23.25 57.17  1.  ]
 [35.07 95.    1.  ]
 [24.92 47.46  1.  ]
 [23.9  51.29  1.  ]
 [21.78 55.61  1.  ]
 [27.6  47.42  1.  ]
 [24.95 50.48  1.  ]
 [33.24 29.5   1.  ]
 [20.03 52.21  1.  ]
 [32.97 95.    1.  ]]

====== Matrix b ======
[[20.3 ]
 [30.35]
 [22.41]
 [21.03]
 [19.05]
 [25.28]
 [22.11]
 [31.61]
 [17.52]
 [28.12]]

===== CALIBRATION EQUATION=====
Actual Temp = (0.9952 x Raw Temp) -0.0479 x Humidity  -0.0857
So the value of m1, m2, and c are:
m1 = 0.9952 (temperature cofficient)
m2 = -0.0479 (per & humidity)
c  = -0.0857 (°C offeset)

===== RESIDUALS ======
Point    Actual     Predicted    Residual  
------------------------------------------
1        20.30      20.32        -0.0245
2        30.35      30.27        +0.0782
3        22.41      22.44        -0.0261
4        21.03      21.24        -0.2141
5        19.05      18.93        +0.1180
6        25.28      25.12        +0.1632
7        22.11      22.33        -0.2186
8        31.61      31.58        +0.0281
9        17.52      17.35        +0.1639
10       28.12      28.18        -0.0680

Sum of squared residuals: 0.1739

Residual quality check of the project , where 
        Residual = Actual - Predicted
        if residual is small -> the model fits the data well
        if residual is large -> the model is not accurate


