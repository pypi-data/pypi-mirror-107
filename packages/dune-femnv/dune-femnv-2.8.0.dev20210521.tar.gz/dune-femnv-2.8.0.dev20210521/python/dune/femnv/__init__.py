from . import scheme as scheme
from . import model as model

registry = {}

registry["scheme"] = {"nv" : scheme.nv}
registry["model"] = {"nvelliptic" : model.nvelliptic}
