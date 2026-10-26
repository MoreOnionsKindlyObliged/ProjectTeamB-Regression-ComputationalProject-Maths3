import numpy as np                               # import Library for calcuation 
from dataCollection import data                  # import sensore reading
from average_dataCalculation import SensorData   # import Average Temp and hum  

np.set_printoptions(precision=2, suppress=True)  # all print result will be round up to 2 decimal places

class Calibration: 
    """Performs least squares calibration on averaged senor data"""

    #first set up variable 
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data
        self.actual_temp = np.array(sensor_data.avg_temps)
        self.humidity    = np.array(sensor_data.avg_hums)
        self._simulate_raw_temp()
        self._build_matrices()
        self._solve()
        self._compute_error()


    def _simulate_raw_temp(self):
        """
        step 2: create the simulated raw sensor column
        THE DHT11 is reference reading, and in this step we create a "RAW Reading"  (miscalibrated senor)
        Since no seneor is perfect, every senor have noise which affect the reading 
        this where we assume cheap sensor read the true temperature,
        but humidity add  a small psoitive offest, plus some random noise.

        So we compare the reference reading with this Simulated sensor for find the offset
        This step is very import in engineeing test.
        """
        np.random.seed(42)  # reprpoudcible random number
        noise  =np.random.normal(0, 0.2, 10) # 10 number near 0
        self.raw_temp = self.actual_temp + 0.05 * self.humidity +noise

        # Actual temp and hum -> real reading 
        # raw_temp -> Assumption
    
    
    
    
    def _build_matrices(self):
        """Step 3: build matrix A and Vector b"""
        n = len(self.actual_temp)   # A has three columns: RAW Temp, Humidity and 1s 

        # A has three columns: RAW Temp, Humidity and 1s 
        # np.vstack stack them vertically, then .T transposes the result            

        self.A = np.vstack([self.raw_temp, self.humidity, np.ones(n)]).T
        self.b = self.actual_temp.reshape(-1,1)  #make b a column vector

    def _solve(self):
        """
        step 4: solve least square for m1, m2 ,c
        np.linalg.lstsq = Numpy.Linear Algebra . Least square
        this function find the unknow
        x = solution vector (m1 ,m2 , c)                      | This 3 x 1 matrix
        residual = sum of squared error ||Ax -b||^2           | A single number (or empty if rank-deficient)
        Rank = Rank of matrix A                               | Should be 3 ( all col is independent)
        s = singular values of A                              | Shape(3,)- use for diagonsitc
        ONLY X is need for the project result , but other inform is return from numpy
        """
        #1. Take matrix A and b 
        #2. Internally computes the best-fit solution using SVD (single Value descomposition)
        #3. Return four values in a tuple
        #4. Python unpack them into x, residuals, rank and s
        
        x, residual, rank , s = np.linalg.lstsq(self.A,self.b, rcond=None)
        self.m1 = x[0][0]    #extract m1 , x [0][0] -> row 0 & column 0 pull the first coefficient
        self.m2 = x[1][0]    #extract m2, pull row1 & column 0 
        self.c  = x[2][0]    #extract C,  pull row 2 & column 0 
        
        """
        the other way to solve the promblem is use
        x_manual = np.linalg.inv(A.T @A) @A.T @b
        same as (AᵀA)⁻¹ Aᵀ b, but this method slow in inverting a matrix , 
        Numerically unstable can fail enterly (AᵀA is singular , invers crashes)
        """



    def _compute_error(self):
        """Step 5: Compute prediction and residuals."""
         # use the same eq to find the predicted result
        self.predicted= self.m1 * self.raw_temp +self.m2 * self.humidity + self.c
        # Calculates how far off each prediction is
        self.residuals  = self.actual_temp - self.predicted

    def show_matrix(self):
        """Print matrix A and vector b usd in the least squares problem."""
        print("\n====== Matrix A ======")
        print(self.A) #should be (10,3) with round up 2 decimal places
        print("\n====== Matrix b ======")
        print(self.b)

    def show_equation(self): 
        """Print the calibration equation."""
        sign_m2 = "+" if self.m2 >= 0 else "-"
        sign_c  = "+" if self.c  >= 0 else "-"

        print("\n===== CALIBRATION EQUATION=====")
        print(f"Actual Temp = ({self.m1:.4f} x Raw Temp) "
              f"{sign_m2}{abs(self.m2):.4f} x Humidity "
              f" {sign_c}{abs(self.c):.4f}") 

        print(f"So the value of m1, m2, and c are:")
        print(f"m1 = {self.m1:.4f} (temperature cofficient)")
        print(f"m2 = {sign_m2}{abs(self.m2):.4f} (per & humidity)")
        print(f"c  = {sign_c}{abs(self.c):.4f} (°C offeset)")    

    def show_residuals(self): 
        """
        Print the residual table
        quality check of the project , where 
        Residual = Actual - Predicted
        if residual is small -> the model fits the data well
        if residual is large -> the model is not accurate
        """
        print("\n===== RESIDUALS ======")
        print(f"{'Point':<8} {'Actual':<10} {'Predicted':<12} {'Residual':<10}")
        print("-" *42)

        # loop all 10 value for calcuation
        for i in range(len(self.actual_temp)):
            print(f"{i+1:<8} {self.actual_temp[i]:<10.2f} {self.predicted[i]:<12.2f} {self.residuals[i]:+.4f}")

        print(f"\nSum of squared residuals: {np.sum(self.residuals**2):.4f}")


#only runs if this file is excuted directly (not when imported)

if __name__ == "__main__":
    sd  = SensorData(data)
    cal = Calibration(sd)
    cal.show_equation()
    cal.show_matrix()
    cal.show_residuals()
