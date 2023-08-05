# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3.eth import Eth
from eth_account.signers.local import LocalAccount

# Local
from ...core import PredefinedERC20, PredefinedERC20Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: USDC --------------------------------------------------------- #

class USDC(PredefinedERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        account: Optional[LocalAccount] = None
    ):
        super().__init__(
            eth=eth,
            costants=PredefinedERC20Constants(
                address  = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
                name     = 'USD Coin',
                symbol   = 'USDC',
                decimals = 6
            ),
            account=account
        )


# -------------------------------------------------------------------------------------------------------------------------------- #