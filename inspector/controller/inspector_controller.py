# inspector/controller/inspector_controller.py

from model.usd_reader import USDReader
from model.layer_stack import LayerStackModel

class InspectorController:
    def __init__(self, view):
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        self.view.load_btn.clicked.connect(self.load_usd_file)

    def load_usd_file(self):
        dlg = self.view.getOpenFileNameDialog()
        if dlg is None:
            return

        path = dlg

        reader = USDReader(path)
        reader.load()

        layer_stack = LayerStackModel(reader.get_layer_stack())
        tree_data = layer_stack.as_tree()

        self.view.populate_layers(tree_data)
