from PyQt5.QtWidgets import (
  QWidget, QVBoxLayout, QLabel, QListWidgetItem, QListWidget
)
from PyQt5.QtCore import Qt

from src.shared_variable import list_result
from src.models import Result



class ExecutionResults(QWidget):
    def __init__(self, detailed_result_callback):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Execution Results")
        layout.addWidget(self.label)

        # Store the detailed result callback
        self.detailed_result_callback = detailed_result_callback

        self.list_widget = QListWidget()

        layout.addWidget(self.list_widget)


        self.setLayout(layout)

    '''
    Updates the results list with the given results for the selected function
    '''
    def update_results(self, function_name, data):
        # Clear the previous results
        self.list_widget.clear()

        # Add the new results for the selected function
        for component in data:
            item = QListWidgetItem(f"{component}")
            # item.setForeground(Qt.green if status == "PASS" else Qt.red)
            self.list_widget.addItem(item)



        for element in list_result:
            # condtion check of identifying string or Result object of list
            if isinstance(element, str):
                item = QListWidgetItem(element)
                self.list_widget.addItem(item)
            else:
                item = QListWidgetItem(self.parse_result_object(element))

                if element.packet_data is not None:
                    item.setData(Qt.UserRole, element.packet_data)
                else:
                    item.setData(Qt.UserRole, "")
                item.setForeground(self._set_color(element.status))
                self.list_widget.addItem(item)

        # Trigger detailed view when an item is selected
        self.list_widget.currentItemChanged.connect(self.show_details)

    def show_details(self, data : QListWidgetItem):
        if data is None:
            return
        self.detailed_result_callback(data.data(Qt.UserRole))



    
    def parse_result_object(self, result : Result) -> str:
        txt_req = ""
        if result.req_type == True:
            txt_req = "Request"
        else:
            txt_req = "Response"

        if result.status == "PASS":
            # return green color text
            return f"{txt_req}\t{result.packet_number}\t{result.status}"
        if result.status == "POSSIBLE":
            # return yellow color text
            return f"{txt_req}\t{result.packet_number}\t{result.status}"
        if result.status == "FAIL":
            # return red color text
            return f"{txt_req}\t{result.status}"
        
    def _set_color(self, status):
        if status == "PASS":
            return Qt.darkGreen
        if status == "POSSIBLE":
            return Qt.darkYellow
        if status == "FAIL":
            return Qt.darkRed
        return Qt.black