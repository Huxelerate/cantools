from typing import List, NewType

class AutosarCommConnector:
    def __init__(self, name: str, ref: str, node_ref: str):
        self._name = name
        self._ref = ref
        self._node_ref = node_ref
    
    @property
    def name(self):
        return self._name

    @property
    def ref(self):
        return self._ref
    
    @property
    def node_ref(self):
        return self._node_ref

class AutosarBusSpecifics:
    """This class collects the AUTOSAR specific information of a CAN bus

    """
    AutosarBusSpecificsClusterName = NewType('AutosarBusSpecificsClusterName', str)
    def __init__(self, cluster_name: str, comm_connectors: List[AutosarCommConnector]):
        self._cluster_name = cluster_name
        self._comm_connectors = comm_connectors

    @property
    def cluster_name(self) -> AutosarBusSpecificsClusterName:
        """The name of the AUTOSAR cluster to which the bus belongs.

        """
        return self._cluster_name
    
    @property
    def comm_connectors(self) -> List[AutosarCommConnector]:
        """The communication connectors attached to this bus.

        """
        return self._comm_connectors

    def __repr__(self) -> str:
        """Return a string representation of the object.

        """
        return f"AutosarBusSpecifics(cluster_name={self._cluster_name})"
