from fastapi import APIRouter, Depends,HTTPException, status
from uuid import UUID
from .service import WalletService  # Adjust import as needed
from tradify.db import session_factory

router = APIRouter(prefix='/wallet', tags=['Wallets'])

def get_wallet_service() -> WalletService:

    return WalletService(session_factory)

@router.get('/{user_id}')
def get_wallet(
    user_id: UUID,
    service: WalletService = Depends(get_wallet_service)
):
    result : dict = service.get_wallet(user_id)
    if  isinstance(result, dict) and result.get('success') == True:
        return result
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message':"Wllet fetch failed", **result}
        )
