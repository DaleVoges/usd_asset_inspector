# inspector/model/layer_stack.py

class LayerStackModel:
    """
    Pure data structure representing the layer stack.
    Useful for testing without USD.
    """

    def __init__(self, layers):
        self.layers = layers

    def as_tree(self):
        """
        Convert list into hierarchical data suitable for the View.
        Currently flat; extend later if needed.
        """
        return [{"name": layer["identifier"], "data": layer} for layer in self.layers]
