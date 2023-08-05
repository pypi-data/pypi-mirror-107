# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3.eth import Eth
from eth_account.signers.local import LocalAccount

# Local
from ...core import PredefinedERC20, PredefinedERC20Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Dai ---------------------------------------------------------- #

class Dai(PredefinedERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        account: Optional[LocalAccount] = None
    ):
        super().__init__(
            eth=eth,
            costants=PredefinedERC20Constants(
                address  = '0x6b175474e89094c44da98b954eedeac495271d0f',
                name     = 'Dai Stablecoin',
                symbol   = 'DAI',
                decimals = 18
            ),
            account=account
        )


# -------------------------------------------------------------------------------------------------------------------------------- #