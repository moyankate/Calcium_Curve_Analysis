# 🧠 GUI for Quantifying Neuronal Activation During Memory Recall

This repository provides a Python-based graphical interface and analysis utilities for processing fiber photometry calcium imaging data. The GUI allows users to load raw CSV files, normalize and smooth calcium traces, interactively select time windows, and compute the area under the curve (AUC) as a quantitative measure of neuronal activation.
This tool is helpful for measuring neuron activation during behavioral tasks such as memory recall.

---

## 🌟 Features

* **Load raw CSV files** via a Tkinter file dialog.
* **Automatic preprocessing**:

  * Filter by LED state.
  * Align timestamps so recordings start at 0.
  * Normalize signals using ΔF/F.
  * Smooth traces with a Savitzky–Golay filter.
* **Interactive matplotlib GUI**:

  * Click once to select start time.
  * Click again to select end time.
  * AUC between selections is computed and printed.
* **Keyboard shortcuts**:

  * Press `q` to close the plot and load a new file.
* **Utility functions** (in `utils_1.py`) for:

  * Deinterleaving multiplexed LED channels.
  * Extracting event timestamps from TTL files.
  * Z-score–style normalization (`scale` function).
* **Example Jupyter notebook** (`fiber_photometry_analysis.ipynb`) demonstrating analysis on sample data.

---

## ❓ How It Works

### GUI Workflow (`GUI.py`)

1. A file dialog prompts you to select a `.csv` fiber photometry file.
2. The script:

   * Loads and cleans the data.
   * Uses `Region1R` as the reference channel.
   * Uses `Region0G` as the signal-of-interest.
   * Computes ΔF/F = (signal - reference) / reference.
   * Smooths the trace.
3. An interactive plot appears.
4. You select a start and end time by clicking on the plot.
5. The program computes AUC over that interval using Simpson’s rule.
6. Press `q` to close the plot and load another file.

This workflow makes it easy to quickly compare neuronal activation across trials or behavioral epochs.

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install numpy pandas scipy matplotlib jupyter
```

`tkinter` is usually included with Python, but if missing, install it via your OS package manager (e.g., `sudo apt-get install python3-tk`).

---

## Usage

### ▶️ Running the GUI

```bash
python GUI.py
```

Inside the GUI:

1. Choose a CSV file.
2. View the ΔF/F trace.
3. Click to mark start and end of the analysis window.
4. AUC is printed to the console.
5. Repeat as needed.
6. Press `q` to close the window.

### Running the Notebook

```bash
jupyter notebook
```

Then open and run:

```
fiber_photometry_analysis.ipynb
```

The notebook shows how to load, normalize, and visualize data, and how to use the helper functions in `utils_1.py`.

---

## Data Format

CSV files must include:

* `Timestamp`
* `LedState`
* `Region0G`, `Region1R`, etc.

TTL files (optional) should contain:

* `Timestamp`
* `Value` (0 or 1)

`utils_1.py` handles:

* Event detection (shock, tone, pips, etc.).
* Interpolating LED states onto a common timeline.
* Computing ΔF/F for multiple regions.

---

## Extending the Tool

Possible enhancements:

* Select channels dynamically instead of hard-coded choices.
* Add batch processing across many files.
* Export AUC results to CSV.
* Add automatic event-aligned AUC extraction (e.g., ±5s around shock).

---

## 💜 Acknowledgements

Developed as part of PSL498 Fourth Year Research under the supervision of **Dr. Sheena Josselyn**, University of Toronto. This tool was created to support quantifying neuronal activation during memory recall tasks.

---
