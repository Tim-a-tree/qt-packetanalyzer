from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)
from PyQt5.QtCore import Qt


from src.widgets.file_explorer import FileExplorer
from src.functions import get_result, check_all
# shared variable
from src.shared_variable import list_result

class FunctionSelect(QWidget):
    def __init__(self, on_execute_callback, function_list):
        super().__init__()
        self.on_execute_callback = on_execute_callback  # Callback to trigger function execution

        layout = QVBoxLayout()


        # Add an instance of FileExplorer
        self.file_explorer = FileExplorer()
        self.file_explorer.file_selected.connect(self.update_selected_file)
        layout.addWidget(self.file_explorer)

        self.label = QLabel("Function Selection")
        layout.addWidget(self.label)

        # Create a QListWidget for selecting functions
        self.list_widget = QListWidget()

        # Add an "Analyze All" item to the list
        item = QListWidgetItem("Analyze All")
        item.setData(Qt.UserRole, None)
        self.list_widget.addItem(item)

        for function, data in function_list:
            print(f"Function: {function}, Data: {data}")
            item = QListWidgetItem(function)
            item.setData(Qt.UserRole, data)
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)


        # Add an "Execute" button under the list
        self.execute_button = QPushButton("Execute Selected Function")
        self.execute_button.clicked.connect(self.execute_function)
        layout.addWidget(self.execute_button)

        self.setLayout(layout)


    def update_selected_file(self, file_path):
        self.selected_file = file_path

    def execute_function(self):
        list_result.clear()

        # Get the currently selected item
        selected_item = self.list_widget.currentItem()
        keywords = selected_item.data(Qt.UserRole) if selected_item else None
        if selected_item:
            selected_function = selected_item.text()
            # if 'Analyze All' is selected, execute all functions
            if selected_function == "Analyze All":
                check_all(self.selected_file)
            else:
                get_result(selected_function, self.selected_file)
            # Simulate the execution result for the selected function
            simulated_results = [
              self.selected_file,
              selected_function,
            ]
            # Pass the simulated results to the execution results section
            self.on_execute_callback(selected_function, simulated_results)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a function to execute.")