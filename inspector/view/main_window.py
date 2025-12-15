from PySide6 import QtCore, QtGui, QtWidgets
from model import layer_stack

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle('USD Inspector')
        self.resize(1200, 800)

        # Store the controller reference
        self.controller = controller
        self.controller.view = self

        # Central widget split into three
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        h = QtWidgets.QHBoxLayout(central)
        h.setContentsMargins(6, 6, 6, 6)

        # LEFT: Tabs
        self.left_tabs = QtWidgets.QTabWidget()
        self.left_tabs.setMinimumWidth(280)
        h.addWidget(self.left_tabs)

        # Layer stack tab
        self.layer_view = QtWidgets.QTreeView()
        self.layer_model = layer_stack.LayerStackModel(self)
        self.layer_view.setModel(self.layer_model)
        self.left_tabs.addTab(self.layer_view, 'Layers')

        # External refs tab
        self.ref_list = QtWidgets.QTreeView()
        self.ref_model = QtGui.QStandardItemModel()
        self.ref_model.setHorizontalHeaderLabels(['Reference', 'Count'])
        self.ref_list.setModel(self.ref_model)
        self.left_tabs.addTab(self.ref_list, 'External Refs')

        # Stats tab
        self.stats_widget = QtWidgets.QWidget()
        sv = QtWidgets.QVBoxLayout(self.stats_widget)
        self.stats_text = QtWidgets.QTextBrowser()
        sv.addWidget(self.stats_text)
        self.left_tabs.addTab(self.stats_widget, 'Stats')

        # CENTER: Prim tree
        self.prim_tree = QtWidgets.QTreeView()
        self.prim_model = layer_stack.PrimTreeModel(self)
        self.prim_tree.setModel(self.prim_model)
        self.prim_tree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        h.addWidget(self.prim_tree, 1)

        # RIGHT: Prim details
        right = QtWidgets.QWidget()
        right.setMinimumWidth(360)
        rv = QtWidgets.QVBoxLayout(right)
        h.addWidget(right)

        # Info labels
        self.info_label = QtWidgets.QLabel('Select a prim to see details')
        rv.addWidget(self.info_label)

        # Composition info
        self.comp_text = QtWidgets.QTextEdit()
        self.comp_text.setReadOnly(True)
        self.comp_text.setMaximumHeight(150)
        rv.addWidget(self.comp_text)

        # Attribute table
        self.attr_table = QtWidgets.QTableView()
        self.attr_model = layer_stack.AttributeTableModel(self)
        self.attr_table.setModel(self.attr_model)
        rv.addWidget(self.attr_table, 1)

        # Status bar
        self.status = self.statusBar()
        self.status.showMessage('Ready')

        # Connections
        self.prim_tree.selectionModel().selectionChanged.connect(self.on_prim_selected)

        # toolbar
        toolbar = self.addToolBar('Main')
        load_act = QtGui.QAction('Open', self)
        load_act.triggered.connect(self.controller.open_file)
        toolbar.addAction(load_act)
        reload_act = QtGui.QAction('Reload', self)
        reload_act.triggered.connect(self.controller.reload_file)
        toolbar.addAction(reload_act)

    def on_prim_selected(self, selected, _deselected):
        # This would call the controller to handle selection
        indexes = selected.indexes()
        if not indexes:
            return
        idx = indexes[0]
        item = self.prim_model.itemFromIndex(idx)
        if not item:
            return
        prim_path = item.data(QtCore.Qt.UserRole + 1)
        self.controller.on_prim_selected(prim_path)  # Pass selection to the controller

    def update_status(self, message):
        self.status.showMessage(message)

    def set_layer_data(self, layers):
        self.layer_model.populate(layers)

    def set_ref_data(self, ref_counts):
        self.ref_model.clear()
        self.ref_model.setHorizontalHeaderLabels(['Reference', 'Count'])
        for k, v in sorted(ref_counts.items(), key=lambda t: -t[1]):
            it1 = QtGui.QStandardItem(str(k))
            it2 = QtGui.QStandardItem(str(v))
            self.ref_model.appendRow([it1, it2])

    def set_prim_data(self, prim_data):
        self.prim_model.populate_from_stage(prim_data)

    def set_stats(self, total_prims, total_meshes, total_polys):
        stats = f"Total prims: {total_prims}\nTotal meshes: {total_meshes}\nTotal polygons: {total_polys}\n"
        self.stats_text.setPlainText(stats)

    def set_prim_details(self, prim_path, details):
        self.info_label.setText(f'Path: {prim_path}\nType: {details["type"]}')
        self.comp_text.setPlainText(details["composition"])
        self.attr_model.set_attributes(details["attributes"])

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self, 'Load Error', message)
