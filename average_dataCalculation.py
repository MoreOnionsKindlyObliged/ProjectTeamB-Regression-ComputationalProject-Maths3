# this file is only for calculating the Average Temp and Hum 

import numpy as np
from dataCollection import data

class SensorData: 
    """Take raw sensor reading and calculation averages."""

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.avg_temps = []
        self.avg_hums = []
        self._compute_averages()


    def _compute_averages(self): 
        """Calculate the average for each condition (no printing)"""
        for name, readings in self.raw_data.items(): 
            self.avg_temps.append(np.mean(readings["temp"]))
            self.avg_hums.append(np.mean(readings["hum"]))
           


    def show_table(self):
        """Print the average as a formatted tables."""
        print("===== Average Data =====")
        print(f"{'Condtition':<20} {'Temp (°C)':<12} {'Humidity (%)' :<12}")
        print("-" *45)  
        for (name, _), t, h in zip(self.raw_data.items(),self.avg_temps, self.avg_hums):
            print(f"{name:<20} {t:<12.2f} {h:<12.2f}")


if __name__ == "__main__":
    sd = SensorData(data)
    sd.show_table()