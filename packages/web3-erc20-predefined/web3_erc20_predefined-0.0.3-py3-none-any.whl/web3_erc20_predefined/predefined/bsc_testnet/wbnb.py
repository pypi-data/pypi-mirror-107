# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3.eth import Eth
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
                address  = '0xae13d989dac2f0debff460ac112a837c89baa7cd',
                name     = 'Wrapped BNB',
                symbol   = 'WBNB',
                decimals = 18
            ),
            account=account
        )


# -------------------------------------------------------------------------------------------------------------------------------- #