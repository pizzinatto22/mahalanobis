import math
import sys
import Utils

from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("MainWindow.ui")[0]      # Load the UI
 
class Main(QtGui.QDialog, form_class):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.loadBtn.clicked.connect(self.loadImage)  # Bind the event handlers
        self.resetBtn.clicked.connect(self.resetImage)
        self.testBtn.clicked.connect(self.test)

        self.originalGV.setMouseTracking(True)
        self.originalGV.viewport().installEventFilter(self)
        
        self.originalGV.setScene(QtGui.QGraphicsScene())
        self.patternGV.setScene(QtGui.QGraphicsScene())

        self.originalImage = None
        self.modifiedImage = None
        self.data          = None
        self.coordinates   = set()
        self.samples       = []


    def eventFilter(self, source, event):
        gv     = self.originalGV
        image  = self.originalImage
        radius = self.radius.value()

        if (event.type() == QtCore.QEvent.MouseMove and
            source is gv.viewport() and
            event.buttons() != QtCore.Qt.NoButton and
            image):

            pos = event.pos()
            pos = gv.mapToScene(pos).toPoint()
            
            if (image.rect().contains(pos)):
                self.sample(pos, radius)
        
        return QtGui.QWidget.eventFilter(self, source, event)


    def loadImage(self):
        file_name = QtGui.QFileDialog.getOpenFileName()

        if (file_name):
            image = QtGui.QImage(file_name)
            
            #resize image to fit in QGraphicsView
            sizeGV = self.originalGV.geometry().size()
            image = image.scaled(sizeGV, QtCore.Qt.KeepAspectRatio)

            self.originalImage = image
            self.modifiedImage = QtGui.QImage(image)
            self.draw(self.originalGV.scene(), image)


    def resetImage(self):
        self.coordinates   = set()
        self.data          = None
        self.samples       = []

        if (self.originalImage):
            self.modifiedImage = QtGui.QImage(self.originalImage)
            self.draw(self.originalGV.scene(), self.originalImage)


    def test(self):
        if (len(self.samples) > 0):
            if self.mahalanobis.isChecked():
                mahalanobis = Utils.mahalanobis(self.originalImage, 
                                       self.samples) 
            else:
                mahalanobis = Utils.euclidean(self.originalImage,
                                       self.samples)

            image = Utils.generateImage(mahalanobis['data'], self.threshold.value(), self.grayscale.isChecked())
            self.avg.setText(str(mahalanobis['avg']))

            self.draw(self.patternGV.scene(), image)

        else:
            QtGui.QMessageBox.information(None, "Sample error", "There are no selected samples")


    def draw(self, scene, image):
        pixmap = QtGui.QPixmap(image.size())
        pixmap.convertFromImage(image)
        pixItem = QtGui.QGraphicsPixmapItem(pixmap)

        scene.clear()
        scene.addItem(pixItem)


    def sample(self, point, radius):
        scene  = self.originalGV.scene()
        image  = self.modifiedImage
        rect   = image.rect()

        #sampling all pixels from certain radius
        rx = point.x()
        ry = point.y()
        for x in range(rx - radius, rx + radius):
            for y in range (ry - radius, ry + radius):
                if (rect.contains(x, y)):
                        #if this coordinate wasn't sampled yet
                        if ((x,y) not in self.coordinates):
                            distance = math.sqrt((rx - x)**2 + (ry - y) **2)
                            if (distance <= radius ):
                                self.coordinates.add((x,y))           #do not sample this position anymore
                                self.samples.append(image.pixel(x,y)) #sample this pixel
                                image.setPixel(x, y, 0)
                                self.draw(scene, image)


app = QtGui.QApplication(sys.argv)
myWindow = Main(None)
myWindow.show()
app.exec_()
