import enum


class CarAddition(enum.Enum):
    """
        Defines various car addition actions.
    """
    SELECT = "SELECT"
    DESELECT = "DESELECT"
    ADD = "ADD"
    DELETE = "DELETE"
