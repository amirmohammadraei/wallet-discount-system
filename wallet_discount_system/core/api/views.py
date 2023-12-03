from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import *
from .serializers import *
from django.shortcuts import get_object_or_404


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            Wallet.objects.create(user=user, balance=0)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletListView(APIView):
    def get(self, request, user_id=None):
        if user_id is not None:
            try:
                wallet = Wallet.objects.get(user__id=user_id)
            except Wallet.DoesNotExist:
                return Response({"error": "User wallet not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = WalletSerializer(wallet)
        else:
            wallets = Wallet.objects.all()
            serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get("user_id")
        amount = request.data.get("amount")
        operation_type = request.data.get("operation_type")

        try:
            user_wallet = Wallet.objects.get(user=user_id)
        except Wallet.DoesNotExist:
            return Response({"error": "User wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        transaction_type = 'increase' if operation_type == 'increase' else 'decrease'

        Transaction.objects.create(user=user_wallet.user, amount=amount, type_of_transaction=transaction_type)

        if operation_type == "increase":
            user_wallet.balance += amount
        elif operation_type == "decrease":
            if user_wallet.balance < amount:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            user_wallet.balance -= amount
        else:
            return Response({"error": "Invalid operation type"}, status=status.HTTP_400_BAD_REQUEST)

        user_wallet.save()

        return Response({"message": "Balance updated successfully"})

class TransactionListView(APIView):
    def get(self, request, user_id=None):
        if user_id is not None:
            transactions = Transaction.objects.filter(user__id=user_id)
        else:
            transactions = Transaction.objects.all()

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class DiscountCodeListView(APIView):
    def get(self, request):
        discount_codes = DiscountCode.objects.all()
        serializer = DiscountCodeSerializer(discount_codes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiscountCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscountUsageView(APIView):
    def get(self, request):
        discount_code = request.query_params.get('code', None)
        user_id = request.query_params.get('user_id', None)

        filter_params = {}
        if discount_code:
            filter_params['discount_code__code'] = discount_code
        if user_id:
            filter_params['user__id'] = user_id

        discount_usages = DiscountUsage.objects.filter(**filter_params)
        serializer = DiscountUsageSerializer(discount_usages, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('user_id')
        code = request.data.get('code')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            discount_code = DiscountCode.objects.get(code=code, count__gt=0)
        except DiscountCode.DoesNotExist:
            return Response({"error": "Discount code not found"}, status=status.HTTP_404_NOT_FOUND)

        discount_usage = DiscountUsage(user=user, discount_code=discount_code)
        discount_usage.save()

        discount_code.count -= 1
        discount_code.save()

        serializer = DiscountUsageSerializer(discount_usage)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
