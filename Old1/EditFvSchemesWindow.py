from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox


class EditFvSchemesWindow(QDialog):
    def __init__(self, fv_schemes_path):
        super().__init__()
        self.setWindowTitle("Edit fvSchemes")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        # Add ddtSchemes section
        self.ddt_schemes_label = QLabel("ddtSchemes:")
        self.ddt_schemes_combobox = QComboBox()
        self.ddt_schemes_combobox.addItems(["Euler", "localEuler", "CrankNicholson", "backward", "steadyState"])
        self.layout.addWidget(self.ddt_schemes_label)
        self.layout.addWidget(self.ddt_schemes_combobox)

        # Add gradSchemes section
        self.grad_schemes_label = QLabel("gradSchemes:")
        self.grad_schemes_combobox = QComboBox()
        self.grad_schemes_combobox.addItems(["corrected", "uncorrected", "limited", "bounded", "fourth"])
        self.layout.addWidget(self.grad_schemes_label)
        self.layout.addWidget(self.grad_schemes_combobox)

        self.divSchemes_label = QLabel("divSchemes:")
        self.divSchemes_combobox = QComboBox()
        self.divSchemes_combobox.addItems(["linear", "skewLinear", "cubicCorrected", "upwind", "linearUpwind","QUICK", "TVD schemes", "SFCD", "NVD schemes"])
        self.layout.addWidget(self.divSchemes_label)
        self.layout.addWidget(self.divSchemes_combobox)

        self.laplacianSchemes_label = QLabel("laplacianSchemes:")
        self.laplacianSchemes_combobox = QComboBox()
        self.laplacianSchemes_combobox.addItems(["corrected", "uncorrected", "limited", "bounded", "fourth"])
        self.layout.addWidget(self.laplacianSchemes_label)
        self.layout.addWidget(self.laplacianSchemes_combobox)

        self.interpolationSchemes_label = QLabel("interpolationSchemes:")
        self.interpolationSchemes_combobox = QComboBox()
        self.interpolationSchemes_combobox.addItems(["linear", "cubicCorrection", "midPoint", "Upwinded", "upwind","linearUpwind", "skewLinear", "filteredLinear2"])
        self.layout.addWidget(self.interpolationSchemes_label)
        self.layout.addWidget(self.interpolationSchemes_combobox)

        self.TVD_schemes_label = QLabel("TVD_schemes:")
        self.TVD_schemes_combobox = QComboBox()
        self.TVD_schemes_combobox.addItems(["limitedLinear", "vanLeer", "MUSCL", "limitedCubic"])
        self.layout.addWidget(self.TVD_schemes_label)
        self.layout.addWidget(self.TVD_schemes_combobox)
        
        self.NVD_schemes_label = QLabel("NVD_schemes:")
        self.NVD_schemes_combobox = QComboBox()
        self.NVD_schemes_combobox.addItems(["SFCD", "Gamma"])
        self.layout.addWidget(self.NVD_schemes_label)
        self.layout.addWidget(self.NVD_schemes_combobox)

        self.snGradSchemes_label = QLabel("snGradSchemes:")
        self.snGradSchemes_combobox = QComboBox()
        self.snGradSchemes_combobox.addItems(["corrected", "uncorrected", "limited", "bounded", "fourth"])
        self.layout.addWidget(self.snGradSchemes_label)
        self.layout.addWidget(self.snGradSchemes_combobox)


        



        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_fv_schemes)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.fv_schemes_path = fv_schemes_path

        # Load and display the current values of ddtSchemes and gradSchemes
        self.load_fv_schemes_values()

    def load_fv_schemes_values(self):
        schemes_found = {"ddtSchemes": False, "gradSchemes": False, "divSchemes": False,"laplacianSchemes": False , "interpolationSchemes": False, "TVD_schemes": False, "NVD_schemes": False, "snGradSchemes": False }
        with open(self.fv_schemes_path, 'r') as file:
            for line in file:
                if line.startswith("ddtSchemes"):
                    schemes_found["ddtSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.ddt_schemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'ddtSchemes'.")
                        
                elif line.startswith("gradSchemes"):
                    schemes_found["gradSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.grad_schemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'gradSchemes'.")

                elif line.startswith("divSchemes"):
                    schemes_found["divSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.divSchemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'divSchemes'.")

                elif line.startswith("laplacianSchemes"):
                    schemes_found["laplacianSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.laplacianSchemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'laplacianSchemes'.")

                elif line.startswith("interpolationSchemes"):
                    schemes_found["interpolationSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.interpolationSchemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'interpolationSchemes'.")

                elif line.startswith("TVD_schemes"):
                    schemes_found["TVD_schemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.TVD_schemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'TVD_schemes'.")

                elif line.startswith("NVD_schemes"):
                    schemes_found["NVD_schemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.NVD_schemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'NVD_schemes'.")
                
                elif line.startswith("snGradSchemes"):
                    schemes_found["snGradSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.snGradSchemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'snGradSchemes'.")




        if not schemes_found["ddtSchemes"]:
            print("Warning: 'ddtSchemes' not found in the file.")

        if not schemes_found["gradSchemes"]:
            print("Warning: 'gradSchemes' not found in the file.")

        if not schemes_found["divSchemes"]:
            print("Warning: 'divSchemes' not found in the file.")

        if not schemes_found["laplacianSchemes"]:
            print("Warning: 'laplacianSchemes' not found in the file.")

        if not schemes_found["interpolationSchemes"]:
            print("Warning: 'interpolationSchemes' not found in the file.")

        if not schemes_found["TVD_schemes"]:
            print("Warning: 'TVD_schemes' not found in the file.")

        if not schemes_found["NVD_schemes"]:
            print("Warning: 'NVD_schemes' not found in the file.")

        if not schemes_found["snGradSchemes"]:
            print("Warning: 'snGradSchemes' not found in the file.")



    def save_fv_schemes(self):
        # Get the selected ddtScheme and gradScheme from the comboboxes
        selected_ddt_scheme = self.ddt_schemes_combobox.currentText()
        selected_grad_scheme = self.grad_schemes_combobox.currentText()
        selected_divSchemes = self.divSchemes_combobox.currentText()
        selected_laplacianSchemes = self.laplacianSchemes_combobox.currentText()
        selected_interpolationSchemes = self.laplacianSchemes_combobox.currentText()
        selected_TVD_schemes = self.laplacianSchemes_combobox.currentText()
        selected_NVD_schemes = self.laplacianSchemes_combobox.currentText()
        selected_snGradSchemes = self.laplacianSchemes_combobox.currentText()

        # Update the fvSchemes file with the edited values
        updated_lines = []
        schemes_found = {"ddtSchemes": False, "gradSchemes": False, "divSchemes": False, "laplacianSchemes": False ,"interpolationSchemes": False ,"TVD_schemes": False ,"NVD_schemes": False ,"snGradSchemes": False }
        inside_ddt_schemes_block = False
        inside_grad_schemes_block = False
        inside_divSchemes_block = False
        inside_laplacianSchemes_block = False
        inside_interpolationSchemes_block = False
        inside_TVD_schemes_block = False
        inside_NVD_schemes_block = False
        inside_snGradSchemes_block = False
        
        with open(self.fv_schemes_path, 'r') as file:
            for line in file:
                if line.startswith("ddtSchemes"):
                    schemes_found["ddtSchemes"] = True
                    inside_ddt_schemes_block = True
                    try:
                        updated_lines.append(f"ddtSchemes\n{{\n    default         {selected_ddt_scheme};\n}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'ddtSchemes'.")
                elif line.startswith("gradSchemes"):
                    schemes_found["gradSchemes"] = True
                    inside_grad_schemes_block = True
                    try:
                        updated_lines.append(f"gradSchemes\n{{\n    default         {selected_grad_scheme};\n    grad(p)         Gauss linear;}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'gradSchemes'.")

                elif line.startswith("divSchemes"):
                    schemes_found["divSchemes"] = True
                    inside_divSchemes_block = True
                    try:
                        updated_lines.append(f"divSchemes\n{{\n    default         {selected_divSchemes};\n}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'divSchemes'.")
                        
                
                elif line.startswith("laplacianSchemes"):
                    schemes_found["laplacianSchemes"] = True
                    inside_laplacianSchemes_block = True
                    try:
                        updated_lines.append(f"laplacianSchemes\n{{\n    default         {selected_laplacianSchemes};\n}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'laplacianSchemes'.")

                elif line.startswith("interpolationSchemes"):
                    schemes_found["interpolationSchemes"] = True
                    inside_interpolationSchemes_block = True
                    try:
                        updated_lines.append(f"interpolationSchemes\n{{\n    default         {selected_interpolationSchemes};\n    grad(p)         Gauss linear;}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'interpolationSchemes'.")

                elif line.startswith("TVD_schemes"):
                    schemes_found["TVD_schemes"] = True
                    inside_TVD_schemes_block = True
                    try:
                        updated_lines.append(f"TVD_schemes\n{{\n    default         {selected_TVD_schemes};\n    grad(p)         Gauss linear;}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'TVD_schemes'.")

                elif line.startswith("NVD_schemes"):
                    schemes_found["NVD_schemes"] = True
                    inside_NVD_schemes_block = True
                    try:
                        updated_lines.append(f"NVD_schemes\n{{\n    default         {selected_NVD_schemes};\n    grad(p)         Gauss linear;}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'NVD_schemes'.")

                elif line.startswith("snGradSchemes"):
                    schemes_found["snGradSchemes"] = True
                    inside_snGradSchemes_block = True
                    try:
                        updated_lines.append(f"snGradSchemes\n{{\n    default         {selected_snGradSchemes};\n    grad(p)         Gauss linear;}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'snGradSchemes'.")

                
                        

                elif inside_ddt_schemes_block and line.strip() == "}":
                    inside_ddt_schemes_block = False
                elif inside_grad_schemes_block and line.strip() == "}":
                    inside_grad_schemes_block = False
                elif inside_divSchemes_block and line.strip() == "}":
                    inside_divSchemes_block = False
                elif inside_laplacianSchemes_block and line.strip() == "}":
                    inside_laplacianSchemes_block = False
                elif inside_interpolationSchemes_block and line.strip() == "}":
                    inside_interpolationSchemes_block = False 
                elif inside_TVD_schemes_block and line.strip() == "}":
                    inside_TVD_schemes_block = False 
                elif inside_NVD_schemes_block and line.strip() == "}":
                    inside_NVD_schemes_block = False 
                elif inside_snGradSchemes_block and line.strip() == "}":
                    inside_snGradSchemes_block = False 
                elif not inside_ddt_schemes_block and not inside_grad_schemes_block and not inside_divSchemes_block and not inside_laplacianSchemes_block and not inside_interpolationSchemes_block and not inside_TVD_schemes_block and not inside_NVD_schemes_block and not inside_snGradSchemes_block:
                    updated_lines.append(line)

        if not schemes_found["ddtSchemes"]:
            print("Warning: 'ddtSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\nddtSchemes\n{{\n    default         {selected_ddt_scheme};\n}}\n")

        if not schemes_found["gradSchemes"]:
            print("Warning: 'gradSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\ngradSchemes\n{{\n    default         {selected_grad_scheme};\n}}\n")

        if not schemes_found["divSchemes"]:
            print("Warning: 'divSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\ndivSchemes\n{{\n    default         {selected_divSchemes};\n}}\n")

        if not schemes_found["laplacianSchemes"]:
            print("Warning: 'laplacianSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\nlaplacianSchemes\n{{\n    default         {selected_laplacianSchemes};\n}}\n")
        
        if not schemes_found["interpolationSchemes"]:
            print("Warning: 'interpolationSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\ninterpolationSchemes\n{{\n    default         {selected_interpolationSchemes};\n}}\n")

        if not schemes_found["TVD_schemes"]:
            print("Warning: 'TVD_schemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\nTVD_schemes\n{{\n    default         {selected_TVD_schemes};\n}}\n")

        if not schemes_found["NVD_schemes"]:
            print("Warning: 'NVD_schemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\nNVD_schemes\n{{\n    default         {selected_NVD_schemes};\n}}\n")

        if not schemes_found["snGradSchemes"]:
            print("Warning: 'snGradSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\nsnGradSchemes\n{{\n    default         {selected_snGradSchemes};\n}}\n")



        with open(self.fv_schemes_path, 'w') as file:
            file.writelines(updated_lines)

        self.accept()
