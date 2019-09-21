class Event:
    """
    A superclass for any events that might be generated by an
    object and sent to the EventManager.
    """
    _name: str

    def __init__(self) -> None:
        self._name = "Generic event"

    def __str__(self) -> str:
        return self._name
