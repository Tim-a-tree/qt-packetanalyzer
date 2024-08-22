from PyQt5.QtWidgets import (
    QTreeView, QFileSystemModel,
)
from PyQt5.QtCore import pyqtSignal 
import os
import sys


class FileExplorer(QTreeView):
    file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Set up the file system model
        self.model = QFileSystemModel()

        # Set the path to python app directory

        root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


        self.model.setRootPath(root_dir)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(root_dir))
        self.setColumnWidth(0, 250)

        # selected file
        file_path = self.clicked.connect(self.get_selected_file)

    def get_selected_file(self, index):
        file_path = self.model.filePath(index)

        self.file_selected.emit(str(file_path))