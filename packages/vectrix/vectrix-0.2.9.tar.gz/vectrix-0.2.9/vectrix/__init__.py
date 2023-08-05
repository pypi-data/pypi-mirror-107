from .main import VectrixUtils
from .assets import Asset
from .events import Event
from .issues import Issue
from .metadata import MetadataElement, MetadataPriority

from vectrix import clients as vectrix_clients

clients = vectrix_clients
vectrix = VectrixUtils()
