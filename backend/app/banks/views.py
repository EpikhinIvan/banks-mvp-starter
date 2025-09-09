from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bank
from .serializers import BankListSerializer, BankDetailSerializer
from .filters import BankFilter
from .permissions import IsAdminOrReadOnly
from .export import export_banks_xlsx

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BankFilter
    search_fields = ["name","bic","city","country"]
    ordering_fields = ["name","rating","created_at"]
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list" and not self.request.user.is_authenticated:
            return BankListSerializer
        if self.action in ["retrieve"] and not self.request.user.is_authenticated:
            return BankListSerializer
        return BankDetailSerializer

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        wb_bytes, filename = export_banks_xlsx(self.filter_queryset(self.get_queryset()))
        response = Response(wb_bytes, status=status.HTTP_200_OK)
        response["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
