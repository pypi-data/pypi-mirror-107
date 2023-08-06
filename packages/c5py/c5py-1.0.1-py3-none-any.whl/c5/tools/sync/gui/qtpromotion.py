from PyQt5 import QtGui, QtCore, QtWidgets


class CVVideoWidget(QtWidgets.QWidget):
    """ A class for rendering video coming from OpenCV """

    def __init__(self, processor, parent=None):
        QtWidgets.QWidget.__init__(self)
        self._image = None
        self.processor = processor
        self.setMinimumSize(300, 200)
        self.setMaximumSize(400, 800)

    def set_processor(self, processor):
        self.processor = processor

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        image = self.processor.get_current_image()
        painter.drawImage(QtCore.QPoint(0, 0), image.scaled(self.width(), self.height(), aspectRatioMode=1))
