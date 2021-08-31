from enum import Enum


class AuthResult(Enum):
    """
    Authentication result

    ## Meaning

        `Success`: valid authentication
        `NoKey`: no authentication key provided
        `WrongKey`: authentication key is not valid
    """
    Success = 0
    NoKey = 1
    WrongKey = 2
