from rest_framework import serializers
from .models import Bank

class BankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ["id","name","bic","country","city","rating","is_active"]

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ["id","name","bic","country","city","rating","is_active",
                  "swift","license_number","site","created_at"]
