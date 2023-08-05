from rb.complexity.complexity_index import ComplexityIndex
from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.complexity.index_category import IndexCategory
from rb.complexity.measure_function import MeasureFunction
from rb.core.text_element_type import TextElementType   
from typing import List, Callable
from rb.similarity.vector_model import VectorModel
from rb.cna.cna_graph import CnaGraph
from rb.cna.edge_type import EdgeType

from rb.utils.rblogger import Logger

logger = Logger.get_logger()


class IntraCohesion(ComplexityIndex):

    """IntraCohesion between elements element_type"""
    def __init__(self, lang: Lang, element_type: TextElementType,
            reduce_depth: int, reduce_function: MeasureFunction, cna_graph: CnaGraph):
        ComplexityIndex.__init__(self, lang=lang, category=IndexCategory.COHESION,
                                 reduce_depth=reduce_depth, reduce_function=reduce_function,
                                 abbr="IntraCoh")
        self.element_type = element_type
        self.cna_graph = cna_graph    
        if element_type.value > reduce_depth:
            logger.error('For index {} element_type has to be lower or equal than reduce_depth'.format(self))

    def process(self, element: TextElement) -> float:
        values = self.compute_above(element)
        return self.reduce_function(values) if len(values) > 0 else ComplexityIndex.IDENTITY

    def compute_below(self, element: TextElement) -> List[float]:
        if element.depth == self.element_type.value:
            sim_values = []
            part_of_edges = self.cna_graph.edges(node=element, edge_type=EdgeType.PART_OF, vector_model=None)
            for edge in part_of_edges:
                sim_edge = self.cna_graph.edges(node=(edge[0], edge[1]), edge_type=EdgeType.SEMANTIC, vector_model=None)
                if len(sim_edge) > 0 and len(sim_edge[0]) >= 3:
                    sim_values.append(sim_edge[0][2])
            return sim_values
        elif element.depth <= self.reduce_depth:
            res = []
            for child in element.components:
                res += self.compute_below(child)
            return res

    def compute_above(self, element: TextElement) -> List[float]:
        if element.depth > self.reduce_depth:
            values = []
            for child in element.components:
                values += self.compute_above(child)
            element.indices[self] = self.reduce_function(values) if len(values) > 0 else ComplexityIndex.IDENTITY
        elif element.depth == self.reduce_depth:
            v = self.compute_below(element)
            if len(v) != 0:
                values = [sum(v) / len(v)]
                element.indices[self] = sum(v) / len(v)
            else:
                values = []
                element.indices[self] = ComplexityIndex.IDENTITY
        else:
            logger.error('wrong reduce depth value.')
        return values
    
    def __repr__(self):
        return self.reduce_function_abbr + self.reduce_depth_abbr + self.abbr + '_' + self.element_type.name