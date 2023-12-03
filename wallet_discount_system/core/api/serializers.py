from rest_framework import serializers
from core.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user_id', 'user_mobile_number', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user_id', 'user_mobile_number', 'amount', 'type_of_transaction', 'timestamp']

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

class DiscountUsageSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)
    discount_code_id = serializers.IntegerField(source='discount_code.id', read_only=True)
    discount_code_code = serializers.CharField(source='discount_code.code', read_only=True)

    class Meta:
        model = DiscountUsage
        fields = ['id', 'user_id', 'user_mobile_number', 'discount_code_id', 'discount_code_code', 'timestamp']
