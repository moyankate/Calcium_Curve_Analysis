import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filters
from scipy.integrate import simps
from tkinter import Tk, filedialog

plt.ion()  # Enable interactive mode for matplotlib

def load_traces(data_file):
    data = pd.read_csv(data_file)
    data = data.query("LedState==1")  # Filter for LED state to remove fluctuations
    data["Timestamp"] = data["Timestamp"] - data["Timestamp"].iloc[0]
    return data

class FiberPhotometryGUI:
    def __init__(self):
        self.run()
    
    def run(self):
        while True:
            file_path = self.select_file()
            if not file_path:
                print("No file selected. Exiting.")
                break
            self.process_file(file_path)
    
    def select_file(self):
        root = Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title="Select Fiber Photometry Data File", filetypes=[("CSV files", "*.csv")])
        return file_path

    def process_file(self, file_path):
        self.traces = load_traces(file_path)
        self.time = np.array(self.traces['Timestamp'])
        reference_signal = np.array(self.traces['Region1R'])  # Assuming this is reference
        interest_signal = np.array(self.traces['Region0G'])  # Signal of interest
        self.norm_signal = (interest_signal - reference_signal) / reference_signal  # Normalize ΔF/F
        self.norm_signal = savgol_filter(self.norm_signal, window_length=250, polyorder=3)  # Apply smoothing
        
        self.start_idx = None
        self.end_idx = None
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.setup_plot()
    
    def setup_plot(self):
        self.ax.plot(self.time, self.norm_signal, label='Smoothed Normalized Signal (ΔF/F)', color='orange', linewidth=2)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Signal Intensity (Normalized)')
        self.ax.set_title('Normalized and Smoothed Signal (ΔF/F)')
        self.ax.legend()
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_click)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.on_key)
        plt.show(block=True)  # Keep window open until manually closed
    
    def on_click(self, event):
        if event.xdata is not None:
            if self.start_idx is None:
                self.start_idx = (np.abs(self.time - event.xdata)).argmin()
                print(f"Start point selected at {self.time[self.start_idx]:.2f} s")
            elif self.end_idx is None:
                self.end_idx = (np.abs(self.time - event.xdata)).argmin()
                print(f"End point selected at {self.time[self.end_idx]:.2f} s")
                self.calculate_auc()
    
    def calculate_auc(self):
        if self.start_idx is not None and self.end_idx is not None:
            if self.start_idx < self.end_idx:
                auc = simps(self.norm_signal[self.start_idx:self.end_idx+1],
                            self.time[self.start_idx:self.end_idx+1])
                print(f"AUC between {self.time[self.start_idx]:.2f}s and {self.time[self.end_idx]:.2f}s: {auc:.4f}")
                self.start_idx, self.end_idx = None, None  # Reset for next selection
            else:
                print("Please select points in correct order (start before end).")
                self.start_idx, self.end_idx = None, None
    
    def on_key(self, event):
        if event.key == 'q':
            plt.close(self.fig)  # Close figure on 'q' press

if __name__ == "__main__":
    FiberPhotometryGUI()