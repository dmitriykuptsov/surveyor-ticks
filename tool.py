#!/usr/bin/python3

# Copyright (C) 2023 Micromine
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Dmitriy Kuptsov"
__copyright__ = "Copyright 2023, Micromine"
__license__ = "GPL"
__version__ = "0.0.1a"
__maintainer__ = "Dmitriy Kuptsov"
__email__ = "dkuptsov@micromine.com"
__status__ = "development"

# System stuff
import sys

# OS stuff
import os

# Regular expressions
import re

# UI PyQT stuff
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Main algorithm module
import algo

class GUI(QWidget):
   def __init__(self, parent = None):
      super(GUI, self).__init__(parent)

      self.contours_file = ""
      self.output_folder = ""
		
      layout = QGridLayout()
      
      self.contour_file_name_txb = QLineEdit(self)
      layout.addWidget(self.contour_file_name_txb, 0, 0)

      self.contour_file_btn = QPushButton("Select contour file name")
      self.contour_file_btn.clicked.connect(self.getContourFileName)
      layout.addWidget(self.contour_file_btn, 0, 1)

      self.output_folder_txb = QLineEdit(self)
      layout.addWidget(self.output_folder_txb, 1, 0)

      self.output_folder_btn = QPushButton("Select output folder")
      self.output_folder_btn.clicked.connect(self.getOutputFolder)
      layout.addWidget(self.output_folder_btn, 1, 1)

      self.output_file_name_txb = QLineEdit(self)
      layout.addWidget(self.output_file_name_txb, 2, 0)

      layout.addWidget(QLabel('Output file name'), 2, 1)

      self.step_txb = QLineEdit(self)
      layout.addWidget(self.step_txb, 3, 0)
      self.step_txb.setText("1")

      layout.addWidget(QLabel('Step'), 3, 1)

      self.run_btn = QPushButton("Run the algorithm")
      self.run_btn.clicked.connect(self.runAlgorithm)
      layout.addWidget(self.run_btn, 4, 0)

      self.setLayout(layout)
      self.setWindowTitle("Surveyor ticks calculation tool")

   def runAlgorithm(self):

      if not re.match("[a-zA-Z0-9\_\-]+\.csv", self.output_file_name_txb.text().strip()):
         QMessageBox.question(self, 'Micromine', "Wrong output file name! Must be a valid .csv file", QMessageBox.Ok, QMessageBox.Ok)
         return
      print(os.path.basename(self.contours_file.strip()))
      if not re.match("[a-zA-Z0-9\_\-]+\.csv", os.path.basename(self.contours_file.strip())):
         QMessageBox.question(self, 'Micromine', "Wrong input file name! Must be a valid .csv file", QMessageBox.Ok, QMessageBox.Ok)
         return

      if self.output_folder == "":
         self.output_folder = os.getcwd()
      
      input_file = self.contours_file.strip()
      output_file = os.path.join(self.output_folder, self.output_file_name_txb.text().strip())
      try:
         step = float(self.step_txb.text().strip())
      except:
         step = 1.0
      result = algo.run(input_file, output_file, step)
      if not result[0]:
         if result[1] == CONTOURS_ARE_NOT_CLOSED_ERROR:
            QMessageBox.question(self, 'Micromine', "Contours are not closed", QMessageBox.Ok, QMessageBox.Ok)
         elif result[1] == NOT_EVEN_NUMBER_OF_CONTOURS:
            QMessageBox.question(self, 'Micromine', "Number of contours must be even", QMessageBox.Ok, QMessageBox.Ok)
         elif result[1] == CONTOURS_OVERLAP:
            QMessageBox.question(self, 'Micromine', "Contours overlap!", QMessageBox.Ok, QMessageBox.Ok)
      else:
         QMessageBox.question(self, 'Micromine', "Algorithm completed successfully", QMessageBox.Ok, QMessageBox.Ok)

   def getOutputFolder(self):
      fname = QFileDialog.getExistingDirectory(self, os.getcwd())
      if fname:
         self.output_folder = fname
         self.output_folder_txb.setText(fname)

   def getContourFileName(self):
      fname = QFileDialog.getOpenFileName(self, 'Open pit contours file', 
         os.getcwd(),"Comma seperated files (*.csv)")
      if fname:
         self.contours_file = fname[0]
         self.contour_file_name_txb.setText(fname[0])
      else:
         self.contours_file = ""
				
def main():
   app = QApplication(sys.argv)
   ex = GUI()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
