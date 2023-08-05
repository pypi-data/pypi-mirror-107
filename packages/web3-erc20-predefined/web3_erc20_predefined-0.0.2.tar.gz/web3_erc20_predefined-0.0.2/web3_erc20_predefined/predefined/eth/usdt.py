# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3 import eth as Eth
from eth_account.signers.local import LocalAccount

# Local
from ...core import PredefinedERC20, PredefinedERC20Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: USDT --------------------------------------------------------- #

class USDT(PredefinedERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        account: Optional[LocalAccount] = None
    ):
        super().__init__(
            eth=eth,
            costants=PredefinedERC20Constants(
                address  = '0xdac17f958d2ee523a2206206994597c13d831ec7',
                name     = 'Tether USD',
                symbol   = 'USDT',
                decimals = 6
            ),
            account=account
        )


# -------------------------------------------------------------------------------------------------------------------------------- #