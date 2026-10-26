import matplotlib.pyplot as plt
import numpy as np

class CalibrationPlotter:

    """Draws the calibration fit and residuals plots from a Calibration object."""

    def __init__(self, calibration, title_prefix=""):
        self.cal = calibration
        self.title_prefix = title_prefix
        self.fig = None

    def plot(self):
        """Build the two-panel figure (fit + residuals)."""
        self.fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,5))

        # --- Panel 1 : scatter + regression line ---
        ax1.scatter(self.cal.raw_temp, self.cal.actual_temp,
                    color='red', label='Data points')

        """
        True regression line : eveluate the calibration equation at 
        The minimum and maximum raw temperature , and draw a straight
        line between those two endpoints.
        """
        x_min = self.cal.raw_temp.min()
        x_max = self.cal.raw_temp.max()
        h_mean = self.cal.humidity.mean()

        y_min= self.cal.m1 * x_min + self.cal.m2 * h_mean + self.cal.c
        y_max= self.cal.m1 * x_max + self.cal.m2 * h_mean + self.cal.c
        
        ax1.plot([x_min, x_max], [y_min, y_max],
                 color='blue', label='Regression fit')

        ax1.set_xlabel('Raw Temperature (°C)')
        ax1.set_ylabel('Actual Temperature (°C)')
        ax1.set_title(f'{self.title_prefix}Calibration Fit')
        ax1.legend()
        ax1.grid(True)
        

        # --- Panel 2: residual ---
        points = range(1,len(self.cal.residuals) +1)
        ax2.bar(points, self.cal.residuals, color='green')
        ax2.axhline(0, color='black', linestyle='--')
        ax2.set_xlabel('Data Point')
        ax2.set_ylabel('Residual (°C)')
        ax2.set_title(f'{self.title_prefix}Residuals')
        ax2.grid(True)

        self.fig.tight_layout()
        return self.fig

    def save(self, filename):
        """Save the figure to a file (PNG by default)"""
        if self.fig is None: 
            self.plot()
        self.fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Figure saved as:{filename}")

    def show(self):
        """Display the figure window"""
        if self.fig is None:
            self.plot()
        plt.show()

# only run when this file executed directly 
if __name__ == "__main__":
    from dataCollection import data
    from average_dataCalculation import SensorData
    from leastSquare_Classes import Calibration 

# Step 1: Run The calibration
    sd = SensorData(data)
    cal = Calibration(sd)

# Step 2: plot the result 
    plotter = CalibrationPlotter(cal, title_prefix="")
    plotter.plot()
    plotter.save('calibration_plot.png')
    plotter.show()
