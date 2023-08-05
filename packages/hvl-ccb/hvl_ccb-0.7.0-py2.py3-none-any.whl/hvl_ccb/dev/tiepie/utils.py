#  Copyright (c) 2019-2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""

"""
import logging

from ...utils.typing import Number

from collections import Sequence

from typing import (
    cast,
    Optional,
    Tuple,
    Type,
    Union,
)

logger = logging.getLogger(__name__)


def _validate_number(
    x_name: str,
    x: object,
    limits: Tuple = (None, None),
    number_type: Union[Type[Number], Tuple[Type[Number], ...]] = (int, float),
) -> None:
    """
    Validate if given input `x` is a number of given `number_type` type, with value
    between given `limits[0]` and `limits[1]` (inclusive), if not `None`.

    :param x_name: string name of the validate input, use for the error message
    :param x: an input object to validate as number of given type within given range
    :param limits: [lower, upper] limit, with `None` denoting no limit: [-inf, +inf]
    :param number_type: expected type or tuple of types of a number,
    by default `(int, float)`
    :raises TypeError: when the validated input does not have expected type
    :raises ValueError: when the validated input has correct number type but is not
        within given range
    """
    if limits is None:
        limits = (None, None)
    msg = None
    err_cls: Optional[Type[Exception]] = None
    if not isinstance(number_type, Sequence):
        number_type = (number_type,)
    if not isinstance(x, number_type):
        msg = (
            f"{x_name} = {x} has to be of type "
            f"{' or '.join(nt.__name__ for nt in number_type)}"
        )
        err_cls = TypeError
    elif not (
        (limits[0] is None or cast(Number, x) >= limits[0])
        and (limits[1] is None or cast(Number, x) <= limits[1])
    ):
        if limits[0] is None:
            suffix = f"less or equal than {limits[1]}"
        elif limits[1] is None:
            suffix = f"greater or equal than {limits[0]}"
        else:
            suffix = f"between {limits[0]} and {limits[1]} inclusive"
        msg = f"{x_name} = {x} has to be " + suffix
        err_cls = ValueError
    if err_cls is not None:
        logger.error(msg)
        raise err_cls(msg)


def _validate_bool(x_name: str, x: object) -> None:
    """
    Validate if given input `x` is a `bool`.

    :param x_name: string name of the validate input, use for the error message
    :param x: an input object to validate as boolean
    :raises TypeError: when the validated input does not have boolean type
    """
    if not isinstance(x, bool):
        msg = f"{x_name} = {x} has to of type bool"
        logger.error(msg)
        raise TypeError(msg)


class PublicPropertiesReprMixin:
    """General purpose utility mixin that overwrites object representation to a one
    analogous to `dataclass` instances, but using public properties and their values
    instead of `fields`.
    """

    def _public_properties_gen(self):
        """
        Generator that returns instance's properties names and their values,
        for properties that do not start with `"_"`

        :return: attribute name and value tuples
        """
        for name in dir(self):
            if (
                not name.startswith("_")
                and hasattr(self.__class__, name)
                and isinstance(getattr(self.__class__, name), property)
            ):
                yield name, getattr(self, name)

    def __repr__(self):
        attrs = ", ".join(
            [f"{name}={value!r}" for name, value in self._public_properties_gen()]
        )
        return f"{self.__class__.__qualname__}({attrs})"
