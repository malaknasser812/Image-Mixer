# from PyQt5 import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene,QGraphicsRectItem,QGraphicsItemGroup,QSlider,QHBoxLayout , QLabel ,QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage,QColor
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt,QRectF , QSizeF
import numpy as np
import logging
import cv2

logging.basicConfig(filename="Image.log",level=logging.INFO , format='%(levelname)s: %(message)s')

class Image(QtWidgets.QWidget):
    instances =[]
    all_regions = []
    def __init__(self, image,ft_image, combos, parent=None):
        super().__init__(parent)
        self.image = None
        self.width,self.height = 0,0
        self.image_label = image
        self.ft_components = {}
        self.ft_image_label = ft_image
        self.magnitude_shift = None
        self.phase_shift = None
        self.real_shift = None
        self.imaginary_shift = None
        self.calculated = {}
        
        self.region_item = None  # QGraphicsRectItem for representing the selected region
        self.region_start = None  # Starting point of the region
        self.region_end = None  # Ending point of the region
        self.region_width = 0  # Width of the region
        self.region_height = 0  # Height of the region
        self.active_region_item = None  # Variable to keep track of the currently active region
        self.region_group = None  # Variable to keep track of the QGraphicsItemGroup
        self.combos = combos if combos is not None else []  # Initialize as an empty list if not provided
        self.contrast_coef , self.brightness_coef= 1.0,0.0
        # Append each instance to the class variable
        Image.instances.append(self)
        
    def Browse(self):
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open Image File', './', filter="Image File (*.png *.jpg *.jpeg)")
        if image_path:
            # Load the image using cv2
            cv_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if cv_image is not None:
                #this reterns a tuple with three elements it is the height , width and number of channels
                new_height, new_width = cv_image.shape[:2]
                if self.image is not None and (new_width, new_height) != (self.width, self.height):
                    # Sizes are different, apply adjust_image_sizes function
                    self.adjust_sizes()
                # Update display using cv2 image
                self.update_display(cv_image)
                # Update self.image after loading the first image
                self.image = cv_image
                self.width, self.height = new_width, new_height
                # Adjust sizes after updating the display
                self.adjust_sizes()

    def update_display(self, cv_image):
        if cv_image is not None:
            # Update self.image with the cv_image
            self.image = cv_image
            # Convert cv_image to QPixmap
            height, width = cv_image.shape[:2]
            bytes_per_line = width
            # Create QImage from cv_image
            q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
            # Convert QImage to QPixmap and set the display
            q_pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(q_pixmap)

    def adjust_sizes(self):
        # Check if there are images in the instances list
        valid_images = [image for image in Image.instances if image.image is not None]
        if valid_images:
            # Find the smallest width and height among all images
            min_width = min(image.width for image in valid_images)
            min_height = min(image.height for image in valid_images)

            # Resize images in all instances to the smallest size
            for image in valid_images:
                # Resize the original image using cv2
                resized_image = cv2.resize(image.image, (min_width, min_height))
                # Update the original image display
                image.update_display(resized_image)

                # Resize the FT component image using QGraphicsView
                if hasattr(image.ft_image_label, 'scene'):
                    # Check if the scene exists
                    if image.ft_image_label.scene() is None:
                        # Create a new scene
                        image.ft_image_label.setScene(QGraphicsScene())

                    # Clear the scene before updating
                    image.ft_image_label.scene().clear()

                    # Retrieve the FT component from stored calculations
                    index = Image.instances.index(image)
                    selected_combo = image.combos[index].currentText()

                    # Ensure that the selected_combo exists in the dictionary before accessing it
                    if selected_combo in image.ft_components.get(index, {}):
                        selected_component = image.ft_components[index][selected_combo]

                        # Resize the FT component image using cv2
                        resized_ft_component = cv2.resize(selected_component, (min_width, min_height))

                        # Update the FT component display
                        image.update_ft_display(resized_ft_component)

    def Calculations(self, index):
        if self.image is not None:
            # Convert uint8 array to float64
            image_array_float = self.image.astype(np.float64)
            self.dft = np.fft.fft2(image_array_float)
            self.dft_shift = np.fft.fftshift(self.dft)
            epsilon = 1e-10  # Small constant to avoid log(0)
            self.magnitude_shift = (20 * np.log(np.abs(self.dft_shift) + epsilon)).astype(np.uint8)
            self.phase_shift = (np.angle(self.dft_shift)).astype(np.uint8)
            self.real_shift = (20 * np.log(np.abs(np.real(self.dft_shift)) + epsilon)).astype(np.uint8)
            self.imaginary_shift = (np.imag(self.dft_shift)).astype(np.uint8)
            if index not in self.ft_components:
                self.ft_components[index] = {}
            self.calculated[index] = True
            self.ft_components[index] = {
                "FT Magnitude": self.magnitude_shift,
                "FT Phase": self.phase_shift,
                "FT Real": self.real_shift,
                "FT Imaginary": self.imaginary_shift
            }
    def update_ft_display(self, cv_image):
        if cv_image is not None:
            # Convert the NumPy array to QPixmap
            q_image = QImage(cv_image.data.tobytes(), cv_image.shape[1], cv_image.shape[0], QImage.Format_Grayscale8)
            pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(q_image))

            # Clear the scene before updating
            self.ft_image_label.scene().clear()

            # Add the item to the scene
            self.ft_image_label.scene().addItem(pixmap_item)

            # Set the scene rect to match the item rect
            self.ft_image_label.scene().setSceneRect(QRectF(pixmap_item.pixmap().rect()))

            # Check if the region_item is still in the scene
            if self.region_item is not None and self.region_item in self.ft_image_label.scene().items():
                # Remove the region_item from the scene before updating
                self.ft_image_label.scene().removeItem(self.region_item)

            # Add the region_item to the scene if it exists
            if self.region_item is not None:
                self.draw_region_rectangle()
                
    def calculate_brightness_contrast(self, cv_image):
            result=None
            if cv_image is not None:
                print( self.brightness_coef)
                result = cv2.addWeighted(cv_image, self.contrast_coef, np.zeros_like(cv_image), 0, self.brightness_coef)
                self.image = result
            return result
    

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Remove existing regions from the scene
            for item in self.ft_image_label.scene().items():
                if isinstance(item, QGraphicsRectItem):
                    self.ft_image_label.scene().removeItem(item)

            # Store the starting point of the region if it's the first click
            if self.region_start is None:
                self.region_start = event.pos()

            # Create a new QGraphicsRectItem for the selected region
            self.region_item = QGraphicsRectItem(QRectF(self.region_start, event.pos()))
            self.region_item.setPen(QColor(255, 0, 0))  # Red border

            # Add the region_item to the scene
            self.ft_image_label.scene().addItem(self.region_item)



    def mouseMoveEvent(self, event):
        if self.region_start is not None:
            # Update the size of the active region dynamically
            self.update_region_rectangle(event.pos())


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.region_start is not None:
            # Store the ending point of the region
            self.region_end = event.pos()

            # Calculate the width and height of the region
            self.region_width = abs(self.region_end.x() - self.region_start.x())
            self.region_height = abs(self.region_end.y() - self.region_start.y())

            # Draw the final region rectangle
            self.draw_region_rectangle()
            self.all_regions.append(self.region_item.rect())

            # Reset the region variables for the next selection
            self.region_start = None
            self.region_end = None
            self.region_width = 0
            self.region_height = 0

            # Set region_item to None to avoid accessing it later
            self.region_item = None
    def update_region_rectangle(self, current_pos):
        # Update the region rectangle dynamically
        if self.region_item is not None:
            self.region_item.setRect(QRectF(self.region_start, current_pos))
    def draw_region_rectangle(self):
        if self.region_start is not None and self.region_end is not None:
            # Create a semi-transparent red rectangle representing the selected region
            self.region_item = QGraphicsRectItem(QRectF(self.region_start, self.region_end))
            self.region_item.setBrush(QColor(255, 0, 0, 100))  # Red with 100 alpha (semi-transparent)

            # Add the region_item to the scene
            self.ft_image_label.scene().addItem(self.region_item)

    def check_combo(self, index):
        if index not in self.calculated:
            self.Calculations(index)
        selected_combo = self.combos[index].currentText()
        if selected_combo in self.ft_components[index]:
            selected_component = self.ft_components[index][selected_combo]
            self.update_ft_display(selected_component)

