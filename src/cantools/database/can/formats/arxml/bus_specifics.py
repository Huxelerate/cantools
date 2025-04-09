from typing import NewType


class AutosarBusSpecifics:
    """This class collects the AUTOSAR specific information of a CAN bus

    """
    AutosarBusSpecificsClusterName = NewType('AutosarBusSpecificsClusterName', str)
    def __init__(self, cluster_name: str):
        self._cluster_name = cluster_name

    @property
    def cluster_name(self) -> AutosarBusSpecificsClusterName:
        """The name of the AUTOSAR cluster to which the bus belongs.

        """
        return self._cluster_name

    def __repr__(self) -> str:
        """Return a string representation of the object.

        """
        return f"AutosarBusSpecifics(cluster_name={self._cluster_name})"
