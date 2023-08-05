# ------------------------------------------------ class: PredefinedERC20Constants ----------------------------------------------- #

class PredefinedERC20Constants:

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        address:  str,
        name:     str,
        symbol:   str,
        decimals: int
    ):
        self.address  = address
        self.name     = name
        self.symbol   = symbol
        self.decimals = decimals


# -------------------------------------------------------------------------------------------------------------------------------- #