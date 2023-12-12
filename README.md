# Fourier-Transform-Mixer
## Introduction :-
The Fourier Transform Mixer is a desktop application designed to illustrate the significance of magnitude and phase components within signals, using 2D grayscale images as an example. It allows users to manipulate and visualize the Fourier Transform components of four images, mix them using customizable weights, and control the selection of frequency regions for the output.
## Features :-
### Image Viewers
- Open and view four grayscale images in separate viewports.
- Automatic conversion of colored images to grayscale.
- Unified sizing of images to the smallest size among the opened images.
- Displays for each image showing Fourier Transform components: Magnitude, Phase, Real, Imaginary.

### Interaction :-
- Easy browsing to change any of the images by double-clicking on the viewer.
- Two output viewports for displaying the mixer result.
- Brightness/Contrast adjustment via mouse dragging for any image or its Fourier Transform components.

### Components Mixer :-
- Customizable weights for each image's Fourier Transform components using sliders.
- User-friendly interface for intuitive adjustment of weights for different components.

### Regions Mixer :-
- Selection of frequency regions (inner or outer) for each Fourier Transform component.
- Rectangular region drawing on Fourier Transform displays.
- Customizable size/percentage of the selected region via sliders or resize handles.
 ## Installation :-
1. Clone the repository
```sh
   git clone https://github.com/malaknasser812/Image-Mixer.git
 ```
2. Install project dependencies
```sh
   pip install logging
   pip install cmath
   pip install PyQt5
   pip install cv2
   pip install pandas
   pip install numpy
   pip install pyqtgraph
   pip install matplotlib
 ```
3. Run the application
```sh
   python Main.py
```


## Libraries :-
- PyQt5
- pyqtgraph
- time
- os
- matplotlib
- sys
- logging
- cv2
- numpy
- pandas

## Usage :-

### Launching the Application

After a successful installation, launch the application by executing the main script or running the designated entry point.

### Opening Images

- Open up to four grayscale images using the application's interface. If a colored image is loaded, the application automatically converts it to grayscale for processing.

- Mix and match grayscale and colored images within the four viewports. The application unifies the sizes of the opened images to the smallest size among them for consistency.

### Interacting with Fourier Transform Components

- Explore the Fourier Transform components of the images using the provided viewports:

  - Magnitude: View the magnitude spectrum, emphasizing the importance of the amplitude of various frequencies in the image.
  - Phase: Observe the phase spectrum, highlighting the phase information associated with different frequencies.
  - Real and Imaginary: Explore the real and imaginary components of the Fourier Transform, offering insights into the real and imaginary parts of the frequency domain representation.
- Double-click on a viewer to browse and change the image displayed in that specific viewport, facilitating easy comparison and analysis.

### Adjusting Brightness/Contrast

- Modify the brightness and contrast of the images or their Fourier Transform components using mouse interactions.

- Dragging up/down adjusts the brightness, while left/right movements alter the contrast. This functionality helps in visualizing and analyzing different aspects of the images and their frequency representations.

### Customizing Weights for Components Mixer

- Customize the weights assigned to each image's Fourier Transform components using sliders provided in the user interface.

- Adjust the weights intuitively to emphasize specific features or contributions of different components in the mixer result.

### Selecting Frequency Regions

- Define the frequency regions (inner or outer) for each Fourier Transform component:

  - Use rectangular drawing tools on the Fourier Transform displays to select specific frequency regions.
  - Customize the size or percentage of the selected region using sliders or resize handles.
  - Highlight the selected region for all four images to maintain consistency and observe their impact on the mixer result.
### Observing Mixer Result

- As adjustments are made to brightness/contrast, weights, and frequency regions, observe the resulting image in the output viewports.

- Compare and analyze the mixer results in real-time, understanding how different modifications affect the final combined image based on Fourier Transform manipulations.

## Our Team

- Hager Samir
- Camellia Marwan
- Farah Ossama
- Malak Nasser

