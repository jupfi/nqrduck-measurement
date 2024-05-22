"""Signal processing options."""

import logging
import sympy
from nqrduck_spectrometer.measurement import Measurement, Fit, T2StarFit
from nqrduck.helpers.functions import Function, GaussianFunction, CustomFunction
from nqrduck.helpers.formbuilder import (
    DuckFormBuilder,
    DuckFormFunctionSelectionField,
    DuckFormDropdownField,
    DuckLabelField,
)

logger = logging.getLogger(__name__)


class FIDFunction(Function):
    """The exponetial FID function."""

    name = "FID"

    def __init__(self) -> None:
        """Exponential FID function."""
        expr = sympy.sympify("exp( -x / T2star )")
        super().__init__(expr)
        self.start_x = 0
        self.end_x = 30

        self.add_parameter(Function.Parameter("T2star (microseconds)", "T2star", 10))


class LorentzianFunction(Function):
    """The Lorentzian function."""

    name = "Lorentzian"

    def __init__(self) -> None:
        """Lorentzian function."""
        expr = sympy.sympify("1 / (1 + (x / T2star)^2)")
        super().__init__(expr)
        self.start_x = 0
        self.end_x = 30

        self.add_parameter(Function.Parameter("T2star (microseconds)", "T2star", 10))


class Apodization(DuckFormBuilder):
    """Apodization parameter.

    This parameter is used to apply apodization functions to the signal.
    The apodization functions are used to reduce the noise in the signal.
    """

    def __init__(self, measurement: Measurement, parent=None) -> None:
        """Apodization parameter."""
        super().__init__("Apodization", parent=parent)

        self.measurement = measurement
        functions = [
            FIDFunction(),
            GaussianFunction(),
            CustomFunction(),
        ]

        self.duration = (self.measurement.tdx[-1] - self.measurement.tdx[0]) * 1e-6

        function_selection_field = DuckFormFunctionSelectionField(
            text=None,
            tooltip=None,
            functions=functions,
            duration=self.duration,
            parent=parent,
            default_function=0,
        )

        self.add_field(function_selection_field)

    def get_function(self) -> Function:
        """Get the selected function.

        Returns:
            Function: The selected function.
        """
        return self.get_values()[0]


class Fitting(DuckFormBuilder):
    """Fitting parameter.

    This parameter is used to apply fitting functions to the signal.
    The fitting functions are used to reduce the noise in the signal.
    """

    def __init__(self, measurement: Measurement, parent=None) -> None:
        """Fitting parameter."""
        super().__init__("Fitting", parent=parent)

        self.measurement = measurement

        fits = {}
        fits["T2*"] = T2StarFit(self.measurement)

        selection_field = DuckFormDropdownField(
            text=None,
            tooltip=None,
            options=fits,
            default_option=0,
        )

        self.add_field(selection_field)

    def get_fit(self) -> Fit:
        """Get the selected fit.

        Returns:
            Fit: The selected fit.
        """
        return self.get_values()[0]
