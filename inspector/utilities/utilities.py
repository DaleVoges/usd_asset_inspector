"""
This file is for utility functions
"""
from pxr import Usd, UsdGeom, Sdf

def get_poly_count_for_prim(prim):
    """Return polygon count for a prim if it's a Mesh. Uses USD when available, fallback to 0 or mock counts."""
    try:
        mesh = UsdGeom.Mesh(prim)
        if not mesh:
            return 0
        counts = mesh.GetFaceVertexCountsAttr().Get()
        if counts:
            return int(sum(counts))
    except Exception:
        return 0