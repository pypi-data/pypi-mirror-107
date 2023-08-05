# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from web3.eth import Eth
from eth_account.signers.local import LocalAccount

# Local
from ...core import PredefinedERC20, PredefinedERC20Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Weth --------------------------------------------------------- #

class Weth(PredefinedERC20):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        account: Optional[LocalAccount] = None
    ):
        super().__init__(
            eth=eth,
            costants=PredefinedERC20Constants(
                address  = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                name     = 'Wrapped Ether',
                symbol   = 'WETH',
                decimals = 18
            ),
            account=account
        )


# -------------------------------------------------------------------------------------------------------------------------------- #