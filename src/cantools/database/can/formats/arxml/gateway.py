# A CAN Gateway
from typing import Dict, List, Set, Tuple

class Gateway:
    """A CAN gateway.

    """

    def __init__(self,
                 name: str,
                 node_ref: str,
                 pdu_triggering_routes: List[Tuple[str, str]]
                 ) -> None:
        self._name = name
        self._node_ref = node_ref
        self._pdu_triggering_routes = pdu_triggering_routes

    @property
    def name(self) -> str:
        """The gateway name as a string.

        """

        return self._name

    @property
    def node_ref(self) -> str:
        """The node ref name as a string.

        """

        return self._node_ref
    
    @staticmethod
    def get_pdu_triggering_routes(gateways: List["Gateway"]) -> Dict[str, Tuple[str, List[str]]]:
        """
        Given a list of gateways, return a dictionary storing for each 
        pdu triggering path its source pdu triggering path and the list of gateways
        traversed in the route
        """
        target_to_source: Dict[str, Tuple[str, str]] = {}
        for gateway in gateways:
            for source, target in gateway._pdu_triggering_routes:
                # NOTE: if multiple sources can lead to the same target
                # we take the lexicographically smaller source pair
                source_pair = (source, gateway.name)
                if target_to_source.get(target, source_pair) <= source_pair:
                    target_to_source[target] = source_pair
        
        targets = target_to_source.keys()
        result: Dict[str, Tuple[str, List[str]]] = {}
        
        for target in targets:
            gateways_path: List[str] = []
            seen_sources: Set[str] = set([target])
            
            source = None
            prev_source_pair = target_to_source.get(target, None)

            while prev_source_pair is not None:
                source, gateway = prev_source_pair
                if source in seen_sources:
                    # loop detected: stop resolution and do not store any route
                    source = None
                    break
                else:
                    seen_sources.add(source)
                    gateways_path.append(gateway)
                    prev_source_pair = target_to_source.get(source, None)

            if source is not None:
                gateways_path.reverse()
                result[target] = (source, gateways_path)

        return result


    