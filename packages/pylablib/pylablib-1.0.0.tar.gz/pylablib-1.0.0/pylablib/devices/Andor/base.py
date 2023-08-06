from ...core.devio import DeviceError

class AndorError(DeviceError):
    """Generic Andor error"""
class AndorTimeoutError(AndorError):
    """Andor timeout error"""
class AndorNotSupportedError(AndorError):
    """Option not supported error"""