from django.urls import path
from core.api.views import *

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('wallets/', WalletListView.as_view(), name='wallet-list'),
    path('wallets/<int:user_id>/', WalletListView.as_view(), name='user-wallet-list'),
    path('wallets/update/', WalletListView.as_view(), name='wallet-update'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:user_id>/', TransactionListView.as_view(), name='user-transaction-list'),
    path('discount-codes/', DiscountCodeListView.as_view(), name='discount-code-list'),
    path('discount-codes/create/', DiscountCodeListView.as_view(), name='create-discount-code'),
    path('discount-usage/', DiscountUsageView.as_view(), name='discount-usage'),
]
