import sys, os, time, platform
import matplotlib.pyplot as mp
import numpy             as np
import PyQt5, PyQt5.QtCore, PyQt5.QtWidgets

from scipy.stats import (
  norm
)

from PyQt5.QtCore import (
  Qt     ,
  QTimer
)

from PyQt5.QtWidgets import (
  QApplication   ,
  QMainWindow    ,
  QStyle         ,
  QMessageBox    ,
  QLabel         ,
  QLineEdit      ,
  QTextEdit      ,
  QPlainTextEdit ,
  QVBoxLayout    ,
  QHBoxLayout    ,
  QGridLayout    ,
  QComboBox      ,
  QPushButton    ,
  QCheckBox      ,
  QFileDialog    ,
  QScrollBar     ,
  QSlider        ,
  QWidget
)

# ----------------------------------------------------------------
# Analizer

class Analizer(QMainWindow):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Analizer')
    name = getattr(QStyle, 'SP_ComputerIcon')
    icon = self.style().standardIcon(name)
    self.setWindowIcon(icon)

    self.layout   = QVBoxLayout()
    self.layout_0 = QHBoxLayout()
    self.layout_1 = QHBoxLayout()

    self.button_0 = QPushButton('Import')
    self.button_0.clicked.connect(self.load)
    self.button_1 = QPushButton('Export')
    self.button_1.clicked.connect(self.save)
    self.button_2 = QPushButton('Analize')
    self.button_2.clicked.connect(self.analize)

    self.text_0 = QPlainTextEdit()
    self.text_0.setLineWrapMode(QPlainTextEdit.NoWrap)
    self.text_1 = QPlainTextEdit()
    self.text_1.setReadOnly(True)
    self.text_1.setLineWrapMode(QPlainTextEdit.NoWrap)

    self.slider_0 = QSlider(Qt.Horizontal)
    self.slider_0.setTickPosition(QSlider.TicksBothSides)
    self.slider_0.setTickInterval(100)
    self.slider_0.setSingleStep(1)
    self.slider_0.valueChanged.connect(self.updateBins)

    self.label_0 = QLabel()
    self.label_0.setText('Bins')
    self.label_1 = QLabel()
    self.label_1.setText(str(1 + self.slider_0.value()))

    self.layout_0.addWidget(self.text_0)
    self.layout_0.addWidget(self.text_1)
    self.layout_1.addWidget(self.button_0)
    self.layout_1.addWidget(self.button_1)
    self.layout_1.addWidget(self.button_2)
    self.layout_1.addWidget(self.label_0)
    self.layout_1.addWidget(self.slider_0)
    self.layout_1.addWidget(self.label_1)
    self.layout.addLayout(self.layout_0)
    self.layout.addLayout(self.layout_1)

    widget = QWidget(self)
    widget.setLayout(self.layout)
    self.setCentralWidget(widget)

  def updateBins(self):
    self.label_1.setText(str(self.slider_0.value()))

  def error(self, text):
    box = QMessageBox(self)
    box.setIcon(QMessageBox.Critical)
    box.setWindowTitle('Error')
    box.setText(text)
    box.exec()

  def load(self):
    options = QFileDialog.Options() | QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(self, 'Import', '', 'All Files (*);;Text Files(*.txt)', options = options)
    if filename:
      with open(filename, 'r') as f:
        self.text_0.setPlainText(str(f.read()))
    else:
      self.error('Cannot read from the file')

  def save(self):
    options = QFileDialog.Options() | QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getSaveFileName(self, 'Export', '', 'All Files(*);;Text Files(*.txt)', options = options)
    if filename:
      with open(filename, 'w') as f:
        f.write(self.text_0.toPlainText())
    else:
      self.error('Cannot write to the file')

  def analize(self):
    self.text_1.setPlainText('')
    s = self.text_0.toPlainText()
    v = s.split(sep = '\n')
    v = [ int(i) for i in v ]
    n = len(v)
    if n <= 2:
      self.error('The sample is too poor')
      return
    mean, sd = norm.fit(v)
    self.text_1.setPlainText(
      'N = ' + str(n) + '\nMean = ' + str(mean) + '\nStd. Dev. = ' + str(sd) + '\n'
    )
    self.slider_0.setTickInterval(int(np.sqrt(n)))
    mp.hist(v, bins = 1 + self.slider_0.value(), density = True)
    xmin, xmax = mp.xlim()
    x = np.linspace(xmin, xmax, 100)
    mp.ylabel('Frequency')
    mp.xlabel('Time (ms)')
    mp.plot(x, norm.pdf(x, mean, sd))
    mp.show()

# ----------------------------------------------------------------
# Application

def run():
  app = QApplication(sys.argv)
  ana = Analizer()
  ana.show()
  sys.exit(app.exec()) # use `exec_` in Python < 3

run() # entry point