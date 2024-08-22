from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLabel
import ast

'''
The StepDetail Widget
- Displays the details of a selected step
- Updates the text edit field with the selected step's data

'''


class StepDetails(QWidget):
    '''
    On initialization, create a QVBoxLayout and add a QLabel and QTextEdit to the layout
    '''
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Details")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.setLayout(layout)



    '''
    Function
    Update the text edit field with the selected step's data

    Param
    packet_data - string : The data of the selected step from ExecutionResults

    Issues
    - there are some cases where the data has a non-string type
    '''
    def update_details(self, packet_data):
        if packet_data is None:
            self.text_edit.setPlainText("")
            return
        
        if isinstance(packet_data, str):
            try:
                # Attempt to convert to a Python literal
                packet_data = ast.literal_eval(packet_data)
            except (SyntaxError, ValueError):
                # Handle invalid literal error
                print("Error: Invalid input for literal_eval")
                self.text_edit.setPlainText("Error: Cannot display non-string data")
                return

        # Decode and display the packet data
        try:
            decoded_data = packet_data.decode('utf-8', errors='replace')
            self.text_edit.setPlainText(decoded_data)
        except AttributeError:
            # If packet_data is already a string
            self.text_edit.setPlainText(packet_data)