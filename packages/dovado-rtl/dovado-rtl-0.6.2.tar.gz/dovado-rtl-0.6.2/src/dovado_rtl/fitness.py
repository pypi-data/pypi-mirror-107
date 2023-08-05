from dovado_rtl.point_evaluation import DesignPointEvaluator
from typing import Tuple, List, Union, Dict

from dovado_rtl.abstract_classes import AbstractFitnessEvaluator
from movado import approximate

to_approximate: bool = False
estimator: str = "HoeffdingAdaptiveTree"
controller: str = "Distance"
keyword_args: Dict[str, Union[int, float, str]] = {}


class FitnessEvaluator(AbstractFitnessEvaluator):
    def __init__(
        self,
        evaluator: DesignPointEvaluator,
        approx: bool = False,
        control: str = "Distance",
        estim: str = "HoeffdingAdaptiveTree",
        **kwargs
    ):
        global to_approximate
        global estimator
        global controller
        global keyword_args

        self.__evaluator: DesignPointEvaluator = evaluator
        to_approximate = approx
        estimator = estim
        controller = control
        keyword_args = kwargs

    @approximate(
        disabled=to_approximate,
        estimator=estimator,
        controller=controller,
        controller_debug=True,
    )
    def fitness(self, design_point: List[int]) -> List[float]:
        return list(
            self.__evaluator.evaluate(tuple(design_point)).value.values()
        )
