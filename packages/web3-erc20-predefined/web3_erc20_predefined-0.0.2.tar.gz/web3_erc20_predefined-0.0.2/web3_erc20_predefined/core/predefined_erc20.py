# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3 import eth as Eth
from eth_account.signers.local import LocalAccount

from web3_erc20 import ERC20

# Local
from .predefined_erc20_constants import PredefinedERC20Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------- class: PredefinedERC20 ---------------------------------------------------- #

class PredefinedERC20(ERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        costants: PredefinedERC20Constants,
        account: Optional[LocalAccount] = None
    ):
        super().__init__(
            eth=eth,
            address=costants.address,
            account=account
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