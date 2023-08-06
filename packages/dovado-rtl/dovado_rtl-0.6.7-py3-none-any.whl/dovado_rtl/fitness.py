from dovado_rtl.point_evaluation import DesignPointEvaluator
from typing import List, Union, Dict, Optional

from dovado_rtl.abstract_classes import AbstractFitnessEvaluator
from movado import approximate


class FitnessEvaluator(AbstractFitnessEvaluator):
    def __init__(
        self,
        evaluator: DesignPointEvaluator,
        approx: bool = False,
        control: str = "Distance",
        estim: str = "HoeffdingAdaptiveTree",
    ):

        self.__evaluator: DesignPointEvaluator = evaluator
        self.fitness = approximate(
            disabled=approx,
            outputs=len(self.__evaluator.get_metrics()),
            estimator=estim,
            controller=control,
            controller_debug=True,
        )(self.fitness)

    def fitness(self, design_point: List[int]) -> List[float]:
        return list(
            self.__evaluator.evaluate(tuple(design_point)).value.values()
        )
