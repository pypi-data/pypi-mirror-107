# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3 import eth as Eth
from eth_account.signers.local import LocalAccount

# Local
from ...core import PredefinedERC20, PredefinedERC20Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Wbnb --------------------------------------------------------- #

class Wbnb(PredefinedERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        account: Optional[LocalAccount] = None
    ):
        super().__init__(
            eth=eth,
            costants=PredefinedERC20Constants(
                address  = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
                name     = 'Wrapped BNB',
                symbol   = 'WBNB',
                decimals = 18
            ),
            account=account
        )


# -------------------------------------------------------------------------------------------------------------------------------- #