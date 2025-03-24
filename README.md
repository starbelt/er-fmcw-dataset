# FMCW Radar Dataset Generator

This repository contains tools for generating radar datasets using Frequency Modulated Continuous Wave (FMCW) radar with Chirp Synchronization. The main program configures the Analog Devices CN0566 Phased Array (Phaser) Development Platform, provides an interactive GUI with optional Constant False Alarm Rate (CFAR) processing, and exports both raw data and processed images for machine learning applications.

## Table of Contents

- [Overview](#overview)
- [Theory](#theory)
  - [FMCW Radar](#fmcw-radar)
  - [Range Resolution](#range-resolution)
  - [Chirp Synchronization](#chirp-synchronization)
  - [Constant False Alarm Rate (CFAR)](#constant-false-alarm-rate-cfar)
- [Dataset Structure](#dataset-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Results and Data Format](#results-and-data-format)
  - [Sample Images](#sample-images)
  - [CSV Structure](#csv-structure)
- [File Descriptions](#file-descriptions)
- [License](#license)

## Overview

This project enables the creation of radar imaging datasets using low-cost Software Defined Radio (SDR) and phased array hardware. The main program (`FMCW_Bulk_Data_Export.py`) configures radar hardware with chirp synchronization for improved signal quality, provides an interactive GUI with real-time visualization, and exports both raw data (CSV) and processed data (images) for each acquisition.

The system is designed to capture time-frequency representations of radar returns that can be used for machine learning applications such as object classification, presence detection, and range estimation.

## Theory

### FMCW Radar

Frequency Modulated Continuous Wave (FMCW) radar transmits a continuous signal whose frequency changes over time, typically in a linear pattern called a chirp. When this signal reflects off an object and returns to the receiver, the time delay causes a frequency difference between the transmitted and received signal. This frequency difference, or "beat frequency," is proportional to the distance to the target:

```
f_b = (2R·B)/(c·T_s)
```

Where:
- f_b is the beat frequency
- R is the range to the target
- B is the bandwidth of the chirp
- c is the speed of light
- T_s is the chirp duration

FMCW radar has advantages over pulsed radar for short-range applications because it:
- Requires less peak power
- Provides both range and velocity information
- Allows for simpler hardware implementations

### Range Resolution

Range resolution is the ability of a radar system to distinguish between two targets at different distances. It is determined by the bandwidth of the transmitted signal:

```
ΔR = c/(2·B)
```

Where:
- ΔR is the range resolution
- c is the speed of light
- B is the bandwidth of the chirp

With the default 1000 MHz bandwidth used in this project, the theoretical range resolution is approximately 15 cm (about 6 inches).

### Chirp Synchronization

In real-world systems, the start and end of each frequency chirp often introduce non-linearities in the signal. Chirp synchronization is a technique that mitigates this issue by:

1. Ignoring data from the beginning and end of each chirp cycle
2. Only processing the linear portion of the chirp
3. Synchronizing the data acquisition timing with the linear region of the transmitted waveform

The system uses Pluto's TDD (Time Division Duplex) engine to synchronize chirps with data acquisition, improving data quality and reducing false range readings.

### Constant False Alarm Rate (CFAR)

CFAR is an adaptive threshold technique used in radar systems to separate target returns from background noise. The algorithm works by examining cells surrounding a cell under test, estimating the background noise level, and applying an adaptive threshold to detect targets.

The technique maintains a constant probability of false alarm regardless of changing noise conditions, making detection more robust across different environments and scenarios.

CFAR processing is optional in this system and can be toggled via the GUI, allowing for comparison between raw and CFAR-processed data.

## Dataset Structure

The generated dataset is organized as follows:

```
DataSet/
├── [range_bin_1]/
│   ├── Images/
│   │   ├── [timestamp]_truedist[value]_calcdist[value]_bin[range]_img1.png
│   │   ├── [timestamp]_truedist[value]_calcdist[value]_bin[range]_img2.png
│   │   └── ...
│   └── FilteredCSV/
│   │   ├── [timestamp]_truedist[value]_calcdist[value]_bin[range]_img1.csv
│   │   ├── [timestamp]_truedist[value]_calcdist[value]_bin[range]_img2.csv
│   │   └── ...
├── [range_bin_2]/
└── ...
```

Each range bin corresponds to a class of images at a specific distance range. The images are visualizations of the time-frequency data, colorized using a Viridis colormap. The CSV files contain the raw frequency, magnitude, and calculated range data.

The dataset parameters:
- 6 classes (range bins) corresponding to approximately 6-inch increments
- 300 images per class
- 56×56 pixel resolution (configurable up to 256×256)
- Viridis colormap for visualization

## Requirements

- [Analog Devices CN0566 Phased Array Development Platform](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0566.html)
- [ADALM-Pluto SDR](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html) (with firmware ≥ v0.39)
- [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- Python 3.7+
- Network connection to Phaser platform

Python dependencies:
- NumPy
- PyQt5
- PyQtGraph
- OpenCV
- PyADI-IIO
- Matplotlib
- SciPy

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/starbelt/er-fmcw-dataset.git
   cd er-fmcw-dataset
   ```

2. Install required packages as needed:
   ```bash
   pip install numpy pyqt5 pyqtgraph opencv-python pyadi-iio matplotlib scipy
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```

4. Connect to the CN0566 Phaser platform:
   - Connect the Raspberry Pi physically to the CN0566 board (if using cutom setup)
   - Connect to the network where the Phaser is accessible (local, or port forward if public facing; hardwire if necessary)
   - Ensure the Pluto firmware is updated to v0.39 or later

## Usage

1. Configure the parameters in `FMCW_Bulk_Data_Export.py`:
   ```python
   # Distance configuration
   true_dist = 28.5  # inches (actual distance to target)
   namebin = 26.5    # inches (lower bound of range bin)
   
   # Dataset configuration
   img_size = 56     # Image size (px) - can be configured up to 256
   num_img = 25      # Number of images to collect per session
   ```

2. Run the program:
   ```bash
   python FMCW_Bulk_Data_Export.py
   ```

3. The program will:
   - Configure the radar hardware with chirp synchronization
   - Display an interactive GUI with real-time visualization
   - Provide options to toggle CFAR processing
   - Collect radar data
   - Generate both CSV data and image visualizations
   - Save files to the appropriate locations in the dataset structure
   - Automatically terminate after collecting sufficient data (configured by the `num_img` parameter)

# FMCW Radar Dataset Generator

This repository contains tools for generating radar datasets using Frequency Modulated Continuous Wave (FMCW) radar with Chirp Synchronization. The main program configures the Analog Devices CN0566 Phased Array (Phaser) Development Platform, provides an interactive GUI with optional Constant False Alarm Rate (CFAR) processing, and exports both raw data and processed images for machine learning applications.

## Table of Contents

- [Overview](#overview)
- [Theory](#theory)
  - [FMCW Radar](#fmcw-radar)
  - [Range Resolution](#range-resolution)
  - [Chirp Synchronization](#chirp-synchronization)
  - [Constant False Alarm Rate (CFAR)](#constant-false-alarm-rate-cfar)
- [Dataset Structure](#dataset-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Results and Data Format](#results-and-data-format)
  - [Sample Images](#sample-images)
  - [CSV Structure](#csv-structure)
- [File Descriptions](#file-descriptions)
- [License](#license)

## Overview

This project enables the creation of radar imaging datasets using low-cost Software Defined Radio (SDR) and phased array hardware. The main program (`FMCW_Bulk_Data_Export.py`) configures radar hardware with chirp synchronization for improved signal quality, provides an interactive GUI with real-time visualization, and exports both raw data (CSV) and processed data (images) for each acquisition.

The system is designed to capture time-frequency representations of radar returns that can be used for machine learning applications such as object classification, presence detection, and range estimation.

## Theory

### FMCW Radar

Frequency Modulated Continuous Wave (FMCW) radar transmits a continuous signal whose frequency changes over time, typically in a linear pattern called a chirp. When this signal reflects off an object and returns to the receiver, the time delay causes a frequency difference between the transmitted and received signal. This frequency difference, or "beat frequency," is proportional to the distance to the target:

```
f_b = (2R·B)/(c·T_s)
```

Where:
- f_b is the beat frequency
- R is the range to the target
- B is the bandwidth of the chirp
- c is the speed of light
- T_s is the chirp duration

FMCW radar has advantages over pulsed radar for short-range applications because it:
- Requires less peak power
- Provides both range and velocity information
- Allows for simpler hardware implementations

### Range Resolution

Range resolution is the ability of a radar system to distinguish between two targets at different distances. It is determined by the bandwidth of the transmitted signal:

```
ΔR = c/(2·B)
```

Where:
- ΔR is the range resolution
- c is the speed of light
- B is the bandwidth of the chirp

With the default 1000 MHz bandwidth used in this project, the theoretical range resolution is approximately 15 cm (about 6 inches).

### Chirp Synchronization

In real-world systems, the start and end of each frequency chirp often introduce non-linearities in the signal. Chirp synchronization is a technique that mitigates this issue by:

1. Ignoring data from the beginning and end of each chirp cycle
2. Only processing the linear portion of the chirp
3. Synchronizing the data acquisition timing with the linear region of the transmitted waveform

The system uses Pluto's TDD (Time Division Duplex) engine to synchronize chirps with data acquisition, improving data quality and reducing false range readings.

### Constant False Alarm Rate (CFAR)

CFAR is an adaptive threshold technique used in radar systems to separate target returns from background noise. The algorithm works by examining cells surrounding a cell under test, estimating the background noise level, and applying an adaptive threshold to detect targets.

The technique maintains a constant probability of false alarm regardless of changing noise conditions, making detection more robust across different environments and scenarios.

CFAR processing is optional in this system and can be toggled via the GUI, allowing for comparison between raw and CFAR-processed data.

## Dataset Structure

The generated dataset is organized as follows:

```
DataSet/
├── [range_bin_1]/
│   ├── Images/
│   │   ├── [timestamp]_truedist[value]_calcdist[value]_bin[range]_img1.png
│   │   ├── [timestamp]_truedist[value]_calcdist[value]_bin[range]_img2.png
│   │   └── ...
│   └── CSV/
│       └── [timestamp]_[fft_size]x[num_samples].csv
├── [range_bin_2]/
└── ...
```

Each range bin corresponds to a class of images at a specific distance range. The images are visualizations of the time-frequency data, colorized using a Viridis colormap. The CSV files contain the raw frequency, magnitude, and calculated range data.

The dataset parameters:
- 6 classes (range bins) corresponding to approximately 6-inch increments
- 300 images per class
- 56×56 pixel resolution (configurable up to 256×256)
- Viridis colormap for visualization

## Requirements

- [Analog Devices CN0566 Phased Array Development Platform](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0566.html)
- [ADALM-Pluto SDR](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html) (with firmware ≥ v0.39)
- [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- Python 3.7+
- Network connection to Phaser platform

Python dependencies:
- NumPy
- PyQt5
- PyQtGraph
- OpenCV
- PyADI-IIO
- Matplotlib
- SciPy

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/starbelt/er-fmcw-dataset.git
   cd er-fmcw-dataset
   ```

2. Install required packages as needed:
   ```bash
   pip install numpy pyqt5 pyqtgraph opencv-python pyadi-iio matplotlib scipy
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```

4. Connect to the CN0566 Phaser platform:
   - Connect the Raspberry Pi physically to the CN0566 board (if using custom setup)
   - Connect to the network where the Phaser is accessible (local, or port forward if public facing; hardwire if necessary)
   - Ensure the Pluto firmware is updated to v0.39 or later

## Usage

1. Configure the parameters in `FMCW_Bulk_Data_Export.py`:
   ```python
   # Distance configuration
   true_dist = 28.5  # inches (actual distance to target)
   namebin = 26.5    # inches (lower bound of range bin)
   
   # Dataset configuration
   img_size = 56     # Image size (px) - can be configured up to 256
   num_img = 25      # Number of images to collect per session
   ```

2. Run the program:
   ```bash
   python FMCW_Bulk_Data_Export.py
   ```

3. The program will:
   - Configure the radar hardware with chirp synchronization
   - Display an interactive GUI with real-time visualization
   - Provide options to toggle CFAR processing
   - Collect radar data
   - Generate both CSV data and image visualizations
   - Save files to the appropriate locations in the dataset structure
   - Automatically terminate after collecting sufficient data (configured by the `num_img` parameter)

## Results and Data Format

The system produces two types of output files:

1. **CSV files** with raw time-frequency radar data
2. **PNG images** that visualize the time-frequency data as spectrograms

### Sample Images

The generated images visualize time-frequency data from radar returns, providing a distinctive "signature" for objects at different distances. Each image is a 56×56 pixel (configurable up to 256×256) spectrogram using the Viridis colormap:

![Example Radar Image](DataSet/0.37-0.52/Images/0318-135453_truedist0.432_calcdist0.470_bin0.37-0.52m_img2.png)

*Example of radar return from an object at 0.432m. The program calculates its distance to be 0.470m which is within the range resolution of 0.15m. This image is from the 0.37-0.52m data set*

Each image filename contains important metadata:
- Timestamp of acquisition
- True distance to the target (measured physically to ±2.5cm)
- Calculated distance (determined by signal processing)
- Range bin classification
- Image number in sequence

For example: `0318-135453_truedist0.432_calcdist0.470_bin0.37-0.52m_img2.png` (image shown above)

### CSV Structure

The CSV files contain the raw data used to generate the images, with each file containing thousands of data points. The structure is as follows:

| Time Since Start (s) | Frequency (Hz) | Magnitude (dBFS) | Range (m) |
|----------------------|----------------|------------------|-----------|
| 0.0123 | 125034.5 | -43.21 | 0.673 |
| ... | ... | ... | ... |

- **Time Since Start (s)**: Time elapsed since data collection began
- **Frequency (Hz)**: Frequency bin of the FFT output
- **Magnitude (dBFS)**: Signal strength in decibels relative to full scale
- **Range (m)**: Calculated distance to target based on beat frequency

## File Descriptions

- `FMCW_Bulk_Data_Export.py`: Main program for bulk data collection and processing with FMCW and chirp synchronization
- `target_detection_dbfs.py`: Implementation of the CFAR algorithm for target detection
- `README.md`: This documentation file

## License

Some of the underlying hardware and software components use the Analog Devices license. See `AnalogDevicesLicense.txt` for more info.

## File Descriptions

- `FMCW_Bulk_Data_Export.py`: Main program for bulk data collection and processing with FMCW and chirp synchronization
- `target_detection_dbfs.py`: Implementation of the CFAR algorithm for target detection
- `README.md`: This documentation file

## License

Some of the underlying hardware and software components use the Analog Devices license. See `AnalogDevicesLicense.txt` for more info.
