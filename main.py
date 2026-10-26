"""
Main - Frontend entry point 
Run the full pipeline : Data -> averager Sensor reading data -> Calibrate ->plot

"""
from dataCollection import data
from average_dataCalculation import SensorData
from leastSquare_Classes import Calibration
from plotting import CalibrationPlotter


def run():
    """Execute the full pipeline from raw data to plots"""

    # --- Step 1: Average the raw data
    print("=" * 55)
    print ("Step 1: Average raw sensor data")
    print("=" * 55)
    sd = SensorData(data)
    sd.show_table()

    # --- Step 2: Run the calibration 
    print("\n" + "=" * 55)
    print("STEP 2: Least Squares Calibration")
    print("=" * 55)
    cal = Calibration(sd)
    cal.show_matrix()
    cal.show_equation()
    cal.show_residuals()

    # --- Step 3: Plot the Result
    print("\n" + "=" * 55)
    print("STEP 3: Plotting results")
    print("=" * 55)
    plotter = CalibrationPlotter(cal, title_prefix="")
    plotter.plot()
    plotter.save("calibration_plot.png")
    plotter.show()

if __name__ == "__main__":
    run()