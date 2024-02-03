import os
import subprocess
import sys
from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtGui import QAction, QPixmap, QColor, QFont , QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QPushButton,
    QFormLayout,
    QDialog,
    QLineEdit,
    QInputDialog, QLabel,
)

from OptionsWindow import OptionsWindow
from EditControlDictWindow import EditControlDictWindow
from EditFvSchemesWindow import EditFvSchemesWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create text editor widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.open_foam_logo = QLabel(self)
        self.open_foam_logo.setText("")

        

        width = 256*2  # Replace with your desired width
        height = 183  # Replace with your desired height
        self.open_foam_logo.setPixmap(QPixmap("OpenFOAM.png").scaled(width, height))
        self.open_foam_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.open_foam_logo.setScaledContents(False)    
        self.current_project_directory = None 
         # Variable to store the current project directory

        self.setWindowTitle('MainWindow')

        self.init_ui()

    def init_ui(self):

        self.setWindowIcon(QIcon('openfoam-logo.png'))

        # Create text editor widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.text_edit.setTextColor(QColor('white'))
        self.text_edit.setStyleSheet("color: #fff;\n"
"background-color:#121113;\n"
"selection-background-color:#ffaaff;\n"
"border-radius: 10px;\n"
"padding: 7px 7px;")


        # Add text to the text editor
        initial_text =  '1. Create a new Project or open an existing project\n' \
                        '2. Select a tutorial from Select dropdown menu.\n' \
                        '3. Edit the configuration files from Edit menu\n' \
                        '4. Run your project\n'

        self.text_edit.insertPlainText(initial_text)

        # Create start button
        self.start_button = QPushButton('Run Project', self)
        self.start_button.clicked.connect(self.run_command)
        
        self.start_button.setStyleSheet("color: #000;\n"
"background-color:#fff;\n"
"selection-background-color:#ffaaff;\n"
"border-radius: 10px;\n"
"padding: 7px 7px;")

        # create command label
        command_label = QLabel(self)
        command_label.setText("Command:")
        command_label.setStyleSheet("color: #fff;\n")


        # Create layout for start button
        button_layout = QFormLayout()
        button_layout.addRow(command_label , self.start_button)

        # Create central widget
        central_widget = QWidget(self)
        central_widget.setObjectName("centralwidget")
        central_widget.setStyleSheet("#centralwidget{background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(81, 0, 135, 255), stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(155, 79, 165, 255));}")
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.open_foam_logo)
        central_layout.addWidget(self.text_edit)
        central_layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

        # Create menu bar
        menubar = self.menuBar()


        menubar.setStyleSheet("color: #000;\n"
"background-color:#f0f0f0;\n"
"selection-background-color:#ffaaff;\n"
"padding: 1px 1px;")

        # File menu
        file_menu = menubar.addMenu('File')

        new_project_action = QAction('New Project', self)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)

        open_project_action = QAction('Open Existing Project', self)
        open_project_action.triggered.connect(self.open_existing_project)
        file_menu.addAction(open_project_action)

        save_action = QAction('Save Progress', self)
        save_action.triggered.connect(self.save_progress)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Select menu
        select_menu = menubar.addMenu('Select')

        select_tutorial_action = QAction('Select Tutorial', self)
        select_tutorial_action.triggered.connect(self.show_options_window)
        select_menu.addAction(select_tutorial_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')

        # ControlDict edit action
        control_dict_action = QAction('Edit ControlDict', self)
        control_dict_action.triggered.connect(self.edit_control_dict)
        edit_menu.addAction(control_dict_action)

        # fvSchemes edit action
        fv_schemes_action = QAction('Edit fvSchemes', self)
        fv_schemes_action.triggered.connect(self.edit_fv_schemes)
        edit_menu.addAction(fv_schemes_action)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('OpenFoam GUI')
        self.show()

    def save_progress(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, 'Save Progress', '', 'Text Files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def run_command(self):
        # Build the WSL command to run "./Allrun" and capture the output
        wsl_path = '/mnt/c/' + self.current_project_directory.replace('\\', '/').lstrip('C:').lstrip('/')
        print(wsl_path)
        wsl_command = f"cd '{wsl_path}' && source /usr/lib/openfoam/openfoam2306/etc/bashrc && blockMesh && icoFoam && foamToVTK"

        print("Running command:", wsl_command)

        process = QProcess(self)
        process.readyReadStandardOutput.connect(self.update_output)
        process.started.connect(lambda: print("Process started"))
        process.finished.connect(lambda exit_code, exit_status: print("Process finished with exit code:", exit_code))
        process.errorOccurred.connect(lambda error: print("Error occurred:", error))

        process.start(wsl_command)

        # Launch a cmd window while running the WSL command and capturing the output
        cmd_command = f"wsl -e bash -c \"{wsl_command}\""
        process = subprocess.Popen(cmd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                   text=True)


        self.text_edit.clear()
        # Create a dialog to display the progress
        #progress_dialog = QDialog(self)
      #  progress_dialog.setWindowTitle("Progress")
       # progress_dialog.setGeometry(200, 200, 700, 400)
       # progress_layout = QVBoxLayout(progress_dialog)
       # progress_label = QLabel("Running WSL command:")
      #  progress_layout.addWidget(progress_label)
        
        # progress_text = QTextEdit(progress_dialog)
        # progress_text.setReadOnly(True)
        # progress_layout.addWidget(progress_text)
        # progress_dialog.setLayout(progress_layout)
        # progress_dialog.show()

        # Read and display the output while the process is running
        while process.poll() is None:
            output_line = process.stdout.readline()
            self.text_edit.insertPlainText(output_line)
           # progress_text.append(output_line)
            QApplication.processEvents()

        #Capture any remaining output
        output, error = process.communicate()
        self.text_edit.insertPlainText(output)
        #progress_text.append(output)
        self.text_edit.insertPlainText(error)
       # progress_text.append(error)

       # progress_dialog.exec()

    def update_output(self):
        process = self.sender()
        output = process.readAllStandardOutput().data().decode('utf-8')
        self.text_edit.insertPlainText(output)
      #  self.text_edit.append(output)

    def new_project(self):
        # Show a dialog to get a new project name
        new_project_name, ok = QInputDialog.getText(self, 'New Project', 'Enter a name for the new project:')

        if ok and new_project_name:
            # Create a new directory using the specified name
            directory = QFileDialog.getExistingDirectory(self, 'Select New Project Directory',
                                                         self.current_project_directory)
            if directory and os.path.exists(directory):  # Check if the directory exists
                new_project_directory = os.path.join(directory, new_project_name)
                os.makedirs(new_project_directory, exist_ok=True)

                # Set the current project directory and update the UI
                self.current_project_directory = new_project_directory
                self.setWindowTitle(f'MainWindow - {new_project_directory}')
                print(f'New Project created in directory: {new_project_directory}')
            elif directory:
                print(f'Selected directory does not exist: {directory}')

    def open_existing_project(self):
        # Show a dialog to select an existing project directory
        directory = QFileDialog.getExistingDirectory(self, 'Select Existing Project Directory',
                                                     self.current_project_directory)
        if directory and os.path.exists(directory):  # Check if the directory exists
            # Set the current project directory and update the UI
            self.current_project_directory = directory
            self.setWindowTitle(f'MainWindow - {directory}')
            print(f'Opened Existing Project in directory: {directory}')
        elif directory:
            print(f'Selected directory does not exist: {directory}')

    def show_options_window(self):
        options_window = OptionsWindow(self.current_project_directory, self)
        options_window.exec()

        # Update self.current_project_directory after the OptionsWindow is closed
        if options_window.destination_directory:
            self.current_project_directory = options_window.destination_directory
            self.setWindowTitle(f'MainWindow - {self.current_project_directory}')
            print(self.current_project_directory)

    def edit_control_dict(self):
        if self.current_project_directory:
            control_dict_path = os.path.join(self.current_project_directory, 'system', 'controlDict')
            if os.path.isfile(control_dict_path):
                edit_control_dict_window = EditControlDictWindow(control_dict_path)
                edit_control_dict_window.exec()
            else:
                print("ControlDict file not found.")

    def edit_fv_schemes(self):
        if self.current_project_directory:
            fv_schemes_path = os.path.join(self.current_project_directory, 'system', 'fvSchemes')
            if os.path.isfile(fv_schemes_path):
                edit_fv_schemes_window = EditFvSchemesWindow(fv_schemes_path)
                edit_fv_schemes_window.exec()
            else:
                print("fvSchemes file not found.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
