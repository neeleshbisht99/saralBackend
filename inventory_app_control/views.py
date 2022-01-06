from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import OrderSerializer, FoodItemSerializer
from .models import Order, FoodItem
from rest_framework.decorators import action


class FoodItemViewSet(GenericViewSet):
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()

    def get_order_queryset(self, queryset):
        orderby = self.request.query_params.get('orderby', None)
        if orderby:
            order_key = None
            is_desc = orderby[0] == '-'

            if 'created_at' in orderby:
                order_key = '-created_at' if is_desc else 'created_at'
            elif 'updated_at' in orderby:
                order_key = '-updated_at' if is_desc else 'updated_at'

            if order_key:
                queryset = queryset.order_by(order_key)
        return queryset

    def get_queryset(self, ):
        queryset = FoodItem.objects.values(
            'id',
            'name',
            'pricePerUnit',
            'smallestUnit',
            'updated_at',
            'created_at',
            # created_by_name=F('created_by__name')
        )
        queryset = self.get_order_queryset(queryset)
        return queryset

    @action(
        methods=['get'],
        detail=False,
        url_path='fetchall')
    def food_item_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.serializer_class
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=False,
        url_path='create')
    def food_item_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            item = serializer.save()
            return Response(self.serializer_class(item, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_order_queryset(self, queryset):
        orderby = self.request.query_params.get('orderby', None)
        if orderby:
            order_key = None
            is_desc = orderby[0] == '-'

            if 'created_at' in orderby:
                order_key = '-created_at' if is_desc else 'created_at'
            elif 'updated_at' in orderby:
                order_key = '-updated_at' if is_desc else 'updated_at'

            if order_key:
                queryset = queryset.order_by(order_key)
        return queryset

    def get_queryset(self,):
        queryset = Order.objects.select_related(
            'customer').prefetch_related(
            'order_order_items').values(
            'id',
            'order_status',
            'payment_status',
            'table',
            'updated_at',
            'created_at',
            customer_name=F('customer__name'),
            customer_phone=F('customer__phone'))
        queryset = self.get_order_queryset(queryset)
        return queryset

    @action(
        methods=['get'],
        detail=False,
        url_path='fetchall')
    def feeder_analysis_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.serializer_class
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

