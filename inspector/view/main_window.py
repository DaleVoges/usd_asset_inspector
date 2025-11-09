from PySide6 import QtWidgets, QtGui, QtCore

class LayerItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, layer_data):
        super().__init__([
            layer_data.get("name", ""),
            layer_data.get("path", ""),
            layer_data.get("type", ""),
            str(layer_data.get("prim_count", "")),
            str(layer_data.get("ref_count", "")),
            str(layer_data.get("payload_count", "")),
            str(layer_data.get("sublayer_count", "")),
            layer_data.get("status", "")
        ])
        self.layer_data = layer_data

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USD Layer Stack Inspector")
        self.resize(1000, 500)

        # Main layout
        main = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(main)

        # Load button
        self.load_btn = QtWidgets.QPushButton("Load USD File…")
        layout.addWidget(self.load_btn)

        # Tree widget
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(8)
        self.tree.setHeaderLabels([
            "Layer",
            "File Path",
            "Type",
            "Prim Count",
            "Refs",
            "Payloads",
            "Sublayers",
            "Status"
        ])
        self.tree.setIndentation(20)
        layout.addWidget(self.tree)

        self.setCentralWidget(main)

    def populate_layers(self, layer_stack):
        self.tree.clear()

        for layer in layer_stack:
            item = LayerItem(layer)
            self.tree.addTopLevelItem(item)

            # Expandable: Sublayers
            if layer.get("sublayers"):
                sublayer_root = QtWidgets.QTreeWidgetItem(["Sublayers", "", "", "", "", "", "", ""])
                item.addChild(sublayer_root)
                for sub in layer["sublayers"]:
                    sub_item = QtWidgets.QTreeWidgetItem([sub, "", "", "", "", "", "", ""])
                    sublayer_root.addChild(sub_item)

            # Expandable: References
            if layer.get("references"):
                refs_root = QtWidgets.QTreeWidgetItem(["References", "", "", "", "", "", "", ""])
                item.addChild(refs_root)
                for ref in layer["references"]:
                    ref_item = QtWidgets.QTreeWidgetItem([ref, "", "", "", "", "", "", ""])
                    refs_root.addChild(ref_item)

            # Expandable: Payloads
            if layer.get("payloads"):
                payload_root = QtWidgets.QTreeWidgetItem(["Payloads", "", "", "", "", "", "", ""])
                item.addChild(payload_root)
                for pay in layer["payloads"]:
                    pay_item = QtWidgets.QTreeWidgetItem([pay, "", "", "", "", "", "", ""])
                    payload_root.addChild(pay_item)

        self.tree.expandAll()

    def getOpenFileNameDialog(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select USD File", "", "USD Files (*.usd *.usda *.usdc)"
        )
        return filepath or None

# Example mock data
mock_layers = [
    {
        "name": "asset_root.usd",
        "path": "/project/asset_root.usd",
        "type": "usda",
        "prim_count": 1200,
        "ref_count": 2,
        "payload_count": 1,
        "sublayer_count": 3,
        "status": "OK",
        "sublayers": ["asset_geo.usd", "asset_rig.usd", "asset_shaders.usd"],
        "references": ["char_body.usd", "char_clothes.usd"],
        "payloads": ["char_groom.usd"]
    }
]

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.populate_layers(mock_layers)
    win.show()
    app.exec()
