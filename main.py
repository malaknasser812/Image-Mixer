from scipy.fft import fft
import scipy.signal as sig
import numpy as np
import pandas as pd
import pyqtgraph as pg
import os
import time
import pyqtgraph as pg
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog,QDialog, QGraphicsScene ,QLabel , QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5 import QtWidgets, uic 
from PyQt5.QtGui import QImage, QPixmap
from cmath import*
from numpy import *
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from Image import Image as ig
from Mixer import MyDialog as MX



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI Page
        uic.loadUi(r'task4.ui', self)
        #some variabels assosiated with gragging event
        self.delta_y = 0.0
        self.delta_x = 0.0
        self.setMouseTracking(True)
        self.mousePressPosition = None
        self.mouseMovePosition = None
        #button connection
        self.component_btn.clicked.connect(self.open_dialog)

        image_graphs = [self.image1, self.image2, self.image3, self.image4] #this is a list of qlabel widgets
        ft_image_graphs = [self.ft_compo_1, self.ft_compo_2, self.ft_compo_3, self.ft_compo_4]# a list of images of the ft components
        self.combos = [self.ft_combo1, self.ft_combo2, self.ft_combo3, self.ft_combo4]
        # Create a list to store Image instances and associated QLabel objects
        self.images = [ig(graph, ft_image, self.combos) for graph, ft_image in zip(image_graphs, ft_image_graphs)]
        self.output_graphs = [self.output1, self.output2]
        self.mixer = MX(self.output_graphs, self.images, self)

        #Connections
        # Connect combobox signals to the corresponding check_combo method
        # khodo balkoo hena fe code repeatitions 
        self.ft_combo1.activated.connect(lambda: self.combo_activated(0))
        self.ft_combo2.activated.connect(lambda: self.combo_activated(1))
        self.ft_combo3.activated.connect(lambda: self.combo_activated(2))
        self.ft_combo4.activated.connect(lambda: self.combo_activated(3))
        # Connect double-click events to each QLabel using a loop
        for label, image_instance in zip(image_graphs, self.images):
            label.mousePressEvent = lambda event, label_widget=label: self.mousePressEvent(event,label_widget)
            label.mouseMoveEvent = lambda event, label_widget=label: self.mouseMoveEvent(event,label_widget)
            label.mouseReleaseEvent = lambda event, instance=image_instance: self.mouseReleaseEvent(event,instance)

        for label, image_instance in zip(image_graphs, self.images):
            label.mouseDoubleClickEvent = lambda event, instance=image_instance: self.double_click_event(event, instance)
            
    def double_click_event(self, event, image_instance):
        if event.button() == Qt.LeftButton:
            image_instance.Browse()

# just to calculate the initial press position
    def mousePressEvent(self, event,label):
        if event.button() == Qt.LeftButton:
            label.mousePressPosition = event.pos()
            print(label.mousePressPosition)


    def mouseMoveEvent(self, event,label):
        if event.buttons() == Qt.LeftButton:
            delta_x = event.pos().x() - label.mousePressPosition.x()
            delta_y = event.pos().y() - label.mousePressPosition.y()
            self.delta_y = delta_y
            self.delta_x =delta_x


    def mouseReleaseEvent(self, event, image_instance):
        if event.button() == Qt.LeftButton:
            result = None
            image_instance.contrast_coef  = (-self.delta_y + 100) * 0.01
            result = image_instance.calculate_brightness_contrast(image_instance.image)
            print(result)
            image_instance.update_display(result)
        
    def combo_activated(self, index):
        for i, image_instance in enumerate(self.images):
            if i == index:
                # Update the selected combo box
                image_instance.check_combo(index)
            else:
                # Reset other combo boxes or perform other actions if needed
                pass

    def open_dialog(self):
        # Create an instance of the custom Mixer
        Mixer = MX(self.output_graphs, self.images, self)

        # Show the dialog
        Mixer.exec_()

    


    
        





       
        
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
