"""
Hall measurement.

Induced voltage perpendicular to both current and magnetic field.
"""


import numpy as np
import pandas as pd

from scipy.constants import e as elementary_charge

from physicslab.electricity import carrier_concentration, Mobility, Resistance
from physicslab.utility import _ColumnsBase


def process(data, thickness=None, sheet_resistance=None):
    """ Bundle method.

    Parameter :attr:`data` must include voltage, current and magnetic field.
    See :class:`Columns` for details and column names.

    The optional parameters allows to calculate additional quantities:
    `concentration` and `mobility`.

    :param data: Measured data
    :type data: pandas.DataFrame
    :param thickness: Sample dimension perpendicular to the plane marked
        by the electrical contacts, defaults to None
    :type thickness: float, optional
    :param sheet_resistance: Defaults to None
    :type sheet_resistance: float, optional
    :return: Derived quantities listed in :meth:`Columns.output`.
    :rtype: pandas.Series
    """
    measurement = Measurement(data)
    (concentration, mobility) = [np.nan] * 2

    sheet_density, conductivity_type, residual = measurement.analyze()
    if thickness is not None:
        concentration = carrier_concentration(sheet_density, thickness)
    if sheet_resistance is not None:
        mobility = Mobility.from_sheets(sheet_density, sheet_resistance)

    return pd.Series(
        data=(sheet_density, conductivity_type, residual,
              concentration, mobility),
        index=Columns.output())


class Columns(_ColumnsBase):
    """ Bases: :class:`physicslab.utility._ColumnsBase`

    Column names.
    """
    MAGNETICFIELD = 'B'
    HALLVOLTAGE = 'VH'
    CURRENT = 'I'
    SHEET_DENSITY = 'sheet_density'
    CONDUCTIVITY_TYPE = 'conductivity_type'
    RESIDUAL = 'residual'
    CONCENTRATION = 'concentration'
    MOBILITY = 'mobility'

    @classmethod
    def mandatory(cls):
        """ Get the current mandatory column names.

        :rtype: set(str)
        """
        return {cls.MAGNETICFIELD, cls.HALLVOLTAGE, cls.CURRENT}

    @classmethod
    def output(cls):
        """ Get the current values of the :func:`process` output column names.

        :rtype: lits(str)
        """
        return [cls.SHEET_DENSITY, cls.CONDUCTIVITY_TYPE, cls.RESIDUAL,
                cls.CONCENTRATION, cls.MOBILITY]


class Measurement:
    """ Hall measurement.

    :param pandas.DataFrame data: Voltage-current-magnetic field triples.
    :raises ValueError: If :attr:`data` is missing a mandatory column
    """

    def __init__(self, data):
        if not Columns.mandatory().issubset(data.columns):
            raise ValueError('Missing mandatory column. See Columns class.')
        self.data = data

    def is_valid(self):
        # Is hall measurement linear enough?
        raise NotImplementedError()

    @staticmethod
    def _conductivity_type(hall_voltage):
        """ Find conductivity type based on sign of hall voltage.

        :param float hall_voltage: Hall voltage
        :return: Either "p" or "n"
        :rtype: str
        """
        if hall_voltage > 0:
            return 'p'
        else:
            return 'n'

    def analyze(self):
        """ Compute sheet density and determine conductivity type.

        :return: Sheet density, conductivity type, fit residual
        :rtype: tuple(float, str, float)
        """
        self.data['hall_resistance'] = Resistance.from_ohms_law(
            self.data[Columns.HALLVOLTAGE], self.data[Columns.CURRENT])
        coefficients_full = np.polynomial.polynomial.polyfit(
            self.data['hall_resistance'], self.data[Columns.MAGNETICFIELD],
            deg=1, full=True)
        slope = coefficients_full[0][1]  # Constant can be found at [0][0].
        fit_residual = coefficients_full[1][0][0]

        signed_sheet_density = slope / -elementary_charge
        sheet_density = abs(signed_sheet_density)
        conductivity_type = self._conductivity_type(signed_sheet_density)
        return sheet_density, conductivity_type, fit_residual
