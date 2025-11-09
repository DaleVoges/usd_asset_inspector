# inspector/model/usd_reader.py

from pathlib import Path

class USDReader:
    """
    Thin wrapper around pxr.Usd operations.
    Keeps the controller/view isolated from USD API details.
    """

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def load(self):
        """Load the USD stage."""
        from pxr import Usd
        if not self.filepath.exists():
            raise FileNotFoundError(self.filepath)

        self.stage = Usd.Stage.Open(str(self.filepath))
        return self.stage

    def get_layer_stack(self):
        """
        Iterates through the stage's layer stack and returns a list of dictionaries 
        containing layer metadata and its direct sublayer paths.
        """
        layer_data = []
        
        # Iterate over every Sdf.Layer in the resolved stack
        for layer in self.stage.GetLayerStack():
            
            # Get the sublayer paths directly from the Sdf.Layer object
            sublayer_paths = layer.subLayerPaths 
            
            data = {
                "identifier": layer.identifier,
                "real_path": layer.realPath,
                "is_anonymous": layer.anonymous,
                
                # Sublayer paths for this specific layer
                "sublayer_paths": sublayer_paths, 
                # ------------------------------------
                
                "root_prims": self.get_root_prims(),
                "prim_count": self.get_all_prims()
            }
            layer_data.append(data)
            
        return layer_data

    def get_mata_data(self):
        """Read the files metadata"""

    def get_root_prims(self):
        """Return top-level prims."""
        return [p.GetName() for p in self.stage.GetPseudoRoot().GetChildren()]

    def get_all_prims(self):
        """Return all_prims"""
        return sum(1 for prim in self.stage.Traverse())

    def get_sublayers_and_references(self):
        """Traverse the usd and get all the sublayers and reference files"""

        # Sublayers are authored on the root Sdf.Layer
        root_layer = stage.GetRootLayer()
        
        # Get all sublayer paths
        sublayer_paths = root_layer.subLayerPaths
        
        # References and Payloads are typically authored on the PseudoRoot Prim
        root_prim = stage.GetPseudoRoot()
        
        # Get the spec for the pseudo-root on the current edit target layer
        root_spec = root_layer.GetPrimAtPath(root_prim.GetPath())
        
        # Check if a spec exists (it might not if the root layer only has sublayers)
        if root_spec:
            # Get references (list of Sdf.Reference objects)
            references = root_spec.referenceList.GetAddedOrExplicitItems()
            
            # Get payloads (list of Sdf.Payload objects)
            payloads = root_spec.payloadList.GetAddedOrExplicitItems()
        else:
            # Handle the case where the root layer only points to other layers
            references = []
            payloads = []

        results = {
            "Sublayers": sublayer_paths,
            "References": references,
            "Payloads": payloads
        }
        return results