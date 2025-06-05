from pydantic import BaseModel



class WalletFund(BaseModel):
    amount: float
    currency_code: str


class WalletTrade(BaseModel):
    target_currency_code: str
    amount: float



class WalletConvert(WalletTrade):
    from_currency_code: str


    
