from napari_arnheim.widgets.dialogs.upload import createDataArrayFromLayer
from napari_arnheim.forms.text_field import TextField
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, QVBoxLayout
from grunnlag.schema import Representation, RepresentationVariety


class UploadFileDialog(QDialog):


    def __init__(self, *args, layer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = layer
        
        self.representation_name = QLineEdit()

        self.formGroupBox = QGroupBox("New Representation")
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.representation_name)
        self.formGroupBox.setLayout(layout)


        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.create)
        buttonBox.rejected.connect(self.reject)
        

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("Create a new Representation")


    def create(self):
        self.name = self.representation_name.text()

        newarray = createDataArrayFromLayer(self.layer)
        self.accept()