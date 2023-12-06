# from PyQt5 import Qt
from PyQt5.QtWidgets import QSlider,QHBoxLayout , QLabel ,QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage 
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt
import numpy as np
import logging

logging.basicConfig(filename="Image.log",level=logging.INFO , format='%(levelname)s: %(message)s')



class Image(QtWidgets.QWidget):
    def __init__(self, image_label,parent=None):
        super().__init__(parent)
        self.image = None
        self.width,self.height = 0,0
        self.image_label = image_label 



    def Browse(self):
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open Image File', './', filter="Image File (*.png *.jpg *.jpeg)")
        if image_path:
            new_image = QImage(image_path)
            new_width, new_height = new_image.width(), new_image.height()
            if self.image is not None and (new_width, new_height) != (self.width, self.height):
                # Sizes are different, apply adjust_image_sizes function
                self.adjust_sizes()
            if new_image.format() == QImage.Format.Format_Grayscale8:
                self.update_display(new_image)
            else:
                new_image = new_image.convertToFormat(QImage.Format.Format_Grayscale8)
                self.update_display(new_image)
            # Update self.image after loading the first image
            self.image = new_image
            self.width, self.height = new_width, new_height

                
    def update_display(self,image):
        # self.image_label.setScaledContents(True)
        self.image = image
        pixmap = QPixmap.fromImage(self.image)
        self.image_label.setPixmap(pixmap)

    def adjust_sizes(self):
    # Check if there are images in the viewports
        if any(image.image is not None for image in self.images):
            # Find the smallest width and height among all images
            min_width = min(image.width for image in self.images if image.image is not None)
            min_height = min(image.height for image in self.images if image.image is not None)

            # Resize images in all instances to the smallest size
            for image in self.images:
                if image.image is not None:
                    new_image = image.image.scaled(min_width, min_height, Qt.AspectRatioMode.KeepAspectRatio)
                    image.update_display(new_image)



    def Calculations (self):
        if self.image != None :
            buffer = self.image.bits().asarray().data
            # Reshape the array to match the image dimensions
            image_array = (np.frombuffer(buffer, dtype=np.uint8)).T


    def process(self, img_mag, img_phase, img_real, img_imag):
        mag_mask = np.ones_like(img_mag)
        phase_mask = np.zeros_like(img_phase)
        real_mask = np.ones_like(img_real)
        imag_mask = np.zeros_like(img_imag)
        return mag_mask, phase_mask, real_mask, imag_mask
    
    def crop_low_freq(self, mode, img_mag, img_phase, img_real, img_imag):
        magnitude_mask, phase_mask, real_mask, imag_mask = self.process(img_mag, img_phase, img_real, img_imag)
        for h in range(int(self.current_y ), int( self.height -self.current_y)):
            for w in range(int(self.current_x), int( self.width - self.current_x)):
                if mode == 'mag':
                    magnitude_mask[h][w] = img_mag[h][w]
                elif mode == 'phase':
                    phase_mask[h][w] = img_phase[h][w]
                elif mode == 'real':
                    real_mask[h][w] = img_real[h][w]
                elif mode == 'imag':
                    imag_mask[h][w] = img_imag[h][w]
        if mode == 'mag':
            return magnitude_mask
        elif mode == 'phase':
            return phase_mask
        elif mode == 'real':
            return real_mask
        elif mode == 'imag':
            return imag_mask

    def crop_high_freq(self, mode, img_mag, img_phase, img_real, img_imag):
        magnitude_mask, phase_mask, real_mask, imag_mask = self.process(img_mag, img_phase, img_real, img_imag)
        for h in range(int(self.current_y ), int( self.height -self.current_y)):
            for w in range(int(self.current_x), int( self.width - self.current_x)):
                if mode == 'mag':
                    img_mag[h][w] = magnitude_mask[h][w]
                elif mode == 'phase':
                    img_phase[h][w] = phase_mask[h][w]
                elif mode == 'real':
                    img_real[h][w] = real_mask[h][w]
                elif mode == 'imag':
                    img_imag[h][w] = imag_mask[h][w]
        if mode == 'mag':
            return img_mag
        elif mode == 'phase':
            return img_phase
        elif mode == 'real':
            return img_real
        elif mode == 'imag':
            return img_imag