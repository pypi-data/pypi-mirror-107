# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import List, Optional

# Pip
from web3 import Web3
from web3.eth import Eth

from web3.contract import ContractFunction, ContractFunctions, Contract as EthContract
from eth_account.signers.local import LocalAccount

# -------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------- class: WrappedContract ---------------------------------------------------- #

class WrappedContract:

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        eth: Eth,
        address: str,
        abi: List[dict],
        account: Optional[LocalAccount] = None
    ):
        self.__eth = eth
        self.__address = address
        self.__abi = abi

        self.__contract = eth.contract(
            address=Web3.toChecksumAddress(address),
            abi=abi
        )

        self._account = account


    # --------------------------------------------------- Public properties -------------------------------------------------- #

    @property
    def eth(self) -> Eth:
        return self.__eth

    @property
    def address(self) -> str:
        return self.__address

    @property
    def abi(self) -> str:
        return self.__abi

    @property
    def contract(self) -> EthContract:
        return self.__contract

    @property
    def functions(self) -> ContractFunctions:
        return self.__contract.functions
    
    def send_transaction(
        self,
        function: ContractFunction,
        wei: Optional[int] = None,
        account: Optional[LocalAccount] = None
    ) -> str:
        account = account or self._account

        if not account:
            raise('No account to call transaction function with.')

        transaction_data = {
            'nonce': self.eth.getTransactionCount(account.address)
        }

        if wei:
            transaction_data['value'] = wei

        txn = function.buildTransaction(transaction_data)
        signed_txn = account.sign_transaction(txn)        

        return self.eth.sendRawTransaction(signed_txn.rawTransaction).hex()


# -------------------------------------------------------------------------------------------------------------------------------- #