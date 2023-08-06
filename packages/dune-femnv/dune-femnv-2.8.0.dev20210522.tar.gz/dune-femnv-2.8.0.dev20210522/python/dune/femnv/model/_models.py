from dune.fem.model import elliptic
from . patch import transform

def nvelliptic(view, equation, *args, **kwargs):
    VM = 'dune/femnv/schemes/diffusionmodel.hh'
    return elliptic(view, equation, virtualModel=VM, modelPatch=transform, *args, **kwargs)
