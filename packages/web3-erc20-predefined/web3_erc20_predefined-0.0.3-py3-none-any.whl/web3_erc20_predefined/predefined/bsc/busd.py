# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3.eth import Eth
from eth_account.signers.local import LocalAccount

# Local
from ...core import PredefinedERC20, PredefinedERC20Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Busd --------------------------------------------------------- #

class Busd(PredefinedERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        account: Optional[LocalAccount] = None
    ):
        super().__init__(
            eth=eth,
            costants=PredefinedERC20Constants(
                address  = '0xe9e7cea3dedca5984780bafc599bd69add087d56',
                name     = 'BUSD Token',
                symbol   = 'BUSD',
                decimals = 18
            ),
            account=account
        )


# -------------------------------------------------------------------------------------------------------------------------------- #