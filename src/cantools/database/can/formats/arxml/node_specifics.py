class AutosarNodeSpecifics:
    """This class collects the AUTOSAR specific information of node that
    is attached to a CAN bus

    AUTOSAR calls such nodes "ECU instances"...
    """
    def __init__(self, ref: str):
        self._ref = ref
    
    @property
    def ref(self) -> str:
        return self._ref
