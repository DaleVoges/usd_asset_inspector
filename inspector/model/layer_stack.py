from PySide6 import QtWidgets, QtGui, QtCore
import os
from utilities import utilities

class LayerStackModel(QtGui.QStandardItemModel):
    """
    Simple model to present a layer stack as a tree. Columns: [Name, Path, Type]
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(['Layer', 'Resolved Path', 'Info'])

    def populate(self, layer_list):
        self.clear()
        self.setHorizontalHeaderLabels(['Layer', 'Resolved Path', 'Info'])
        for layer in layer_list:
            # layer can be Sdf.Layer or a simple string
            if hasattr(layer, 'identifier'):
                name = os.path.basename(layer.identifier)
                path = getattr(layer, 'realPath', layer.identifier)
            else:
                name = os.path.basename(str(layer))
                path = str(layer)
            name_item = QtGui.QStandardItem(name)
            path_item = QtGui.QStandardItem(path)
            info_item = QtGui.QStandardItem('sublayers: {}'.format(len(getattr(layer, 'subLayerPaths', []))))
            self.appendRow([name_item, path_item, info_item])

class PrimTreeModel(QtGui.QStandardItemModel):
    """
        Prim hierarchy model. Columns: [Prim, Type, Polys]
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(['Prim', 'Type', 'Polygons'])

    def populate_from_stage(self, stage):
        self.clear()
        self.setHorizontalHeaderLabels(['Prim', 'Type', 'Polygons'])
        # build tree
        root_item = self.invisibleRootItem()

        # helper to create items for a prim
        def make_row(prim):
            name = str(prim.GetPath().pathString) if hasattr(prim, 'GetPath') else str(prim)
            typeName = prim.GetTypeName() if hasattr(prim, 'GetTypeName') else 'Unknown'
            polys = utilities.get_poly_count_for_prim(prim)
            i1 = QtGui.QStandardItem(os.path.basename(name) or name)
            i1.setData(name, QtCore.Qt.UserRole + 1)  # full path
            i2 = QtGui.QStandardItem(typeName)
            i3 = QtGui.QStandardItem(str(polys))
            return [i1, i2, i3]

        # TODO implement lazy loading.for massive stages
        parents = {}
        for prim in stage.Traverse():
            path = str(prim.GetPath().pathString)
            parts = [p for p in path.split('/') if p != '']
            # find parent item
            parent = root_item
            curr_path = ''
            for idx, part in enumerate(parts):
                curr_path = curr_path + '/' + part
                if curr_path not in parents:
                    # create new row under parent
                    row = make_row(prim if idx == len(parts)-1 else type('P', (), {'GetPath': lambda: type('PP',(),{'pathString':curr_path})(), 'GetTypeName': lambda : 'Xform', 'GetChildren': lambda : []}))
                    parent.appendRow(row)
                    parents[curr_path] = row[0]
                parent = parents[curr_path]

class AttributeTableModel(QtCore.QAbstractTableModel):
    """
        Two-column table: Attribute name, value; optional source layer.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []  # list of (name, value, source)

    def set_attributes(self, rows):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._rows)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 3

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            row = self._rows[index.row()]
            return str(row[index.column()])
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return ['Attribute', 'Value', 'Source'][section]
        return super().headerData(section, orientation, role)







