from fastapi import APIRouter, Depends,HTTPException, status
from uuid import UUID
from .service import TransactionService  # Adjust import as needed
from tradify.db import session_factory

from .schema import TransactionTrade, TransactionFund, TransactionWithdraw
router = APIRouter(prefix='/transactions', tags=['Transactions'])

def get_transaction_service() -> TransactionService:
    return TransactionService(session_factory)

@router.get('/{user_id}')
def get_all_transactions(
    user_id: UUID,
    service: TransactionService = Depends(get_transaction_service)
):
    transactions = service.get_all_user_transactions(user_id)
    if transactions:
        return {"success": True, "transactions": transactions}
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No transactions found for this user."
        )



@router.post('/fund')
def fund(
    data: TransactionFund,
    service: TransactionService = Depends(get_transaction_service)
):
    result = service.fund(data.user_id, data.amount)
    if isinstance(result, dict) and result.get("success"):
        return result
    
    if not isinstance(result, dict):
        result = {'result': result}
    raise HTTPException(status_code=400, detail={'message':"Funding failed.", **result})

@router.post('/withdraw')
def withdraw(
    data: TransactionWithdraw,
    service: TransactionService = Depends(get_transaction_service)
):
    result = service.withdraw(data.user_id, data.currency_code, data.amount)
    if isinstance(result, dict) and result.get("success"):
        return result
    
    if not isinstance(result, dict):
        result = {'result': result}
    raise HTTPException(status_code=400, detail={'message': "Withdrawal failed.", **result})

@router.post('/trade')
def trade(
    data: TransactionTrade,
    service: TransactionService = Depends(get_transaction_service)
):
    result = service.trade(data.user_id, data.from_code, data.to_code, data.amount)
    if isinstance(result, dict) and result.get("success"):
        return result
    
    if not isinstance(result, dict):
        result = {'result': result}
    raise HTTPException(status_code=400, detail={'message':"Trade failed.", **result})