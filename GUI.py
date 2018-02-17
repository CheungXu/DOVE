# -*- coding:utf-8 -*-  
import sys
from PyQt4 import QtGui,QtCore
import experiment

class GUI(QtGui.QWidget):

           def __init__(self):
                      super(GUI, self).__init__()
                      self.exp = experiment.Experiments(20,3)
                      self.matching = self.exp.unidirectional_match()
                      self.initUI()

           def initUI(self):
                      self.setWindowTitle(' Stable Matching ')
                      grid = QtGui.QGridLayout()
                      step_button = QtGui.QPushButton('STEP',self)
                      epoch_button = QtGui.QPushButton('EPOCH',self)
                      end_button = QtGui.QPushButton('END',self)
                      self.showText = QtGui.QTextEdit(self)
                      self.showText.setText('START! ')
                      
                      grid.addWidget(step_button,1,1)
                      grid.addWidget(epoch_button,2,1)
                      grid.addWidget(end_button,3,1)
                      grid.addWidget(self.showText,1,2,5,1)
                      self.setLayout(grid)
                      
                      self.connect(step_button,QtCore.SIGNAL('clicked()'),self.nextStep)
                      self.connect(epoch_button,QtCore.SIGNAL('clicked()'),self.nextEpoch)
                      self.connect(end_button,QtCore.SIGNAL('clicked()'),self.exeToEnd)
                      self.resize(500,800)
                      
           def nextStep(self):
                      info = self.matching.step()
                      self.showText.setText(info)

           def nextEpoch(self):
                      info = self.matching.epoch()
                      self.showText.setText(info)

           def exeToEnd(self):
                      info = self.matching.exe_to_end()
                      self.showText.setText(info)
           
           def closeEvent(self, event):
                      reply = QtGui.QMessageBox.question(self, 'Message',
                                                         'Are you sure to quit?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                      if reply == QtGui.QMessageBox.Yes:
                                 event.accept()
                      else:
                                 event.ignore()

if __name__ == '__main__':
           app = QtGui.QApplication(sys.argv)
           gui = GUI()
           gui.show()
           sys.exit(app.exec_())
