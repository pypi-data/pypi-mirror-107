# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# Pip
from web3 import eth as Eth

# Local
from .predefined_erc20_constants import PredefinedERC20Constants
from web3_erc20 import ERC20

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------- class: PredefinedERC20 ---------------------------------------------------- #

class PredefinedERC20(ERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        costants: PredefinedERC20Constants
    ):
        super().__init__(
            eth=eth,
            address=costants.address,
        )

        self.__costants = costants


    # ---------------------------------------------------- Public methods ---------------------------------------------------- #

    def name(self) -> str:
        return self.__costants.name

    def symbol(self) -> str:
        return self.__costants.symbol

    def decimals(self) -> int:
        return self.__costants.decimals


# -------------------------------------------------------------------------------------------------------------------------------- #