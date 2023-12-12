

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


class MyDialog(QtWidgets.QDialog):
    def __init__(self, outputgraphs, image, main):
        super(MyDialog, self).__init__()
        # Load the UI Page
        uic.loadUi(r'mixer.ui', self)

        self.outputgraphs = outputgraphs if outputgraphs is not None else []
        self.type1 = ''
        self.type2 = 'FT Magnitude'
        self.mode= None
        self.main = main
        print(self.main.images[0].ft_components)
        #print (self.ft_components, 'hello')self.comp1_hslider_1.setMinimum(0)
        self.comp1_hslider_1.setMinimum(0)
        self.comp1_hslider_1.setMaximum(1)
        self.comp1_hslider_1.setValue(1)
        self.comp1_hslider_2.setMinimum(0)
        self.comp1_hslider_2.setMaximum(1)
        self.comp1_hslider_2.setValue(1)

        self.output_channels_controlers = {
            'Output 1': {
                'select1 img': '',
                'select2 img': '',
                'slider1 val': 0,
                'slider2 va;': 0,
                'type1': '',
                'type2': ''
            },
            'Output 2': {
                'select1 img': '',
                'select2 img': '',
                'slider1 val': 0,
                'slider2 val': 0,
                'type1': '',
                'type2': ''
            }
        }
        


        #select type corresponding to the radio button toggled
        # self.mag_radioBtn_1.toggled.connect(lambda: self.select_type(1, 'FT Magnitude'))
        # self.phase_radioBtn_1.toggled.connect(lambda: self.select_type(1, 'FT Phase'))
        # self.real_radioBtn_1.toggled.connect(lambda: self.select_type(1, 'FT Real Component'))
        # self.imaginary_radioBtn_1.toggled.connect(lambda: self.select_type(1, 'FT Imaginary Component'))
        # self.mag_radioBtn_2.toggled.connect(lambda: self.select_type(2, 'FT Magnitude'))
        # self.phase_radioBtn_2.toggled.connect(lambda: self.select_type(2, 'FT Phase'))
        # self.real_radioBtn_2.toggled.connect(lambda: self.select_type(2, 'FT Real Component'))
        # self.imaginary_radioBtn_2.toggled.connect(lambda: self.select_type(2, 'FT Imaginary Component'))

        self.apply_btn.clicked.connect(self.pick_mix)


       

    def select_type(self,component,type):
        if component == 1: 
            self.type1 = type
        else : self.type2 = type

    # def pick_mix(self): #filling the output_channels_controlers dictionary
    #     outputgrpah = self.mixer_output_combobox.currentText()
    #     img1,self.output_channels_controlers[outputgrpah]['select1 img'] = self.input_img_selection_combobox_1.currentIndex()
    #     img2,self.output_channels_controlers[outputgrpah]['select2 img'] = self.input_img_selection_combobox_2.currentIndex()
    #     slider1,self.output_channels_controlers[outputgrpah]['slider1 val'] = self.comp1_hslider_1.value()
    #     slider2,self.output_channels_controlers[outputgrpah]['slider2 val'] = self.comp1_hslider_2.value()
    #     self.output_channels_controlers[outputgrpah]['type1'] = self.type1
    #     self.output_channels_controlers[outputgrpah]['type1'] = self.type2
    #     self.mix(img1,img2,slider1,slider2)

    def pick_mix(self): #filling the output_channels_controlers dictionary
        img1 = self.input_img_selection_combobox_1.currentIndex()
        img2 = self.input_img_selection_combobox_2.currentIndex()
        slider1 = self.comp1_hslider_1.value()
        slider2 = self.comp1_hslider_2.value()
        self.type1= self.mixer_combo_1.currentText()
        self.type2= self.mixer_combo_2.currentText()
        # self.output_channels_controlers[outputgrpah]['type1'] = self.type1
        # self.output_channels_controlers[outputgrpah]['type1'] = self.type2
        self.mix(img1,img2,slider1,slider2)


    def mix (self, img1, img2, slid1, slid2):
        outputgraph = self.mixer_output_combobox.currentIndex()
        first = self.get_component(img1,slid1,self.type1)
        second= self.get_component(img2,slid2,self.type2)

        if self.mode == 'mag-phase':
            construct = np.real(np.fft.ifft2(np.multiply(first, second)))
        if self.mode == 'real-imag':
            construct = np.real(np.fft.ifft2(first + second))
        
        if np.max(construct) > 1.0: #normalizing
            construct /= np.max(construct)
        print(construct)

        self.display_output(construct, outputgraph)
        

    def display_output(self, construct, outputIndex):
        outputgraph = self.outputgraphs[outputIndex]    
        
        image_height, image_width = construct.shape[:2]
        q_image = QImage(construct.data.tobytes(), image_width, image_height, QImage.Format_Grayscale8)

        # Convert QImage to QPixmap
        q_pixmap = QPixmap.fromImage(q_image)

        # Set the QPixmap as the pixmap for your QtLabel
        outputgraph.setPixmap(q_pixmap)
        #self.hide()



    def get_component(self, img, ratio,type)-> np.ndarray:
        
        print(self.main.images[img].ft_components)

        if type == "FT Magnitude":
            self.mode =  'mag-phase'
            print(self.mode,ratio)
            return self.main.images[img].ft_components[img][type] * ratio
        elif type == "FT Phase":
            self.mode =  'mag-phase'
            print(self.mode, ratio)
            return np.exp(1j * self.main.images[img].ft_components[img][type] * ratio)
        elif type == "FT Real":
            self.mode = 'real-imag'
            print(self.mode)
            return self.main.images[img].ft_components[img][type] * ratio
        elif type == "FT Imaginary":
            self.mode = 'real-imag'
            print(self.mode)
            return 1j* self.main.images[img].ft_components[img][type] * ratio
    
