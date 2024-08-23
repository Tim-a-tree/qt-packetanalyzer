import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QGridLayout
)

from src.widgets import FunctionSelect, ExecutionResults, StepDetails
from src.functions import extract_function

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Packet Analyzer")
        self.setGeometry(100, 100, 800, 600)


        # List of functions to display in the function select widget
        function_list = extract_function()

        # Create the grid layout
        layout = QGridLayout()

        # Create widgets
        # self.file_explorer = FileExplorer()
        self.step_details = StepDetails()

        # Pass the detailed result update callback
        self.execution_results = ExecutionResults(self.step_details.update_details)
        self.function_select = FunctionSelect(self.execution_results.update_results, function_list)

        # Add widgets to layout (matching your original layout design)
        # layout.addWidget(self.file_explorer, 0, 0, 2, 1)
        layout.addWidget(self.function_select, 2, 0)
        layout.addWidget(self.execution_results, 0, 1, 3, 1)
        layout.addWidget(self.step_details, 0, 2, 3, 1)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
