import sys
import math
import os
import time
import cv2
import numpy as np
import mysql.connector as mc
from scipy.stats import skew, kurtosis
from PyQt5.QtCore import QTime, QDateTime, QDate, Qt, QRect
from PyQt5.QtGui import QFont, QImage, QPixmap, QBrush, QWindow, QPainter, QIcon
from PyQt5.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, \
    QGridLayout, QLineEdit, QPushButton, QListWidget, QApplication, QComboBox, QSpinBox, \
    QFontComboBox, QTimeEdit, QDateTimeEdit, QDateEdit, QCalendarWidget, QCheckBox, QSlider, \
    QLCDNumber, QProgressBar, QTreeWidget, QTreeWidgetItem, QMainWindow, QStatusBar, QToolBar, QAction, QFileDialog, \
    QErrorMessage, QFrame, QDesktopWidget, QMenuBar, QMenu, QRadioButton
import getopt
from skimage.feature import greycomatrix, greycoprops

# MAIN WINDOW
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        self.filename = None

        #self.move(30,30)
        self.resize(1600, 900)
        self.setCenter()
        self.setWindowTitle('DIP MAIN WINDOW')
        #self.label = QLabel()
        #self.label.move(0,0)
        #self.label.resize(1200, 20)
        #self.label.setText("DIGITAL IMAGE PROCESSING")
        #self.label.setStyleSheet("background : white;")
        #font = QFont()
        #font.setFamily("Myriad Pro")
        #font.setPointSize(12)
        #font.setBold(True)
        #font.setItalic(False)
        #font.setWeight(75)
        #self.label.setFont(font)
        #self.label.setAlignment(Qt.AlignCenter)
        #self.label.setParent(self)
        captureImage = QIcon('09-gui-icon/camera.png')
        self.captureButton = QPushButton('\tCAPTURE')
        self.captureButton.setStatusTip("Capture images")
        self.captureButton.setToolTip("Capture images ")
        self.captureButton.setIcon(captureImage)
        self.captureButton.move(20, 10)
        self.captureButton.resize(100, 30)
        self.captureButton.setParent(self)
        #self.uploadButton.setStyleSheet("background : white;")
        uploadImage = QIcon('09-gui-icon/upload.png')
        self.uploadButton = QPushButton('\tUPLOAD')
        self.uploadButton.setStatusTip("Upload image to get features")
        self.uploadButton.setToolTip("Upload Image")
        self.uploadButton.setIcon(uploadImage)
        self.uploadButton.move(25, 630)
        self.uploadButton.resize(100, 30)
        self.uploadButton.setParent(self)

        self.path_ = QLineEdit()
        self.path_.move(150, 630)
        self.path_.resize(160, 30)
        self.path_.setAlignment(Qt.AlignLeft)
        self.path_.setFont(QFont('SansSerif', 10))
        self.path_.setToolTip("Input ID Sample")
        self.path_.setEnabled(False)
        self.path_.setStyleSheet("background : white;")
        self.path_.setParent(self)

        classifyIcon = QIcon('09-gui-icon/classify.png')
        self.classifyButton = QPushButton('\tCLASSIFY')
        self.classifyButton.setIcon(classifyIcon)
        self.classifyButton.move(120,10)
        self.classifyButton.resize(100, 30)
        self.classifyButton.setParent(self)

        db = QIcon('09-gui-icon/database.png')
        self.connectDBButton = QPushButton('\tDATABASE')
        self.connectDBButton.setIcon(db)
        self.connectDBButton.setToolTip("Check Database Connection")
        self.connectDBButton.move(220, 10)
        self.connectDBButton.resize(100,30)
        self.connectDBButton.setParent(self)

        roi = QIcon('09-gui-icon/coffee_bean.png')
        self.roiButton = QPushButton('\tROI')
        self.roiButton.setIcon(roi)
        self.roiButton.setToolTip("Get Region of Interest")
        self.roiButton.move(320, 10)
        self.roiButton.resize(100,30)
        self.roiButton.setParent(self)

        closeIcon = QIcon('09-gui-icon/exit.png')
        self.exitButton = QPushButton('\tCLOSE')
        self.exitButton.setToolTip("Quit Application")
        self.exitButton.move(1480, 855)
        self.exitButton.resize(100, 30)
        self.exitButton.setIcon(closeIcon)
        self.exitButton.setParent(self)

        self.author = QLabel('<b>© 2022 AGUS DHARMAWAN | DIGITAL IMAGE PROCESSING</b>')
        self.author.move(26, 857)
        self.author.resize(400, 30)
        self.author.setParent(self)

        helIcon = QIcon('09-gui-icon/help.png')
        self.helpButton = QPushButton()
        self.helpButton.move(1550, 10)
        self.helpButton.resize(30, 30)
        self.helpButton.setIcon(helIcon)
        self.helpButton.setParent(self)

        self.source_filename = None
        self.max_imgWidth = 512
        self.max_imgHeight = 512

        self.label1 = QLabel('<b>PREVIEW IMAGE</b>')
        self.label1.move(25, 55)
        self.label1.setParent(self)
        self.label2 = QLabel('<b>SHOW PROCESSED IMAGE</b>')
        self.label2.move(560, 55)
        self.label2.setParent(self)

        self.originalImage = QLabel()
        self.originalImage.setMaximumSize(self.max_imgWidth, self.max_imgHeight)
        self.originalImage.move(25, 80)
        self.originalImage.resize(512, 512)
        self.originalImage.setAlignment(Qt.AlignCenter)
        self.originalImage.setParent(self)
        self.originalImage.setStyleSheet("background : white;")

        self.processedImage = QLabel()
        self.processedImage.setMaximumSize(self.max_imgWidth, self.max_imgHeight)
        self.processedImage.move(560, 80)
        self.processedImage.resize(512, 512)
        self.processedImage.setParent(self)
        self.processedImage.setStyleSheet("background : white;")

        # DEFINISIKAN BUTTONS DI MAIN FORM
        self.captureButton.clicked.connect(self.captureButtonClick)
        self.uploadButton.clicked.connect(self.uploadButtonClick)
        self.connectDBButton.clicked.connect(self.connectDBButtonClick)
        self.roiButton.clicked.connect(self.roiButtonClick)
        self.helpButton.clicked.connect(self.helpButtonClick)
        self.exitButton.clicked.connect(self.exitButtonClick)

        # ZOOM IN AND OUT ORIGINAL IMAGE
        #zoomin = QIcon('09-gui-icon/zoomin.png')
        #self.zoomin = QPushButton()
        #self.zoomin.setIcon(zoomin)
        #self.zoomin.setToolTip("Zoom in")
        #self.zoomin.move(435, 45)
        #self.zoomin.resize(35, 30)
        #self.zoomin.setParent(self)
        #self.zoomin.clicked.connect(self.big_img)

        #zoomout = QIcon('09-gui-icon/zoomout.png')
        #self.zoomout = QPushButton()
        #self.zoomout.setIcon(zoomout)
        #self.zoomout.setToolTip("Zoom out")
        #self.zoomout.move(470, 45)
        #self.zoomout.resize(35, 30)
        #self.zoomout.setParent(self)
        #self.zoomout.clicked.connect(self.small_img)

        #save1 = QIcon('09-gui-icon/save.png')
        #self.save1 = QPushButton()
        #self.save1.setIcon(save1)
        #self.save1.setToolTip("Save Resized Image")
        #self.save1.move(505, 45)
        #self.save1.resize(35, 30)
        #self.save1.setParent(self)
        #self.save1.clicked.connect(self.saveimgresized)

        #rotLeft90 = QIcon('09-gui-icon/icon-rotate-right-90.png')
        #self.rotateLeft = QPushButton()
        #self.rotateLeft.setIcon(rotLeft90)
        #self.rotateLeft.setToolTip("Rotate Left 90°")
        #self.rotateLeft.move(400, 45)
        #self.rotateLeft.resize(35, 30)
        #self.rotateLeft.setParent(self)
        #self.rotateLeft.clicked.connect(self.rotateLeftClick)
        #rotRight90 = QIcon('09-gui-icon/icon-rotate-left-90.png')
        #self.rotateRight = QPushButton()
        #self.rotateRight.setIcon(rotRight90)
        #self.rotateRight.setToolTip("Rotate Right 90°")
        #self.rotateRight.move(365, 45)
        #self.rotateRight.resize(35, 30)
        #self.rotateRight.setParent(self)
        #self.rotateRight.clicked.connect(self.rotateRightClick)
        #flipV = QIcon('09-gui-icon/flip-vertical.png')
        #self.flipVertical = QPushButton()
        #self.flipVertical.setIcon(flipV)
        #self.flipVertical.setToolTip("Flip Vertically")
        #self.flipVertical.move(330, 45)
        #self.flipVertical.resize(35, 30)
        #self.flipVertical.setParent(self)
        #self.flipVertical.clicked.connect(self.flipVerticalClick)
        #flipH = QIcon('09-gui-icon/flip-horizontal.png')
        #self.flipHorizontal = QPushButton()
        #self.flipHorizontal.setIcon(flipH)
        #self.flipHorizontal.setToolTip("Flip Horizontally")
        #self.flipHorizontal.move(295, 45)
        #self.flipHorizontal.resize(35, 30)
        #self.flipHorizontal.setParent(self)
        #self.flipHorizontal.clicked.connect(self.flipHorizontalClick)

        self.Hline = QFrame()
        self.Hline.setFrameShape(QFrame.HLine)
        self.Hline.setFrameShadow(QFrame.Sunken)
        self.Hline.move(25, 595)
        self.Hline.resize(1070, 20)
        self.Hline.setParent(self)
        self.smoothingCombo = QComboBox()

        self.label6 = QLabel('<b>IMAGE PREPROCESSING</b>')
        self.label6.move(25, 680)
        self.label6.setParent(self)

        # ====== SMOOTHING ==================================================
        self.label3 = QLabel('SMOOTHING')
        self.label3.move(25, 710)
        self.label3.setParent(self)

        self.noneBlur = QRadioButton()
        self.noneBlur.setText('None')
        self.noneBlur.setChecked(True)
        self.noneBlur.move(120, 710)
        self.noneBlur.setParent(self)

        self.cvBlur = QRadioButton()
        self.cvBlur.setText('cvBlur')
        self.cvBlur.move(200, 710)
        self.cvBlur.setParent(self)

        self.medianBlur = QRadioButton()
        self.medianBlur.setText('MedianBlur')
        self.medianBlur.move(280, 710)
        self.medianBlur.setParent(self)

        self.gausBlur = QRadioButton()
        self.gausBlur.setText('Gaus.Blur')
        self.gausBlur.move(360, 710)
        self.gausBlur.setParent(self)

        self.boxFilter = QRadioButton()
        self.boxFilter.setText('BoxFilter')
        self.boxFilter.move(440, 710)
        self.boxFilter.setParent(self)

        self.bilateralFilter = QRadioButton()
        self.bilateralFilter.setText('BilateralFilter')
        self.bilateralFilter.move(520, 710)
        self.bilateralFilter.setParent(self)

        self.noneBlur.clicked.connect(self.noneBlurClick)
        self.cvBlur.clicked.connect(self.cvBlurClick)
        self.medianBlur.clicked.connect(self.medianBlurClick)
        self.gausBlur.clicked.connect(self.gausBlurClick)
        self.boxFilter.clicked.connect(self.boxFilterClick)
        self.bilateralFilter.clicked.connect(self.bilateralFilterClick)

        # ====== DENOISING ==================================================
        self.label4 = QLabel('DENOISING')
        self.label4.move(25, 740)
        self.label4.setParent(self)

        self.denoise0 = QRadioButton()
        self.denoise0.setText('None')
        self.denoise0.move(120, 740)
        self.denoise0.setParent(self)
        #self.denoise0.setChecked(True)

        self.denoise1 = QRadioButton()
        self.denoise1.setText('fansNlMeansDonoising')
        self.denoise1.move(200, 740)
        self.denoise1.setParent(self)

        self.denoise2 = QRadioButton()
        self.denoise2.setText('fansNlMeansDonoisingColored')
        self.denoise2.move(360, 740)
        self.denoise2.setParent(self)

        self.denoise0.clicked.connect(self.denoise0Click)
        self.denoise1.clicked.connect(self.denoise1Click)
        self.denoise2.clicked.connect(self.denoise2Click)

        # ====== IMAGE ENHANCEMENT ==========================================
        self.label7 = QLabel('CONTRAST')
        self.label7.move(25, 780)
        self.label7.setParent(self)

        self.label8 = QLabel('BRIGHTNESS')
        self.label8.move(270, 780)
        self.label8.setParent(self)

        self.alphaTxt = QLineEdit()
        self.alphaTxt.move(100, 780)
        self.alphaTxt.resize(60, 30)
        self.alphaTxt.setAlignment(Qt.AlignCenter)
        self.alphaTxt.setFont(QFont('SansSerif', 12))
        self.alphaTxt.setParent(self)

        self.betaTxt = QLineEdit()
        self.betaTxt.move(350, 780)
        self.betaTxt.resize(60, 30)
        self.betaTxt.setAlignment(Qt.AlignCenter)
        self.betaTxt.setFont(QFont('SansSerif', 12))
        self.betaTxt.setParent(self)

        self.enhanceButton = QPushButton('Enhance')
        self.enhanceButton.move(500, 780)
        self.enhanceButton.resize(80, 30)
        self.enhanceButton.setParent(self)
        self.enhanceButton.clicked.connect(self.enhanceButtonClick)

        self.label37 = QLabel('(1.0 - 3.0)')
        self.label37.move(170, 785)
        self.label37.setParent(self)

        self.label38 = QLabel('(0 - 100)')
        self.label38.move(420, 785)
        self.label38.setParent(self)

        # ====== BACKGROUND REMOVAL =================================
        #self.label6 = QLabel('<b>REMOVE BACKGROUND</b>')
        #self.label6.move(1120, 550)
        #self.label6.setParent(self)

        self.bgremovalButton = QPushButton('Remove BG')
        self.bgremovalButton.move(1120, 550)
        self.bgremovalButton.resize(100,30)
        self.bgremovalButton.setParent(self)
        self.bgremovalButton.clicked.connect(self.bgremovalButtonClick)

        #self.label6 = QLabel('<b>FEATURE EXTRACTION</b>')
        #self.label6.move(1355, 75)
        #self.label6.setParent(self)

        self.colorFeatures = QPushButton('COLOR')
        self.colorFeatures.move(1120, 80)
        self.colorFeatures.resize(80, 30)
        self.colorFeatures.setParent(self)
        self.colorFeatures.clicked.connect(self.colorFtrButtonClick)

        self.textureFeatures = QPushButton('TEXTURE')
        self.textureFeatures.move(680, 615)
        self.textureFeatures.resize(80, 30)
        self.textureFeatures.setParent(self)
        self.textureFeatures.clicked.connect(self.textureFtrButtonClick)

        self.shapeFeatures = QPushButton('SHAPE')
        self.shapeFeatures.move(1220, 550)
        self.shapeFeatures.resize(80, 30)
        self.shapeFeatures.setParent(self)
        self.shapeFeatures.clicked.connect(self.shapeFtrButtonClick)

        self.Vline2 = QFrame()
        self.Vline2.setFrameShape(QFrame.VLine)
        self.Vline2.setFrameShadow(QFrame.Sunken)
        self.Vline2.move(650,615)
        self.Vline2.resize(20, 215)
        self.Vline2.setParent(self)

        self.Vline = QFrame()
        self.Vline.setFrameShape(QFrame.VLine)
        self.Vline.setFrameShadow(QFrame.Sunken)
        self.Vline.move(1085, 80)
        self.Vline.resize(20,750)
        self.Vline.setParent(self)

        self.label11 = QLabel('<b>R</b>')
        self.label11.move(1220, 120)
        self.label11.setParent(self)
        self.label12 = QLabel('<b>G</b>')
        self.label12.move(1350, 120)
        self.label12.setParent(self)
        self.label13 = QLabel('<b>B</b>')
        self.label13.move(1480, 120)
        self.label13.setParent(self)

        self.label14 = QLabel('<b>Mean</b>')
        self.label14.move(1120, 140)
        self.label14.setParent(self)

        self.rmean = QLineEdit()
        self.rmean.move(1220, 140)
        self.rmean.resize(100, 25)
        self.rmean.setAlignment(Qt.AlignRight)
        self.rmean.setFont(QFont('SansSerif', 10))
        self.rmean.setEnabled(False)
        self.rmean.setStyleSheet("background : white;")
        self.rmean.setParent(self)

        self.gmean = QLineEdit()
        self.gmean.move(1350, 140)
        self.gmean.resize(100, 25)
        self.gmean.setAlignment(Qt.AlignRight)
        self.gmean.setFont(QFont('SansSerif', 10))
        self.gmean.setEnabled(False)
        self.gmean.setParent(self)
        self.gmean.setStyleSheet("background : white;")

        self.bmean = QLineEdit()
        self.bmean.move(1480, 140)
        self.bmean.resize(100, 25)
        self.bmean.setAlignment(Qt.AlignRight)
        self.bmean.setFont(QFont('SansSerif', 10))
        self.bmean.setEnabled(False)
        self.bmean.setParent(self)
        self.bmean.setStyleSheet("background : white;")

        self.label15 = QLabel('<b>Std. Dev.</b>')
        self.label15.move(1120, 170)
        self.label15.setParent(self)

        self.rsd = QLineEdit()
        self.rsd.move(1220, 170)
        self.rsd.resize(100, 25)
        self.rsd.setAlignment(Qt.AlignRight)
        self.rsd.setFont(QFont('SansSerif', 10))
        self.rsd.setEnabled(False)
        self.rsd.setStyleSheet("background : white;")
        self.rsd.setParent(self)

        self.gsd = QLineEdit()
        self.gsd.move(1350, 170)
        self.gsd.resize(100, 25)
        self.gsd.setAlignment(Qt.AlignRight)
        self.gsd.setFont(QFont('SansSerif', 10))
        self.gsd.setEnabled(False)
        self.gsd.setParent(self)
        self.gsd.setStyleSheet("background : white;")

        self.bsd = QLineEdit()
        self.bsd.move(1480, 170)
        self.bsd.resize(100, 25)
        self.bsd.setAlignment(Qt.AlignRight)
        self.bsd.setFont(QFont('SansSerif', 10))
        self.bsd.setEnabled(False)
        self.bsd.setParent(self)
        self.bsd.setStyleSheet("background : white;")

        self.label17 = QLabel('<b>Skewness</b>')
        self.label17.move(1120, 200)
        self.label17.setParent(self)

        self.rskew = QLineEdit()
        self.rskew.move(1220, 200)
        self.rskew.resize(100, 25)
        self.rskew.setAlignment(Qt.AlignRight)
        self.rskew.setFont(QFont('SansSerif', 10))
        self.rskew.setEnabled(False)
        self.rskew.setStyleSheet("background : white;")
        self.rskew.setParent(self)

        self.gskew = QLineEdit()
        self.gskew.move(1350, 200)
        self.gskew.resize(100, 25)
        self.gskew.setAlignment(Qt.AlignRight)
        self.gskew.setFont(QFont('SansSerif', 10))
        self.gskew.setEnabled(False)
        self.gskew.setParent(self)
        self.gskew.setStyleSheet("background : white;")

        self.bskew = QLineEdit()
        self.bskew.move(1480, 200)
        self.bskew.resize(100, 25)
        self.bskew.setAlignment(Qt.AlignRight)
        self.bskew.setFont(QFont('SansSerif', 10))
        self.bskew.setEnabled(False)
        self.bskew.setParent(self)
        self.bskew.setStyleSheet("background : white;")

        self.label18 = QLabel('<b>Kurtosis</b>')
        self.label18.move(1120, 230)
        self.label18.setParent(self)

        self.rkurt = QLineEdit()
        self.rkurt.move(1220, 230)
        self.rkurt.resize(100, 25)
        self.rkurt.setAlignment(Qt.AlignRight)
        self.rkurt.setFont(QFont('SansSerif', 10))
        self.rkurt.setEnabled(False)
        self.rkurt.setStyleSheet("background : white;")
        self.rkurt.setParent(self)

        self.gkurt = QLineEdit()
        self.gkurt.move(1350, 230)
        self.gkurt.resize(100, 25)
        self.gkurt.setAlignment(Qt.AlignRight)
        self.gkurt.setFont(QFont('SansSerif', 10))
        self.gkurt.setEnabled(False)
        self.gkurt.setParent(self)
        self.gkurt.setStyleSheet("background : white;")

        self.bkurt = QLineEdit()
        self.bkurt.move(1480, 230)
        self.bkurt.resize(100, 25)
        self.bkurt.setAlignment(Qt.AlignRight)
        self.bkurt.setFont(QFont('SansSerif', 10))
        self.bkurt.setEnabled(False)
        self.bkurt.setParent(self)
        self.bkurt.setStyleSheet("background : white;")

        self.label11 = QLabel('<b>H</b>')
        self.label11.move(1220, 265)
        self.label11.setParent(self)
        self.label12 = QLabel('<b>S</b>')
        self.label12.move(1350, 265)
        self.label12.setParent(self)
        self.label13 = QLabel('<b>V</b>')
        self.label13.move(1480, 265)
        self.label13.setParent(self)

        self.label14 = QLabel('<b>Mean</b>')
        self.label14.move(1120, 285)
        self.label14.setParent(self)

        self.Hmean = QLineEdit()
        self.Hmean.move(1220, 285)
        self.Hmean.resize(100, 25)
        self.Hmean.setAlignment(Qt.AlignRight)
        self.Hmean.setFont(QFont('SansSerif', 10))
        self.Hmean.setEnabled(False)
        self.Hmean.setStyleSheet("background : white;")
        self.Hmean.setParent(self)

        self.Smean = QLineEdit()
        self.Smean.move(1350, 285)
        self.Smean.resize(100, 25)
        self.Smean.setAlignment(Qt.AlignRight)
        self.Smean.setFont(QFont('SansSerif', 10))
        self.Smean.setEnabled(False)
        self.Smean.setParent(self)
        self.Smean.setStyleSheet("background : white;")

        self.Vmean = QLineEdit()
        self.Vmean.move(1480, 285)
        self.Vmean.resize(100, 25)
        self.Vmean.setAlignment(Qt.AlignRight)
        self.Vmean.setFont(QFont('SansSerif', 10))
        self.Vmean.setEnabled(False)
        self.Vmean.setParent(self)
        self.Vmean.setStyleSheet("background : white;")

        self.label15 = QLabel('<b>Std. Dev.</b>')
        self.label15.move(1120, 315)
        self.label15.setParent(self)

        self.Hsd = QLineEdit()
        self.Hsd.move(1220, 315)
        self.Hsd.resize(100, 25)
        self.Hsd.setAlignment(Qt.AlignRight)
        self.Hsd.setFont(QFont('SansSerif', 10))
        self.Hsd.setEnabled(False)
        self.Hsd.setStyleSheet("background : white;")
        self.Hsd.setParent(self)

        self.Ssd = QLineEdit()
        self.Ssd.move(1350, 315)
        self.Ssd.resize(100, 25)
        self.Ssd.setAlignment(Qt.AlignRight)
        self.Ssd.setFont(QFont('SansSerif', 10))
        self.Ssd.setEnabled(False)
        self.Ssd.setParent(self)
        self.Ssd.setStyleSheet("background : white;")

        self.Vsd = QLineEdit()
        self.Vsd.move(1480, 315)
        self.Vsd.resize(100, 25)
        self.Vsd.setAlignment(Qt.AlignRight)
        self.Vsd.setFont(QFont('SansSerif', 10))
        self.Vsd.setEnabled(False)
        self.Vsd.setParent(self)
        self.Vsd.setStyleSheet("background : white;")

        self.label17 = QLabel('<b>Skewness</b>')
        self.label17.move(1120, 345)
        self.label17.setParent(self)

        self.Hskew = QLineEdit()
        self.Hskew.move(1220, 345)
        self.Hskew.resize(100, 25)
        self.Hskew.setAlignment(Qt.AlignRight)
        self.Hskew.setFont(QFont('SansSerif', 10))
        self.Hskew.setEnabled(False)
        self.Hskew.setStyleSheet("background : white;")
        self.Hskew.setParent(self)

        self.Sskew = QLineEdit()
        self.Sskew.move(1350, 345)
        self.Sskew.resize(100, 25)
        self.Sskew.setAlignment(Qt.AlignRight)
        self.Sskew.setFont(QFont('SansSerif', 10))
        self.Sskew.setEnabled(False)
        self.Sskew.setParent(self)
        self.Sskew.setStyleSheet("background : white;")

        self.Vskew = QLineEdit()
        self.Vskew.move(1480, 345)
        self.Vskew.resize(100, 25)
        self.Vskew.setAlignment(Qt.AlignRight)
        self.Vskew.setFont(QFont('SansSerif', 10))
        self.Vskew.setEnabled(False)
        self.Vskew.setParent(self)
        self.Vskew.setStyleSheet("background : white;")

        self.label18 = QLabel('<b>Kurtosis</b>')
        self.label18.move(1120, 375)
        self.label18.setParent(self)

        self.Hkurt = QLineEdit()
        self.Hkurt.move(1220, 375)
        self.Hkurt.resize(100, 25)
        self.Hkurt.setAlignment(Qt.AlignRight)
        self.Hkurt.setFont(QFont('SansSerif', 10))
        self.Hkurt.setEnabled(False)
        self.Hkurt.setStyleSheet("background : white;")
        self.Hkurt.setParent(self)

        self.Skurt = QLineEdit()
        self.Skurt.move(1350, 375)
        self.Skurt.resize(100, 25)
        self.Skurt.setAlignment(Qt.AlignRight)
        self.Skurt.setFont(QFont('SansSerif', 10))
        self.Skurt.setEnabled(False)
        self.Skurt.setParent(self)
        self.Skurt.setStyleSheet("background : white;")

        self.Vkurt = QLineEdit()
        self.Vkurt.move(1480, 375)
        self.Vkurt.resize(100, 25)
        self.Vkurt.setAlignment(Qt.AlignRight)
        self.Vkurt.setFont(QFont('SansSerif', 10))
        self.Vkurt.setEnabled(False)
        self.Vkurt.setParent(self)
        self.Vkurt.setStyleSheet("background : white;")

        self.label57 = QLabel('<b>CIE-L*</b>')
        self.label57.move(1220, 405)
        self.label57.setParent(self)
        self.label58 = QLabel('<b>CIE-a*</b>')
        self.label58.move(1350, 405)
        self.label58.setParent(self)
        self.label59 = QLabel('<b>CIE-b*</b>')
        self.label59.move(1480, 405)
        self.label59.setParent(self)

        self.label14 = QLabel('<b>Mean</b>')
        self.label14.move(1120, 425)
        self.label14.setParent(self)
        self.label15 = QLabel('<b>Std. Dev.</b>')
        self.label15.move(1120, 455)
        self.label15.setParent(self)
        self.label17 = QLabel('<b>Skewness</b>')
        self.label17.move(1120, 485)
        self.label17.setParent(self)
        self.label18 = QLabel('<b>Kurtosis</b>')
        self.label18.move(1120, 515)
        self.label18.setParent(self)

        self.CIELmean = QLineEdit()
        self.CIELmean.move(1220, 425)
        self.CIELmean.resize(100, 25)
        self.CIELmean.setAlignment(Qt.AlignRight)
        self.CIELmean.setFont(QFont('SansSerif', 10))
        self.CIELmean.setEnabled(False)
        self.CIELmean.setParent(self)
        self.CIELmean.setStyleSheet("background : white;")

        self.CIEamean = QLineEdit()
        self.CIEamean.move(1350, 425)
        self.CIEamean.resize(100, 25)
        self.CIEamean.setAlignment(Qt.AlignRight)
        self.CIEamean.setFont(QFont('SansSerif', 10))
        self.CIEamean.setEnabled(False)
        self.CIEamean.setParent(self)
        self.CIEamean.setStyleSheet("background : white;")

        self.CIEbmean = QLineEdit()
        self.CIEbmean.move(1480, 425)
        self.CIEbmean.resize(100, 25)
        self.CIEbmean.setAlignment(Qt.AlignRight)
        self.CIEbmean.setFont(QFont('SansSerif', 10))
        self.CIEbmean.setEnabled(False)
        self.CIEbmean.setParent(self)
        self.CIEbmean.setStyleSheet("background : white;")

        self.CIELsd = QLineEdit()
        self.CIELsd.move(1220, 455)
        self.CIELsd.resize(100, 25)
        self.CIELsd.setAlignment(Qt.AlignRight)
        self.CIELsd.setFont(QFont('SansSerif', 10))
        self.CIELsd.setEnabled(False)
        self.CIELsd.setParent(self)
        self.CIELsd.setStyleSheet("background : white;")

        self.CIEasd = QLineEdit()
        self.CIEasd.move(1350, 455)
        self.CIEasd.resize(100, 25)
        self.CIEasd.setAlignment(Qt.AlignRight)
        self.CIEasd.setFont(QFont('SansSerif', 10))
        self.CIEasd.setEnabled(False)
        self.CIEasd.setParent(self)
        self.CIEasd.setStyleSheet("background : white;")

        self.CIEbsd = QLineEdit()
        self.CIEbsd.move(1480, 455)
        self.CIEbsd.resize(100, 25)
        self.CIEbsd.setAlignment(Qt.AlignRight)
        self.CIEbsd.setFont(QFont('SansSerif', 10))
        self.CIEbsd.setEnabled(False)
        self.CIEbsd.setParent(self)
        self.CIEbsd.setStyleSheet("background : white;")

        self.CIELskew = QLineEdit()
        self.CIELskew.move(1220, 485)
        self.CIELskew.resize(100, 25)
        self.CIELskew.setAlignment(Qt.AlignRight)
        self.CIELskew.setFont(QFont('SansSerif', 10))
        self.CIELskew.setEnabled(False)
        self.CIELskew.setParent(self)
        self.CIELskew.setStyleSheet("background : white;")

        self.CIEaskew = QLineEdit()
        self.CIEaskew.move(1350, 485)
        self.CIEaskew.resize(100, 25)
        self.CIEaskew.setAlignment(Qt.AlignRight)
        self.CIEaskew.setFont(QFont('SansSerif', 10))
        self.CIEaskew.setEnabled(False)
        self.CIEaskew.setParent(self)
        self.CIEaskew.setStyleSheet("background : white;")

        self.CIEbskew = QLineEdit()
        self.CIEbskew.move(1480, 485)
        self.CIEbskew.resize(100, 25)
        self.CIEbskew.setAlignment(Qt.AlignRight)
        self.CIEbskew.setFont(QFont('SansSerif', 10))
        self.CIEbskew.setEnabled(False)
        self.CIEbskew.setParent(self)
        self.CIEbskew.setStyleSheet("background : white;")

        self.CIELkurt = QLineEdit()
        self.CIELkurt.move(1220, 515)
        self.CIELkurt.resize(100, 25)
        self.CIELkurt.setAlignment(Qt.AlignRight)
        self.CIELkurt.setFont(QFont('SansSerif', 10))
        self.CIELkurt.setEnabled(False)
        self.CIELkurt.setParent(self)
        self.CIELkurt.setStyleSheet("background : white;")

        self.CIEakurt = QLineEdit()
        self.CIEakurt.move(1350, 515)
        self.CIEakurt.resize(100, 25)
        self.CIEakurt.setAlignment(Qt.AlignRight)
        self.CIEakurt.setFont(QFont('SansSerif', 10))
        self.CIEakurt.setEnabled(False)
        self.CIEakurt.setParent(self)
        self.CIEakurt.setStyleSheet("background : white;")

        self.CIEbkurt = QLineEdit()
        self.CIEbkurt.move(1480, 515)
        self.CIEbkurt.resize(100, 25)
        self.CIEbkurt.setAlignment(Qt.AlignRight)
        self.CIEbkurt.setFont(QFont('SansSerif', 10))
        self.CIEbkurt.setEnabled(False)
        self.CIEbkurt.setParent(self)
        self.CIEbkurt.setStyleSheet("background : white;")


        # ========= TEXTURE FEATURES ===============================================

        self.label47 = QLabel('<b>0</b>')
        self.label47.move(795, 635)
        self.label47.setParent(self)
        self.label48 = QLabel('<b>45</b>')
        self.label48.move(870, 635)
        self.label48.setParent(self)
        self.label49 = QLabel('<b>90</b>')
        self.label49.move(945, 635)
        self.label49.setParent(self)
        self.label50 = QLabel('<b>135</b>')
        self.label50.move(1020, 635)
        self.label50.setParent(self)

        self.label42 = QLabel('<b>Contrast</b>')
        self.label42.move(680, 655)
        self.label42.setParent(self)

        self.contrast0 = QLineEdit()
        self.contrast0.move(775, 655)
        self.contrast0.resize(70, 25)
        self.contrast0.setAlignment(Qt.AlignRight)
        self.contrast0.setFont(QFont('SansSerif', 10))
        self.contrast0.setEnabled(False)
        self.contrast0.setParent(self)
        self.contrast0.setStyleSheet("background : white;")

        self.contrast45 = QLineEdit()
        self.contrast45.move(850, 655)
        self.contrast45.resize(70, 25)
        self.contrast45.setAlignment(Qt.AlignRight)
        self.contrast45.setFont(QFont('SansSerif', 10))
        self.contrast45.setEnabled(False)
        self.contrast45.setParent(self)
        self.contrast45.setStyleSheet("background : white;")

        self.contrast90 = QLineEdit()
        self.contrast90.move(925, 655)
        self.contrast90.resize(70, 25)
        self.contrast90.setAlignment(Qt.AlignRight)
        self.contrast90.setFont(QFont('SansSerif', 10))
        self.contrast90.setEnabled(False)
        self.contrast90.setParent(self)
        self.contrast90.setStyleSheet("background : white;")

        self.contrast135 = QLineEdit()
        self.contrast135.move(1000, 655)
        self.contrast135.resize(70, 25)
        self.contrast135.setAlignment(Qt.AlignRight)
        self.contrast135.setFont(QFont('SansSerif', 10))
        self.contrast135.setEnabled(False)
        self.contrast135.setParent(self)
        self.contrast135.setStyleSheet("background : white;")

        self.label43 = QLabel('<b>Dissimilarity</b>')
        self.label43.move(680, 685)
        self.label43.setParent(self)

        self.dissimilarity0 = QLineEdit()
        self.dissimilarity0.move(775, 685)
        self.dissimilarity0.resize(70, 25)
        self.dissimilarity0.setAlignment(Qt.AlignRight)
        self.dissimilarity0.setFont(QFont('SansSerif', 10))
        self.dissimilarity0.setEnabled(False)
        self.dissimilarity0.setParent(self)
        self.dissimilarity0.setStyleSheet("background : white;")

        self.dissimilarity45 = QLineEdit()
        self.dissimilarity45.move(850, 685)
        self.dissimilarity45.resize(70, 25)
        self.dissimilarity45.setAlignment(Qt.AlignRight)
        self.dissimilarity45.setFont(QFont('SansSerif', 10))
        self.dissimilarity45.setEnabled(False)
        self.dissimilarity45.setParent(self)
        self.dissimilarity45.setStyleSheet("background : white;")

        self.dissimilarity90 = QLineEdit()
        self.dissimilarity90.move(925, 685)
        self.dissimilarity90.resize(70, 25)
        self.dissimilarity90.setAlignment(Qt.AlignRight)
        self.dissimilarity90.setFont(QFont('SansSerif', 10))
        self.dissimilarity90.setEnabled(False)
        self.dissimilarity90.setParent(self)
        self.dissimilarity90.setStyleSheet("background : white;")

        self.dissimilarity135 = QLineEdit()
        self.dissimilarity135.move(1000, 685)
        self.dissimilarity135.resize(70, 25)
        self.dissimilarity135.setAlignment(Qt.AlignRight)
        self.dissimilarity135.setFont(QFont('SansSerif', 10))
        self.dissimilarity135.setEnabled(False)
        self.dissimilarity135.setParent(self)
        self.dissimilarity135.setStyleSheet("background : white;")

        self.label44 = QLabel('<b>Homogeneity</b>')
        self.label44.move(680, 715)
        self.label44.setParent(self)

        self.homogeneity0 = QLineEdit()
        self.homogeneity0.move(775, 715)
        self.homogeneity0.resize(70, 25)
        self.homogeneity0.setAlignment(Qt.AlignRight)
        self.homogeneity0.setFont(QFont('SansSerif', 10))
        self.homogeneity0.setEnabled(False)
        self.homogeneity0.setParent(self)
        self.homogeneity0.setStyleSheet("background : white;")

        self.homogeneity45 = QLineEdit()
        self.homogeneity45.move(850, 715)
        self.homogeneity45.resize(70, 25)
        self.homogeneity45.setAlignment(Qt.AlignRight)
        self.homogeneity45.setFont(QFont('SansSerif', 10))
        self.homogeneity45.setEnabled(False)
        self.homogeneity45.setParent(self)
        self.homogeneity45.setStyleSheet("background : white;")

        self.homogeneity90 = QLineEdit()
        self.homogeneity90.move(925, 715)
        self.homogeneity90.resize(70, 25)
        self.homogeneity90.setAlignment(Qt.AlignRight)
        self.homogeneity90.setFont(QFont('SansSerif', 10))
        self.homogeneity90.setEnabled(False)
        self.homogeneity90.setParent(self)
        self.homogeneity90.setStyleSheet("background : white;")

        self.homogeneity135 = QLineEdit()
        self.homogeneity135.move(1000, 715)
        self.homogeneity135.resize(70, 25)
        self.homogeneity135.setAlignment(Qt.AlignRight)
        self.homogeneity135.setFont(QFont('SansSerif', 10))
        self.homogeneity135.setEnabled(False)
        self.homogeneity135.setParent(self)
        self.homogeneity135.setStyleSheet("background : white;")

        self.label45 = QLabel('<b>ASM</b>')
        self.label45.move(680, 745)
        self.label45.setParent(self)

        self.asm0 = QLineEdit()
        self.asm0.move(775, 745)
        self.asm0.resize(70, 25)
        self.asm0.setAlignment(Qt.AlignRight)
        self.asm0.setFont(QFont('SansSerif', 10))
        self.asm0.setEnabled(False)
        self.asm0.setParent(self)
        self.asm0.setStyleSheet("background : white;")

        self.asm45 = QLineEdit()
        self.asm45.move(850, 745)
        self.asm45.resize(70, 25)
        self.asm45.setAlignment(Qt.AlignRight)
        self.asm45.setFont(QFont('SansSerif', 10))
        self.asm45.setEnabled(False)
        self.asm45.setParent(self)
        self.asm45.setStyleSheet("background : white;")

        self.asm90 = QLineEdit()
        self.asm90.move(925, 745)
        self.asm90.resize(70, 25)
        self.asm90.setAlignment(Qt.AlignRight)
        self.asm90.setFont(QFont('SansSerif', 10))
        self.asm90.setEnabled(False)
        self.asm90.setParent(self)
        self.asm90.setStyleSheet("background : white;")

        self.asm135 = QLineEdit()
        self.asm135.move(1000, 745)
        self.asm135.resize(70, 25)
        self.asm135.setAlignment(Qt.AlignRight)
        self.asm135.setFont(QFont('SansSerif', 10))
        self.asm135.setEnabled(False)
        self.asm135.setParent(self)
        self.asm135.setStyleSheet("background : white;")

        self.label46 = QLabel('<b>Energy</b>')
        self.label46.move(680, 775)
        self.label46.setParent(self)

        self.energy0 = QLineEdit()
        self.energy0.move(775, 775)
        self.energy0.resize(70, 25)
        self.energy0.setAlignment(Qt.AlignRight)
        self.energy0.setFont(QFont('SansSerif', 10))
        self.energy0.setEnabled(False)
        self.energy0.setParent(self)
        self.energy0.setStyleSheet("background : white;")

        self.energy45 = QLineEdit()
        self.energy45.move(850, 775)
        self.energy45.resize(70, 25)
        self.energy45.setAlignment(Qt.AlignRight)
        self.energy45.setFont(QFont('SansSerif', 10))
        self.energy45.setEnabled(False)
        self.energy45.setParent(self)
        self.energy45.setStyleSheet("background : white;")

        self.energy90 = QLineEdit()
        self.energy90.move(925, 775)
        self.energy90.resize(70, 25)
        self.energy90.setAlignment(Qt.AlignRight)
        self.energy90.setFont(QFont('SansSerif', 10))
        self.energy90.setEnabled(False)
        self.energy90.setParent(self)
        self.energy90.setStyleSheet("background : white;")

        self.energy135 = QLineEdit()
        self.energy135.move(1000, 775)
        self.energy135.resize(70, 25)
        self.energy135.setAlignment(Qt.AlignRight)
        self.energy135.setFont(QFont('SansSerif', 10))
        self.energy135.setEnabled(False)
        self.energy135.setParent(self)
        self.energy135.setStyleSheet("background : white;")

        self.label46 = QLabel('<b>Correlation</b>')
        self.label46.move(680, 805)
        self.label46.setParent(self)

        self.correlation0 = QLineEdit()
        self.correlation0.move(775, 805)
        self.correlation0.resize(70, 25)
        self.correlation0.setAlignment(Qt.AlignRight)
        self.correlation0.setFont(QFont('SansSerif', 10))
        self.correlation0.setEnabled(False)
        self.correlation0.setParent(self)
        self.correlation0.setStyleSheet("background : white;")

        self.correlation45 = QLineEdit()
        self.correlation45.move(850, 805)
        self.correlation45.resize(70, 25)
        self.correlation45.setAlignment(Qt.AlignRight)
        self.correlation45.setFont(QFont('SansSerif', 10))
        self.correlation45.setEnabled(False)
        self.correlation45.setParent(self)
        self.correlation45.setStyleSheet("background : white;")

        self.correlation90 = QLineEdit()
        self.correlation90.move(925, 805)
        self.correlation90.resize(70, 25)
        self.correlation90.setAlignment(Qt.AlignRight)
        self.correlation90.setFont(QFont('SansSerif', 10))
        self.correlation90.setEnabled(False)
        self.correlation90.setParent(self)
        self.correlation90.setStyleSheet("background : white;")

        self.correlation135 = QLineEdit()
        self.correlation135.move(1000, 805)
        self.correlation135.resize(70, 25)
        self.correlation135.setAlignment(Qt.AlignRight)
        self.correlation135.setFont(QFont('SansSerif', 10))
        self.correlation135.setEnabled(False)
        self.correlation135.setParent(self)
        self.correlation135.setStyleSheet("background : white;")

        self.label20 = QLabel('<b>Area</b>')
        self.label20.move(1120, 595)
        self.label20.setParent(self)

        self.area_ = QLineEdit()
        self.area_.move(1220, 595)
        self.area_.resize(100, 25)
        self.area_.setAlignment(Qt.AlignRight)
        self.area_.setFont(QFont('SansSerif', 10))
        self.area_.setEnabled(False)
        self.area_.setStyleSheet("background : white;")
        self.area_.setParent(self)

        self.label21 = QLabel('<b>Perimeter</b>')
        self.label21.move(1120, 625)
        self.label21.setParent(self)

        self.perimeter_ = QLineEdit()
        self.perimeter_.move(1220, 625)
        self.perimeter_.resize(100, 25)
        self.perimeter_.setAlignment(Qt.AlignRight)
        self.perimeter_.setFont(QFont('SansSerif', 10))
        self.perimeter_.setEnabled(False)
        self.perimeter_.setStyleSheet("background : white;")
        self.perimeter_.setParent(self)

        self.label22 = QLabel('<b>Roundness</b>')
        self.label22.move(1120, 655)
        self.label22.setParent(self)

        self.roundness_ = QLineEdit()
        self.roundness_.move(1220, 655)
        self.roundness_.resize(100, 25)
        self.roundness_.setAlignment(Qt.AlignRight)
        self.roundness_.setFont(QFont('SansSerif', 10))
        self.roundness_.setEnabled(False)
        self.roundness_.setStyleSheet("background : white;")
        self.roundness_.setParent(self)

        self.label23 = QLabel('<b>Complexity</b>')
        self.label23.move(1120, 715)
        self.label23.setParent(self)

        self.complexity_ = QLineEdit()
        self.complexity_.move(1220, 715)
        self.complexity_.resize(100, 25)
        self.complexity_.setAlignment(Qt.AlignRight)
        self.complexity_.setFont(QFont('SansSerif', 10))
        self.complexity_.setEnabled(False)
        self.complexity_.setStyleSheet("background : white;")
        self.complexity_.setParent(self)

        self.label24 = QLabel('<b>Aspect Ratio</b>')
        self.label24.move(1120, 745)
        self.label24.setParent(self)

        self.aspectRatio_ = QLineEdit()
        self.aspectRatio_.move(1220, 745)
        self.aspectRatio_.resize(100, 25)
        self.aspectRatio_.setAlignment(Qt.AlignRight)
        self.aspectRatio_.setFont(QFont('SansSerif', 10))
        self.aspectRatio_.setEnabled(False)
        self.aspectRatio_.setStyleSheet("background : white;")
        self.aspectRatio_.setParent(self)

        self.label25 = QLabel('<b>Extent</b>')
        self.label25.move(1120, 775)
        self.label25.setParent(self)

        self.extent_ = QLineEdit()
        self.extent_.move(1220, 775)
        self.extent_.resize(100, 25)
        self.extent_.setAlignment(Qt.AlignRight)
        self.extent_.setFont(QFont('SansSerif', 10))
        self.extent_.setEnabled(False)
        self.extent_.setStyleSheet("background : white;")
        self.extent_.setParent(self)

        self.label26 = QLabel('<b>Solidity</b>')
        self.label26.move(1120, 805)
        self.label26.setParent(self)

        self.solidity_ = QLineEdit()
        self.solidity_.move(1220, 805)
        self.solidity_.resize(100, 25)
        self.solidity_.setAlignment(Qt.AlignRight)
        self.solidity_.setFont(QFont('SansSerif', 10))
        self.solidity_.setEnabled(False)
        self.solidity_.setStyleSheet("background : white;")
        self.solidity_.setParent(self)

        self.label27 = QLabel('<b>Minor Axis Length</b>')
        self.label27.move(1350, 595)
        self.label27.setParent(self)

        self.minorAxis_ = QLineEdit()
        self.minorAxis_.move(1480, 595)
        self.minorAxis_.resize(100, 25)
        self.minorAxis_.setAlignment(Qt.AlignRight)
        self.minorAxis_.setFont(QFont('SansSerif', 10))
        self.minorAxis_.setEnabled(False)
        self.minorAxis_.setStyleSheet("background : white;")
        self.minorAxis_.setParent(self)

        self.label28 = QLabel('<b>Major Axis Length</b>')
        self.label28.move(1350, 625)
        self.label28.setParent(self)

        self.majorAxis_ = QLineEdit()
        self.majorAxis_.move(1480, 625)
        self.majorAxis_.resize(100, 25)
        self.majorAxis_.setAlignment(Qt.AlignRight)
        self.majorAxis_.setFont(QFont('SansSerif', 10))
        self.majorAxis_.setEnabled(False)
        self.majorAxis_.setStyleSheet("background : white;")
        self.majorAxis_.setParent(self)

        self.label29 = QLabel('<b>Compactness</b>')
        self.label29.move(1350, 655)
        self.label29.setParent(self)

        self.compactness_ = QLineEdit()
        self.compactness_.move(1480, 655)
        self.compactness_.resize(100, 25)
        self.compactness_.setAlignment(Qt.AlignRight)
        self.compactness_.setFont(QFont('SansSerif', 10))
        self.compactness_.setEnabled(False)
        self.compactness_.setStyleSheet("background : white;")
        self.compactness_.setParent(self)

        self.label30 = QLabel('<b>Convex Area</b>')
        self.label30.move(1350, 685)
        self.label30.setParent(self)

        self.ConvexArea_ = QLineEdit()
        self.ConvexArea_.move(1480, 685)
        self.ConvexArea_.resize(100, 25)
        self.ConvexArea_.setAlignment(Qt.AlignRight)
        self.ConvexArea_.setFont(QFont('SansSerif', 10))
        self.ConvexArea_.setEnabled(False)
        self.ConvexArea_.setStyleSheet("background : white;")
        self.ConvexArea_.setParent(self)

        self.label31 = QLabel('<b>Equiv. Diameter</b>')
        self.label31.move(1120, 685)
        self.label31.setParent(self)

        self.EquivDia_ = QLineEdit()
        self.EquivDia_.move(1220, 685)
        self.EquivDia_.resize(100, 25)
        self.EquivDia_.setAlignment(Qt.AlignRight)
        self.EquivDia_.setFont(QFont('SansSerif', 10))
        self.EquivDia_.setEnabled(False)
        self.EquivDia_.setStyleSheet("background : white;")
        self.EquivDia_.setParent(self)

        self.label53 = QLabel('<b>Shape Factor 1</b>')
        self.label53.move(1350, 715)
        self.label53.setParent(self)

        self.SF1_ = QLineEdit()
        self.SF1_.move(1480, 715)
        self.SF1_.resize(100, 25)
        self.SF1_.setAlignment(Qt.AlignRight)
        self.SF1_.setFont(QFont('SansSerif', 10))
        self.SF1_.setEnabled(False)
        self.SF1_.setStyleSheet("background : white;")
        self.SF1_.setParent(self)

        self.label54 = QLabel('<b>Shape Factor 2</b>')
        self.label54.move(1350, 745)
        self.label54.setParent(self)

        self.SF2_ = QLineEdit()
        self.SF2_.move(1480, 745)
        self.SF2_.resize(100, 25)
        self.SF2_.setAlignment(Qt.AlignRight)
        self.SF2_.setFont(QFont('SansSerif', 10))
        self.SF2_.setEnabled(False)
        self.SF2_.setStyleSheet("background : white;")
        self.SF2_.setParent(self)

        self.label55 = QLabel('<b>Shape Factor 3</b>')
        self.label55.move(1350, 775)
        self.label55.setParent(self)

        self.SF3_ = QLineEdit()
        self.SF3_.move(1480, 775)
        self.SF3_.resize(100, 25)
        self.SF3_.setAlignment(Qt.AlignRight)
        self.SF3_.setFont(QFont('SansSerif', 10))
        self.SF3_.setEnabled(False)
        self.SF3_.setStyleSheet("background : white;")
        self.SF3_.setParent(self)

        self.label56 = QLabel('<b>Shape Factor 4</b>')
        self.label56.move(1350, 805)
        self.label56.setParent(self)

        self.SF4_ = QLineEdit()
        self.SF4_.move(1480, 805)
        self.SF4_.resize(100, 25)
        self.SF4_.setAlignment(Qt.AlignRight)
        self.SF4_.setFont(QFont('SansSerif', 10))
        self.SF4_.setEnabled(False)
        self.SF4_.setStyleSheet("background : white;")
        self.SF4_.setParent(self)

        # ========== CLASS ====================================
        self.label51 = QLabel('<b>ID</b>')
        self.label51.move(350, 635)
        self.label51.setParent(self)

        self.id_ = QLineEdit()
        self.id_.move(380, 630)
        self.id_.resize(80, 30)
        self.id_.setAlignment(Qt.AlignCenter)
        self.id_.setFont(QFont('SansSerif', 10))
        self.id_.setToolTip("Input ID Sample")
        self.id_.setEnabled(True)
        self.id_.setStyleSheet("background : white;")
        self.id_.setParent(self)

        self.label33 = QLabel('<b>Class</b>')
        self.label33.move(480, 635)
        self.label33.setParent(self)

        self.class_ = QLineEdit()
        self.class_.move(520, 630)
        self.class_.resize(80, 30)
        self.class_.setAlignment(Qt.AlignCenter)
        self.class_.setFont(QFont('SansSerif', 10))
        self.class_.setToolTip("Input Class (for Supervised Learning)")
        self.class_.setEnabled(True)
        self.class_.setStyleSheet("background : white;")
        self.class_.setParent(self)

        input = QIcon('09-gui-icon/check.png')
        self.inputDB = QPushButton('\tSAVE')
        self.inputDB.setIcon(input)
        self.inputDB.move(1380, 855)
        self.inputDB.resize(100, 30)
        self.inputDB.setParent(self)
        self.inputDB.clicked.connect(self.inputDBClick)


        self.labelResult = QLabel()
        self.labelResult.move(1300,780)
        self.labelResult.resize(200,30)
        self.labelResult.setParent(self)

        self.resetButton = QPushButton('\tRESET ALL')
        resetIcon = QIcon('09-gui-icon/reset.png')
        self.resetButton.setToolTip("Reset all process")
        self.resetButton.setIcon(resetIcon)
        self.resetButton.move(1280, 855)
        self.resetButton.resize(100, 30)
        self.resetButton.setEnabled(True)
        #self.resetButton.setStyleSheet("font-weight:bold;")
        self.resetButton.setParent(self)
        self.resetButton.clicked.connect(self.resetButtonClick)

        self.Hline2 = QFrame()
        self.Hline2.setFrameShape(QFrame.HLine)
        self.Hline2.setFrameShadow(QFrame.Sunken)
        self.Hline2.move(25, 835)
        self.Hline2.resize(1550, 20)
        self.Hline2.setParent(self)

        self.show()
    def inputDBClick(self):
        try:
            mydb = mc.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "cvs"
            )
            mycursor = mydb.cursor()

            id = self.id_.text()
            mean_r = self.rmean.text()
            mean_g = self.gmean.text()
            mean_b = self.bmean.text()
            sd_r = self.rsd.text()
            sd_g = self.gsd.text()
            sd_b = self.bsd.text()
            skew_r = self.rskew.text()
            skew_g = self.gskew.text()
            skew_b = self.bskew.text()
            kurt_r = self.rkurt.text()
            kurt_g = self.gkurt.text()
            kurt_b = self.bkurt.text()
            mean_h = self.Hmean.text()
            mean_s = self.Smean.text()
            mean_v = self.Vmean.text()
            sd_h = self.Hsd.text()
            sd_s = self.Ssd.text()
            sd_v = self.Vsd.text()
            skew_h = self.Hskew.text()
            skew_s = self.Sskew.text()
            skew_v = self.Vskew.text()
            kurt_h = self.Hkurt.text()
            kurt_s = self.Skurt.text()
            kurt_v = self.Vkurt.text()
            mean_CIEL = self.CIELmean.text()
            mean_CIEa = self.CIEamean.text()
            mean_CIEb = self.CIEbmean.text()
            sd_CIEL = self.CIELsd.text()
            sd_CIEa = self.CIEasd.text()
            sd_CIEb = self.CIEbsd.text()
            skew_CIEL = self.CIELskew.text()
            skew_CIEa = self.CIEaskew.text()
            skew_CIEb = self.CIEbskew.text()
            kurt_CIEL = self.CIELkurt.text()
            kurt_CIEa = self.CIEakurt.text()
            kurt_CIEb = self.CIEbkurt.text()

            contrast_0 = self.contrast0.text()
            contrast_45= self.contrast45.text()
            contrast_90= self.contrast90.text()
            contrast_135= self.contrast135.text()
            dissimilarity_0 = self.dissimilarity0.text()
            dissimilarity_45 = self.dissimilarity45.text()
            dissimilarity_90 = self.dissimilarity90.text()
            dissimilarity_135 = self.dissimilarity135.text()
            homogeneity_0 = self.homogeneity0.text()
            homogeneity_45 = self.homogeneity45.text()
            homogeneity_90 = self.homogeneity90.text()
            homogeneity_135 = self.homogeneity135.text()
            asm_0= self.asm0.text()
            asm_45 = self.asm45.text()
            asm_90 = self.asm90.text()
            asm_135 = self.asm135.text()
            energy_0 = self.energy0.text()
            energy_45 = self.energy45.text()
            energy_90 = self.energy90.text()
            energy_135 = self.energy135.text()
            correlation_0 = self.correlation0.text()
            correlation_45 = self.correlation45.text()
            correlation_90 = self.correlation90.text()
            correlation_135 = self.correlation135.text()
            area = self.area_.text()
            perimeter = self.perimeter_.text()
            roundness = self.roundness_.text()
            equiv_diameter = self.EquivDia_.text()
            complexity = self.complexity_.text()
            aspect_ratio = self.aspectRatio_.text()
            extent = self.extent_.text()
            solidity = self.solidity_.text()
            minor_axis = self.minorAxis_.text()
            major_axis = self.majorAxis_.text()
            compactness = self.compactness_.text()
            convex_area = self.ConvexArea_.text()
            SF1 = self.SF1_.text()
            SF2 = self.SF2_.text()
            SF3 = self.SF3_.text()
            SF4 = self.SF4_.text()
            class_ = self.class_.text()
            basename = 1
            sql = "INSERT INTO features (basename, r_mean, mean_g, mean_b, sd_r, sd_g, sd_b, var_r, var_g, var_b, skew_r, skew_g, skew_b, kurt_r, kurt_g, kurt_b," \
                  "mean_h, mean_s, mean_v, sd_h, sd_s, sd_v, skew_h, skew_s, skew_v, kurt_h, kurt_s, kurt_v," \
                  "mean_CIEL, mean_CIEa, mean_CIEb, sd_CIEL, sd_CIEa, sd_CIEb, skew_CIEL, skew_CIEa, skew_CIEb, kurt_CIEL, kurt_CIEa, kurt_CIEb," \
                  "contrast_0, contrast_45, contrast_90, contrast_135, dissimilarity_0, dissimilarity_45, dissimilarity_90, dissimilarity_135," \
                  "homogeneity_0, homogeneity_45, homogeneity_90, homogeneity_135, asm_0, asm_45, asm_90, asm_135, energy_0, energy_45, energy_90, energy_135," \
                  "correlation_0, correlation_45, correlation_90, correlation_135, " \
                  "area, perimeter, roundness, equiv_dia, complexity, aspect_ratio, extent, solidity," \
                  "minor_axis, major_axis, compactness, convex_area, SF1, SF2, SF3, SF4, class_) VALUES (" \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                  " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, " \
                  " %s, %s, %s, %s, %s, %s, %s, %s," \
                  " %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (id, mean_r, mean_g, mean_b, sd_r, sd_g, sd_b, skew_r, skew_g, skew_b, kurt_r, kurt_g, kurt_b,        #13
                   mean_h, mean_s, mean_v, sd_h, sd_s, sd_v, skew_h, skew_s, skew_v, kurt_h, kurt_s, kurt_v,            #12
                   mean_CIEL, mean_CIEa, mean_CIEb, sd_CIEL, sd_CIEa, sd_CIEb, skew_CIEL, skew_CIEa, skew_CIEb, kurt_CIEL, kurt_CIEa, kurt_CIEb,    #12
                   contrast_0, contrast_45, contrast_90, contrast_135,              #4
                   dissimilarity_0, dissimilarity_45, dissimilarity_90, dissimilarity_135,          #4
                   homogeneity_0, homogeneity_45, homogeneity_90, homogeneity_135,          #4
                   asm_0, asm_45, asm_90, asm_135,          #4
                   energy_0, energy_45, energy_90, energy_135,      #4
                   correlation_0, correlation_45, correlation_90, correlation_135,      #4
                   area, perimeter, roundness, equiv_diameter, complexity, aspect_ratio, extent, solidity,      #8
                   minor_axis, major_axis, compactness, convex_area, SF1, SF2, SF3, SF4, class_)        #9
            mycursor.execute(sql, val)
            mydb.commit()
            self.labelResult.setText("Data Inserted")
        except mc.Error as e:
            self.labelResult.setText("Error Inserting")

    def connectDBButtonClick(self):
        try:
            condb = mc.connect(host='localhost', user='root', passwd='', port=3306, autocommit=True)
            QMessageBox.about(self, 'Connection', 'Database Connection Successfully')
        except mc.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed to Connect Database')
            sys.exit(1)
    def roiButtonClick(self):
        fname = QFileDialog.getOpenFileName()[0]
        # Load the image and get its filename without path and dimensions.
        filename = fname
        basename = os.path.basename(filename)
        image = cv2.imread(filename)
        h, w = image.shape[:2]

        # The coordinates defining the square selected will be kept in this list.
        select_coords = []
        selecting = False
        # While we are in the process of selecting a region, this flag is True.
        def get_square_coords(x, y, cx, cy):
            """
            Get the diagonally-opposite coordinates of the square.
            (cx, cy) are the coordinates of the square centre.
            (x, y) is a selected point to which the largest square is to be matched.
            """
            # Selected square edge half-length; don't stray outside the image boundary.
            a = max(abs(cx - x), abs(cy - y))
            a = min(a, w - cx, cx, h - cy, cy)
            return cx - a, cy - a, cx + a, cy + a
        def region_selection(event, x, y, flags, param):
            """Callback function to handle mouse events related to region selection."""
            global image, selecting, select_coords
            if event == cv2.EVENT_LBUTTONDOWN:
                # Left mouse button down: begin the selection.
                # The first coordinate pair is the centre of the square.
                select_coords = [(x, y)]
                selecting = True
            elif event == cv2.EVENT_MOUSEMOVE and selecting:
                # If we're dragging the selection square, update it.
                image = clone.copy()
                x0, y0, x1, y1 = get_square_coords(x, y, *select_coords[0])
                cv2.rectangle(image, (x0, y0), (x1, y1), (0, 255, 0), 2)
            elif event == cv2.EVENT_LBUTTONUP:
                # Left mouse button up: the selection has been made.
                select_coords.append((x, y))
                selecting = False
        # The cropped image will be saved with this filename.
        cropped_filename = os.path.splitext(filename)[0] + '_sq.png'
        cropped_basename = os.path.basename(cropped_filename)
        # Store a clone of the original image (without selected region annotation).
        clone = image.copy()
        # Name the main image window after the image filename.
        cv2.namedWindow(basename)
        cv2.setMouseCallback(basename, region_selection)
        # Keep looping and listening for user input until 'c' is pressed.
        while True:
            # Display the image and wait for a keypress
            cv2.imshow(basename, image)
            key = cv2.waitKey(1) & 0xFF
            # If 'c' is pressed, break from the loop and handle any region selection.
            if key == ord("c"):
                break
        # Did we make a selection?
        if len(select_coords) == 2:
            cx, cy = select_coords[0]
            x, y = select_coords[1]
            x0, y0, x1, y1 = get_square_coords(x, y, cx, cy)
            # Crop the image to the selected region and display in a new window.
            cropped_image = clone[y0:y1, x0:x1]
            cv2.imshow(cropped_basename, cropped_image)
            cv2.imwrite(cropped_filename, cropped_image)
            # Wait until any key press.
            cv2.waitKey(0)
        # We're done: close all open windows before exiting.
        cv2.destroyAllWindows()

    def textureFtrButtonClick(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        angle1 = 0; angle2 = np.pi/4; angle3 = np.pi/2; angle4 = 3 * np.pi / 4;

        graycom1 = greycomatrix(gray, [1], [angle1], levels=256)
        contrast0 = greycoprops(graycom1, 'contrast')
        self.contrast0.setText("%.5f" % contrast0)
        dissimilarity0 = greycoprops(graycom1, 'dissimilarity')
        self.dissimilarity0.setText("%.5f" % dissimilarity0)
        homogeneity0 = greycoprops(graycom1, 'homogeneity')
        self.homogeneity0.setText("%.5f" % homogeneity0)
        asm0 = greycoprops(graycom1, 'ASM')
        self.asm0.setText("%.5f" % asm0)
        energy0 = greycoprops(graycom1, 'energy')
        self.energy0.setText("%.5f" % energy0)
        correlation0 = greycoprops(graycom1, 'correlation')
        self.correlation0.setText("%.5f" % correlation0)

        graycom2 = greycomatrix(gray, [1], [angle2], levels=256)
        contrast45 = greycoprops(graycom2, 'contrast')
        self.contrast45.setText("%.5f" % contrast45)
        dissimilarity45 = greycoprops(graycom2, 'dissimilarity')
        self.dissimilarity45.setText("%.5f" % dissimilarity45)
        homogeneity45 = greycoprops(graycom2, 'homogeneity')
        self.homogeneity45.setText("%.5f" % homogeneity45)
        asm45 = greycoprops(graycom2, 'ASM')
        self.asm45.setText("%.5f" % asm45)
        energy45 = greycoprops(graycom2, 'energy')
        self.energy45.setText("%.5f" % energy45)
        correlation45 = greycoprops(graycom2, 'correlation')
        self.correlation45.setText("%.5f" % correlation45)

        graycom3 = greycomatrix(gray, [1], [angle3], levels=256)
        contrast90 = greycoprops(graycom3, 'contrast')
        self.contrast90.setText("%.5f" % contrast90)
        dissimilarity90 = greycoprops(graycom3, 'dissimilarity')
        self.dissimilarity90.setText("%.5f" % dissimilarity90)
        homogeneity90 = greycoprops(graycom3, 'homogeneity')
        self.homogeneity90.setText("%.5f" % homogeneity90)
        asm90 = greycoprops(graycom3, 'ASM')
        self.asm90.setText("%.5f" % asm90)
        energy90 = greycoprops(graycom3, 'energy')
        self.energy90.setText("%.5f" % energy90)
        correlation90 = greycoprops(graycom3, 'correlation')
        self.correlation90.setText("%.5f" % correlation90)

        graycom4 = greycomatrix(gray, [1], [angle4], levels=256)
        contrast135 = greycoprops(graycom4, 'contrast')
        self.contrast135.setText("%.5f" % contrast135)
        dissimilarity135 = greycoprops(graycom4, 'dissimilarity')
        self.dissimilarity135.setText("%.5f" % dissimilarity135)
        homogeneity135 = greycoprops(graycom4, 'homogeneity')
        self.homogeneity135.setText("%.5f" % homogeneity135)
        asm135 = greycoprops(graycom4, 'ASM')
        self.asm135.setText("%.5f" % asm135)
        energy135 = greycoprops(graycom4, 'energy')
        self.energy135.setText("%.5f" % energy135)
        correlation135 = greycoprops(graycom4, 'correlation')
        self.correlation135.setText("%.5f" % correlation135)

    def colorFtrButtonClick(self):
        b, g, r = cv2.split(self.image)
        N = r.shape[0] * r.shape[1]
        # Mean
        r_mean = np.mean(r[0:250]); g_mean = np.mean(g[0:250]); b_mean = np.mean(b[0:250])
        self.rmean.setText(str("%.5f" % r_mean))
        self.gmean.setText(str("%.5f" % g_mean))
        self.bmean.setText(str("%.5f" % b_mean))

        r_sd = np.std(r); g_sd = np.std(g); b_sd = np.std(b)
        self.rsd.setText(str("%.5f" % r_sd))
        self.gsd.setText(str("%.5f" % g_sd))
        self.bsd.setText(str("%.5f" % b_sd))

        #r_var = np.var(r); g_var = np.var(g); b_var = np.var(b)
        #self.rvar.setText(str("%.5f" % r_var))
        #self.gvar.setText(str("%.5f" % g_var))
        #self.bvar.setText(str("%.5f" % b_var))

        r_skew = skew(r.reshape(-1)); g_skew = skew(g.reshape(-1)); b_skew = skew(b.reshape(-1))
        self.rskew.setText(str("%.5f" % r_skew))
        self.gskew.setText(str("%.5f" % g_skew))
        self.bskew.setText(str("%.5f" % b_skew))

        r_kurt = kurtosis(r.reshape(-1)); g_kurt = kurtosis(g.reshape(-1)); b_kurt = kurtosis(b.reshape(-1))
        self.rkurt.setText(str("%.5f" % r_kurt))
        self.gkurt.setText(str("%.5f" % g_kurt))
        self.bkurt.setText(str("%.5f" % b_kurt))

        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        h_mean = np.mean(h); s_mean = np.mean(s); v_mean = np.mean(v)
        self.Hmean.setText(str("%.5f" % h_mean))
        self.Smean.setText(str("%.5f" % s_mean))
        self.Vmean.setText(str("%.5f" % v_mean))

        h_sd = np.std(h); s_sd = np.std(s); v_sd = np.std(v)
        self.Hsd.setText(str("%.5f" % h_sd))
        self.Ssd.setText(str("%.5f" % s_sd))
        self.Vsd.setText(str("%.5f" % v_sd))

        h_skew = skew(h.reshape(-1)); s_skew = skew(s.reshape(-1)); v_skew = skew(v.reshape(-1))
        self.Hskew.setText(str("%.5f" % h_skew))
        self.Sskew.setText(str("%.5f" % s_skew))
        self.Vskew.setText(str("%.5f" % v_skew))

        h_kurt = kurtosis(h.reshape(-1));
        s_kurt = kurtosis(s.reshape(-1));
        v_kurt = kurtosis(v.reshape(-1))
        self.Hkurt.setText(str("%.5f" % h_kurt))
        self.Skurt.setText(str("%.5f" % s_kurt))
        self.Vkurt.setText(str("%.5f" % v_kurt))

        # Convert the BGR image to Lab
        Lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2Lab)
        L, a, b = cv2.split(Lab)

        L_mean = np.mean(L); a_mean = np.mean(a); b_mean = np.mean(b)
        self.CIELmean.setText(str("%.5f" % L_mean))
        self.CIEamean.setText(str("%.5f" % a_mean))
        self.CIEbmean.setText(str("%.5f" % b_mean))

        L_sd = np.std(L); a_sd = np.std(a); b_sd = np.std(b)
        self.CIELsd.setText(str("%.5f" % L_sd))
        self.CIEasd.setText(str("%.5f" % a_sd))
        self.CIEbsd.setText(str("%.5f" % b_sd))

        L_skew = skew(L.reshape(-1)); a_skew = skew(a.reshape(-1)); b_skew = skew(b.reshape(-1))
        self.CIELskew.setText(str("%.5f" % L_skew))
        self.CIEaskew.setText(str("%.5f" % a_skew))
        self.CIEbskew.setText(str("%.5f" % b_skew))

        L_kurt = kurtosis(L.reshape(-1)); a_kurt = kurtosis(a.reshape(-1)); b_kurt = kurtosis(b.reshape(-1))
        self.CIELkurt.setText(str("%.5f" % L_kurt))
        self.CIEakurt.setText(str("%.5f" % a_kurt))
        self.CIEbkurt.setText(str("%.5f" % b_kurt))

    def flipHorizontalClick(self):
        self.image = cv2.flip(self.image, 0)
        self.displayImage()
    def flipVerticalClick(self):
        self.image = cv2.flip(self.image, 90)
        self.displayImage()
    def rotateRightClick(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.displayImage()
    def rotateLeftClick(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.displayImage()
    def enhanceButtonClick(self):
        a = float(self.alphaTxt.text())
        b = float(self.betaTxt.text())
        self.image = cv2.convertScaleAbs(self.image, alpha=a, beta=b)
        self.displayImage(1)
    def bgremovalButtonClick(self):
        self.rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h, w, c = self.rgb.shape
        rectangle = (0, 0, h-1, w-1)
        self.mask = np.zeros(self.image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        cv2.grabCut(self.image, self.mask, rectangle, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        self.mask2 = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype('uint8')
        self.image_ = self.image * self.mask2[:, :, np.newaxis]

        # Make Transparent
        self.tmp_ = cv2.cvtColor(self.image_, cv2.COLOR_BGR2GRAY)
        th, self.a_ = cv2.threshold(self.tmp_, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        b, g, r, = cv2.split(self.image_)
        rgba = [r, g, b, self.a_]
        self.nobg = cv2.merge(rgba, 4)
        self.image = cv2.cvtColor(self.nobg, cv2.COLOR_RGB2BGR)
        self.displayImage(2)
    def shapeFtrButtonClick(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blank = np.zeros(self.image.shape, dtype='uint8')
        ret, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
        #self.edges = cv2.Canny(self.thresh, 50, 200)

        contour, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(blank, contour, -1, (0, 0, 255), 1)
        # numContour = len(contour)
        # self.numContour.setText(numContour)

        cnt = contour[0]

        # PERIMETER
        perimeter = cv2.arcLength(cnt, True)
        self.perimeter_.setText("%.5f" % perimeter)

        # AREA
        area = cv2.contourArea(cnt, False)
        self.area_.setText(str("%.5f" % area))

        # ROUNDNESS
        roundness = 4 * math.pi * area / (perimeter * perimeter)
        self.roundness_.setText("%.5f" % roundness)

        # EQUIVALENT DIAMETER --- the diameter of the circle whose area is same as the contour area.
        equiv_diameter = np.sqrt(4 * area / np.pi)
        self.EquivDia_.setText("%.5f" % equiv_diameter)

        # COMPLEXITY
        complexity = (perimeter * perimeter) / area
        self.complexity_.setText("%.5f" % complexity)

        # ASPECT RATIO  --- the ratio of width to height of bounding rect of the object
        rx, ry, width, height = cv2.boundingRect(cnt)
        if height  > width:
            objWidth = width
            objHeight = height
        else:
            objWidth = height
            objHeight = width
        aspect_ratio = objWidth / objHeight
        self.aspectRatio_.setText("%.5f" % aspect_ratio)

        # EXTENT --- the ratio of contour area to bounding rectangle area
        rect_area = width * height
        extent = area / rect_area
        self.extent_.setText("%.5f" % extent)

        # CONVEX HULL
        convex = cv2.convexHull(cnt)
        convex_perimeter = cv2.arcLength(convex, True)
        ConvexArea_ = cv2.contourArea(convex, False)
        self.ConvexArea_.setText("%.5f" % ConvexArea_)

        # SOLIDITY --- the ratio of contour area to its convex hull area.
        solidity = area / ConvexArea_
        self.solidity_.setText("%.5f" % solidity)

        (px, py), (Ma, ma), angle = cv2.fitEllipse(cnt)
        axLengthRatio = Ma / ma
        MinorAxis = ma
        MajorAxis = Ma
        self.minorAxis_.setText("%.5f" % MinorAxis)
        self.majorAxis_.setText("%.5f" % MajorAxis)

        compactness = math.sqrt(equiv_diameter/Ma)
        self.compactness_.setText("%.5f" % compactness)

        SF1 = Ma/area
        self.SF1_.setText("%.5f" % SF1)

        SF2 = ma/area
        self.SF2_.setText("%.5f" % SF2)

        SF3 = area/((Ma/2)*(Ma/2)*np.pi)
        self.SF3_.setText("%.5f" % SF3)

        SF4 = area/((Ma/2)*(ma/2)*np.pi)
        self.SF4_.setText("%.5f" % SF4)

        self.image = blank
        self.displayImage(2)
    def resetButtonClick(self):
        self.rmean.clear()
        self.gmean.clear()
        self.bmean.clear()
        self.rsd.clear()
        self.gsd.clear()
        self.bsd.clear()
        self.rskew.clear()
        self.gskew.clear()
        self.bskew.clear()
        self.rkurt.clear()
        self.gkurt.clear()
        self.bkurt.clear()
        self.contrast0.clear()
        self.contrast45.clear()
        self.contrast90.clear()
        self.contrast135.clear()
        self.Hmean.clear()
        self.Smean.clear()
        self.Vmean.clear()
        self.Hsd.clear()
        self.Ssd.clear()
        self.Vsd.clear()
        self.Hskew.clear()
        self.Sskew.clear()
        self.Vskew.clear()
        self.Hkurt.clear()
        self.Skurt.clear()
        self.Vkurt.clear()
        self.CIELmean.clear()
        self.CIEamean.clear()
        self.CIEbmean.clear()
        self.CIELsd.clear()
        self.CIEasd.clear()
        self.CIEbsd.clear()
        self.CIELskew.clear()
        self.CIEaskew.clear()
        self.CIEbskew.clear()
        self.CIELkurt.clear()
        self.CIEakurt.clear()
        self.CIEbkurt.clear()
        self.contrast0.clear()
        self.contrast45.clear()
        self.contrast90.clear()
        self.contrast135.clear()
        self.dissimilarity0.clear()
        self.dissimilarity45.clear()
        self.dissimilarity90.clear()
        self.dissimilarity135.clear()
        self.homogeneity0.clear()
        self.homogeneity45.clear()
        self.homogeneity90.clear()
        self.homogeneity135.clear()
        self.asm0.clear()
        self.asm45.clear()
        self.asm90.clear()
        self.asm135.clear()
        self.energy0.clear()
        self.energy45.clear()
        self.energy90.clear()
        self.energy135.clear()
        self.correlation0.clear()
        self.correlation45.clear()
        self.correlation90.clear()
        self.correlation135.clear()
        self.area_.clear()
        self.perimeter_.clear()
        self.roundness_.clear()
        self.EquivDia_.clear()
        self.complexity_.clear()
        self.aspectRatio_.clear()
        self.extent_.clear()
        self.solidity_.clear()
        self.minorAxis_.clear()
        self.majorAxis_.clear()
        self.compactness_.clear()
        self.ConvexArea_.clear()
        self.SF1_.clear()
        self.SF2_.clear()
        self.SF3_.clear()
        self.SF4_.clear()
        self.originalImage.clear()
        self.processedImage.clear()
        self.path_.clear()
        self.class_.clear()
        self.id_.clear()
        self.alphaTxt.clear()
        self.betaTxt.clear()
    def noneBlurClick(self):
        self.image = self.tmp
        self.displayImage(1)
    def cvBlurClick(self):
        self.image = self.tmp
        self.image = cv2.blur(self.image, (5,5))
        self.displayImage(1)
    def medianBlurClick(self):
        self.image = self.tmp
        self.image = cv2.medianBlur(self.image, 5)
        self.displayImage(1)
    def gausBlurClick(self):
        self.image = self.tmp
        self.image = cv2.GaussianBlur(self.image, (5,5), 0)
        self.displayImage(1)
    def boxFilterClick(self):
        self.image = self.tmp
        self.image = cv2.boxFilter(self.image, -1, (5, 5))
        self.displayImage(1)
    def bilateralFilterClick(self):
        self.image = self.tmp
        self.image = cv2.bilateralFilter(self.image, 9, 75, 75)
        self.displayImage(1)
    def denoise0Click(self):
        self.image = self.tmp
        self.displayImage(1)
    def denoise1Click(self):
        self.image = self.tmp
        self.image = cv2.fastNlMeansDenoising(self.image, None, 5)
        self.displayImage(1)
    def denoise2Click(self):
        self.image = self.tmp
        self.image = cv2.fastNlMeansDenoisingColored(self.image, None, 5, 10, 7, 10)
        self.displayImage(1)
    def helpButtonClick(self):
        QMessageBox.information(self, 'About us', 'Copyright 2022 AGUS DHARMAWAN')
    def saveimgresized(self):
        if self.image is None:
            errorDialog = QErrorMessage()
            errorDialog.showMessage('No image processed')
            errorDialog.exec()
        else:
            fname = QFileDialog.getSaveFileName(self, 'Save File', 'C:\\', "Image Files (*.png)")[0]
            if len(fname) > 0:
                cv2.imwrite(fname, self.image)
    def small_img(self):
        self.image = cv2.resize(self.image, None, fx=0.75, fy= 0.75, interpolation = cv2.INTER_CUBIC)
        self.displayImage()
    def big_img(self):
        self.image = cv2.resize(self.image, None, fx=1.5, fy= 1.5, interpolation = cv2.INTER_CUBIC)
        self.displayImage()
    def setCenter(self):
        desktop = QDesktopWidget()
        screenWidth = desktop.screen().width()
        screenHeight = desktop.screen().height()
        self.setGeometry((screenWidth - self.width()) // 2,
                      (screenHeight - self.height()) // 2,
                      self.width(), self.height())
    def displayImage(self, window = 1):
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3: #3
            if(self.image.shape[2]) == 4: #4
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()
        #self.originalImage.setPixmap(QPixmap.fromImage(img))
        #self.originalImage.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        if window == 1:
            self.originalImage.setPixmap(QPixmap.fromImage(img))
            self.originalImage.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        if window == 2:
            self.processedImage.setPixmap(QPixmap.fromImage(img))
            self.processedImage.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    def loadImage(self, fname):
        self.image = cv2.imread(fname)
        h, w, c = self.image.shape
        dim = (w,h)
        self.image = cv2.resize(self.image, dim, interpolation=cv2.INTER_LINEAR)
        self.tmp = self.image
        self.displayImage()
    def uploadButtonClick(self):
        #fname, filter = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\Users\DELL\PycharmProjects\DemoPro',"Image Files (*)")
        #self.source_filename = QFileDialog.getOpenFileName()[0]
        fname = QFileDialog.getOpenFileName()[0]
        if fname:
            self.loadImage(fname)
            c = os.path.dirname(fname)
            d = os.path.relpath(fname)
            self.path_.setText(c+'/'+d)
        else:
            print("Invalid Image")
    def captureButtonClick(self):
        self.form1 = ImageAcquisitionForm()
        self.form1.show()
    def exitButtonClick(self):
        self.close()

class FeatureExtractionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        # ==================== SETTING UP MAIN WINDOW ====================
        self.setGeometry(100,100,1200,600)   # geometry
        self.setWindowTitle('Feature Extraction Image')    # sheet style
        self.show()

    def selectImageButtonClick(self):
        # fname, filter = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\Users\DELL\PycharmProjects\DemoPro',"Image Files (*)")
        # self.source_filename = QFileDialog.getOpenFileName()[0]
        fname = QFileDialog.getOpenFileName()[0]
        if fname:
            self.loadImage(fname)
            c = os.path.dirname(fname)
            d = os.path.relpath(fname)
            self.path_.setText(c + '/' + d)
        else:
            print("Invalid Image")

class ImageAcquisitionForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        # ==================== SETTING UP MAIN WINDOW =====================
        self.setGeometry(100,100,800,600)   # geometry
        self.setWindowTitle('Image Acquisition')    # sheet style
        self.setStyleSheet("background : lightgrey;")
        # ==================== FIND CAMERA ================================
        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            sys.exit()
        # ===================== CREATE A STATUS BAR =======================
        self.status = QStatusBar()
        self.status.setStyleSheet("background : white;")
        self.setStatusBar(self.status)
        self.save_path = ""
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.select_camera(0)
        toolbar = QToolBar("Camera Tool Bar")
        self.addToolBar(toolbar)
        # ==================== CREATE AN ACTION TO TAKE A PHOTO ===========
        cameraIcon = QIcon('09-gui-icon/camera.png')
        click_action = QAction("\tTake a photo", self)
        click_action.setIcon(cameraIcon)
        click_action.setStatusTip("This will capture picture")
        click_action.setToolTip("Capture picture")
        click_action.triggered.connect(self.click_photo)
        toolbar.addAction(click_action)
        # ==================== CREATE AN ACTION OT SELECT A FOLDER AND SAVE
        folderIcon = QIcon('09-gui-icon/folder.png')
        change_folder_action = QAction("\tWhere to save", self)
        change_folder_action.setIcon(folderIcon)
        change_folder_action.setStatusTip("Change folder where picture will be saved.")
        change_folder_action.setToolTip("Select a folder to save photos")
        change_folder_action.triggered.connect(self.change_folder)
        toolbar.addAction(change_folder_action)
        # ==================== CREATE A ComboBox TO SELECT A CAMERA DEVICE =
        camera_selector = QComboBox()
        camera_selector.setStatusTip("Select a camera device")
        camera_selector.setToolTip("Select a camera device")
        camera_selector.setToolTipDuration(2500)
        camera_selector.addItems([camera.description() for camera in self.available_cameras])
        camera_selector.currentIndexChanged.connect(self.select_camera)
        toolbar.addWidget(camera_selector)
        toolbar.setStyleSheet("background : white;")
        # ===================== CREATE CLOSE ACTION ========================
        closeIcon = QIcon('09-gui-icon/exit.png')
        close_action = QAction('\tClose', self)
        close_action.setIcon(closeIcon)
        close_action.setStatusTip("Close window.")
        close_action.setToolTip('Close window')
        close_action.triggered.connect(self.close_)
        toolbar.addAction(close_action)
        # ===================== SHOW THE MAIN WINDOW =======================
        self.show()
    # TO SELECT A CAMERA DEVICE
    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()
        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda error_msg, error, msg: self.alert(msg))
        self.capture.imageCaptured.connect(lambda d, i: self.status.showMessage("Image captured : "+ str(self.save_seq)))
        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0
    # TO TAKE A PHOTO
    def click_photo(self):
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.save_path,"%s-%04d-%s.jpg" % (self.current_camera_name, self.save_seq, timestamp)))
        self.save_seq += 1
    # FOLDER LOCATION
    def change_folder(self):
        path = QFileDialog.getExistingDirectory(self,"Picture Location", "")
        if path:
            self.save_path = path
            self.save_seq = 0
    def close_(self):
        self.close()
    def alert(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)

if __name__ == '__main__':
    a = QApplication(sys.argv)
    Dialog = QDialog()
    form = MainWindow()
    a.exec_()
