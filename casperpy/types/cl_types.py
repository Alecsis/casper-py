import dataclasses
import enum
import typing
import abc

@dataclasses.dataclass
class CL_Type(abc.ABC):
    """
    CL type.
    """
    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        pass