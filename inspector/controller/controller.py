from PySide6 import QtCore, QtWidgets
import traceback
from pxr import Usd, UsdGeom, Sdf
from model import layer_stack

class StageLoader(QtCore.QThread):
    """Load USD stage in background to avoid UI blocking."""
    stageLoaded = QtCore.Signal(object)
    error = QtCore.Signal(str)

    def __init__(self, path=None):
        super().__init__()
        self.path = path

    def run(self):
        try:
            stage = Usd.Stage.Open(self.path) if self.path else Usd.Stage.CreateInMemory()
            self.stageLoaded.emit(stage)
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(tb)

class Controller:
    def __init__(self, view=None):
        self.view = view
        self.stage = None
        self.current_stage_path = None

    def open_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, 'Open USD', '', 'USD Files (*.usd *.usda *.usdc)')
        if path:
            self.load_stage(path)

    def reload_file(self):
        if self.current_stage_path:
            self.load_stage(self.current_stage_path)

    def load_stage(self, path=None):
        self.view.update_status('Loading...')
        self.loader = StageLoader(path)
        self.loader.stageLoaded.connect(self.on_stage_loaded)
        self.loader.error.connect(self.on_loader_error)
        self.loader.start()
        self.current_stage_path = path

    def on_loader_error(self, tb):
        self.view.show_error(tb)
        self.view.update_status('Error loading stage')

    def on_stage_loaded(self, stage):
        self.stage = stage
        self.view.update_status('Stage loaded')

        # populate models
        layers = stage.GetUsedLayers()
        self.view.set_layer_data(layers)

        # refs summary (quick pass over stage to find references)
        ref_counts = {}
        for prim in stage.Traverse():
            try:
                if prim.HasAuthoredReferences():
                    refs = prim.GetMetadata('references') or []
                    for r in refs:
                        ref_counts[r.assetPath] = ref_counts.get(r.assetPath, 0) + 1
                # payloads detection
                if prim.HasAuthoredPayloads():
                    pl = prim.GetMetadata('payload')
                    ref_counts[str(pl)] = ref_counts.get(str(pl), 0) + 1
            except Exception:
                continue

        self.view.set_ref_data(ref_counts)

        # prim tree
        self.view.set_prim_data(stage)

        # stats
        total_prims = 0
        total_meshes = 0
        total_polys = 0
        for prim in stage.Traverse():
            total_prims += 1
            try:
                polys = get_poly_count_for_prim(prim)
                if polys > 0:
                    total_meshes += 1
                    total_polys += polys
            except Exception:
                pass
        self.view.set_stats(total_prims, total_meshes, total_polys)

    def on_prim_selected(self, prim_path):
        found = None
        print(prim_path)
        try:
            found = self.stage.GetPrimAtPath(prim_path)
        except Exception:
            found = None

        if not found:
            # If not found, show simple info
            self.view.set_prim_details(prim_path, {"type": "Not found", "composition": "", "attributes": []})
            return

        # info
        details = {
            "type": found.GetTypeName(),
            "composition": self.get_composition_details(found),
            "attributes": self.get_attributes(found)
        }
        self.view.set_prim_details(prim_path, details)

    def get_composition_details(self, prim):
        # Extract composition details for a prim
        comp_lines = []
        try:
            if prim.HasAuthoredReferences():
                refs = prim.GetMetadata('references') or []
                comp_lines.append('References:')
                for r in refs:
                    comp_lines.append('  ' + str(r))
            if prim.HasAuthoredPayloads():
                payload = prim.GetMetadata('payload')
                comp_lines.append('Payload: ' + str(payload))
            spec_stack = prim.GetPrimStack()
            layers = [s.layer for s in spec_stack if getattr(s, 'layer', None)]
            comp_lines.append('Contributing layers:')
            for l in layers:
                comp_lines.append('  ' + getattr(l, 'realPath', getattr(l, 'identifier', str(l))))
        except Exception:
            comp_lines.append('Error reading composition metadata')

        return '\n'.join(comp_lines)

    def get_attributes(self, prim):
        rows = []
        try:
            for attr in prim.GetAttributes():
                name = attr.GetBaseName()
                val = attr.Get()
                rows.append((name, val, 'unknown'))
        except Exception:
            rows.append(('Error', 'Could not query attributes', ''))
        return rows

