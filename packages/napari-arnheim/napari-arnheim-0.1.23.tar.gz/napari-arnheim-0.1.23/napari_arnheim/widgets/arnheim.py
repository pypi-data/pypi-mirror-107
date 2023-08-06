from napari_arnheim.widgets.dialogs.upload import createDataArrayFromLayer
from napari.layers.base.base import Layer
from napari_arnheim.dialogs.upload import UploadFileDialog
from napari_arnheim.widgets.toolbar import ArnheimToolbar
from napari_arnheim.widgets.helper import Helper
import xarray as xr
from bergen.clients.provider import ProviderBergen, Bergen
from napari.viewer import Viewer
from napari_arnheim.widgets.context.context_aware import ContextAwareWidget
from napari_arnheim.widgets.lists.replist import RepresentationListWidget
from PyQt5.QtWidgets import (QLabel,  QPushButton,
                             QVBoxLayout, QWidget)
from qasync import asyncClose, asyncSlot
import asyncio
from bergen.console import console



class ArnheimWidget(QWidget):

    def __init__(self, *args, bergen_params = {}, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.status = QLabel(self)
        self.status.text = "Arnheim"


        self.default_kwargs = {
            "config_path": "bergen.yaml",
            "force_new_token": True,
        }
        self.default_kwargs.update(bergen_params)

        self._bergen = ProviderBergen(**self.default_kwargs)

        self.user_button = QPushButton("Connect")
        self.user_button.clicked.connect(self.connectBergen)

        self.layout.addWidget(self.user_button)
        self.setLayout(self.layout)



    def buildToolbar(self):
        self.toolbar = ArnheimToolbar(self, base=self)
        return self.toolbar



    @property
    def helper(self) -> Helper:
        if hasattr(self.parent(), "qt_viewer"):
            return Helper(self.parent().qt_viewer.viewer)


    @property
    def viewer(self) -> Viewer:
        if hasattr(self.parent(), "qt_viewer"):
            return self.parent().qt_viewer.viewer


    @property
    def bergen(self) -> Bergen:
        if hasattr(self, "_bergen"):
            assert self._bergen is not None, "Please instatiate correctly"
            return self._bergen


    @asyncClose
    async def closeEvent(self, event):
        await self._bergen.disconnect_async()



    @asyncSlot()
    async def createRepresentationFromCurrent(self, name=None):
        if name == None:
            dialog = UploadFileDialog(layer=self.viewer.active_layer)
            if dialog.exec_():
                name = dialog.name
                return createDataArrayFromLayer(layer=self.viewer.active_layer), name

        else:
            return createDataArrayFromLayer(layer=self.viewer.active_layer), name


    

    @asyncSlot()
    async def connectBergen(self):
        try:
            await self._bergen.negotiate_async()
            self.layout.addWidget(self.buildToolbar())
            user = self._bergen.getUser()
            self.user_button.setText(f"Logout {user.username}")

        except:
            console.print_exception()


    def buildContext(self):
        widget = ContextAwareWidget(base=self)
        return widget

