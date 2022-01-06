from django.db import models
from user_control.views import add_user_activity
from user_control.models import (CustomUser, )
# Create your models here.


class FoodItem(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    pricePerUnit = models.IntegerField()
    smallestUnit = models.CharField(max_length=100,)
    created_by = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name="food_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-name", )

    def delete(self, *args, **kwargs):
        action = f"deleted item - '{self.name}'"
        super.delete(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)

    class Meta:
        ordering = ("-name", )

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    table = models.CharField(max_length=10)
    payment_status = models.BooleanField()
    order_status = models.BooleanField()

    class Meta:
        ordering = ("-updated_at", )

    def __str__(self):
        return self.name


class OrderItems(models.Model):
    food_item = models.ForeignKey(FoodItem, null=False, on_delete=models.CASCADE, related_name="food_items_order_items")
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, related_name="order_order_items")
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "-created_at", )

    def save(self, *args, **kwargs):
        self.total_price = self.food_item.pricePerUnit * self.quantity
        super.save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_item.name} ordered on {self.updated_at}"



#
# class FeederAnalysisViewSet(GenericViewSet):
#     serializer_class = FeederAnalysisListNewSerializer
#     queryset = FeederAnalysis.objects.filter(feeder__is_active=True).all()
#     filter_backends = (drf_filters.DjangoFilterBackend,)
#     filter_class = FeederAnalysisFilter
#
#     def get_order_queryset(self, queryset):
#         orderby = self.request.query_params.get('orderby', None)
#         if orderby:
#             order_key = None
#             is_desc = orderby[0] == '-'
#
#             if 'feeder' in orderby:
#                 order_key = '-feeder__title' if is_desc else 'feeder__title'
#             if order_key:
#                 queryset = queryset.order_by(order_key)
#         return queryset
#
#     def get_queryset(self, is_subtransmission):
#         queryset = FeederAnalysis.objects.filter(
#             feeder__is_active=True,
#             feeder__is_subtransmission=is_subtransmission).prefetch_related(
#             'feeder').prefetch_related(
#             'feeder__region').prefetch_related(
#             'feeder__subregion').prefetch_related(
#             'feeder_task').values(
#             'id',
#             'predicted_next_trim_year',
#             'predicted_trim_cycle',
#             'criticality_score',
#             'cost',
#             'actual_cost',
#             'aci',
#             'approved_trim_year',
#             'approved_trim_cycle',
#             'percent_critical_overhead_linemile',
#             feeder_idx=F('feeder__id'),
#             feeder_name=F('feeder__title'),
#             region=F('feeder__region__title'),
#             subregion=F('feeder__subregion__title'),
#             last_trim_year=F('feeder__last_trim_year'),
#             color_code=F('feeder__color_code'),
#             overhead_linemile=F('feeder__overhead_linemile'),
#             last_trim_date=F('feeder__last_trim_date'),
#             percent_no_veg=F('feeder__percent_no_veg'),
#             is_problem_feeder=F('feeder__is_problem_feeder'),
#             total_effort_index=F('feeder__total_effort_index'))
#         queryset = self.get_order_queryset(queryset)
#         return queryset
#
#     def get_map_queryset(self, is_subtransmission):
#         queryset = FeederAnalysis.objects.filter(
#             feeder__is_active=True,
#             feeder__is_subtransmission=is_subtransmission).select_related(
#             'feeder').values(
#             'id',
#             'criticality_score',
#             'approved_trim_year',
#             'feeder_id',
#             centroid=F('feeder__centroid'),
#             overhead_linemile=F('feeder__overhead_linemile'),
#             feeder_name=F('feeder__title'), )
#         return queryset
#
#     @swagger_auto_schema(
#         responses={200: FeederAnalysisListNewSerializer(many=True)})
#     @action(
#         methods=['get'],
#         detail=False,
#         url_path='fetchall',
#         renderer_classes=[CustomJSONRenderer])
#     def feeder_analysis_list(self, request, *args, **kwargs):
#         self.pagination_class = AggregatedLimitOffsetPagination
#
#         status = self.request.query_params.get('status', None)
#         viewtype = self.request.query_params.get('viewtype', None)
#         is_subtransmission = self.request.query_params.get('is_subtransmission', False)
#         is_subtransmission = str_to_boolean(is_subtransmission)
#
#         if viewtype == 'map':
#             serializer_class = FeederAnalysisMapListSerializer
#             queryset_without_status = self.filter_queryset(self.get_map_queryset(is_subtransmission))
#         else:
#             serializer_class = FeederAnalysisListNewSerializer
#             queryset_without_status = self.filter_queryset(self.get_queryset(is_subtransmission))
#
#         queryset_without_status = auth_filter_analysis_list(request.user, queryset_without_status, NetworkType.FEEDER)
#         queryset = queryset_without_status
#         if status is not None:
#             queryset = queryset.filter(status__title=status)
#
#         queryset.count_queryset = queryset_without_status
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             if viewtype not in ('map', 'list'):
#                 analysis_ids = []
#                 analysis_task_map = defaultdict(list)
#                 for record in page:
#                     analysis_ids.append(record['id'])
#
#                 all_tasks = Task.objects.filter(
#                     feeder_id__in=analysis_ids).values(
#                     'id',
#                     'feeder_id',
#                     'completed_linemiles',
#                     'planned_trim_year',
#                     status_title=F('status__title'))
#                 for record in all_tasks:
#                     analysis_task_map[record['feeder_id']].append(record)
#
#                 # Map tasks to result
#                 for record in page:
#                     if record['id'] in analysis_task_map:
#                         record['tasks'] = analysis_task_map[record['id']]
#                     else:
#                         record['tasks'] = []
#
#             serializer = serializer_class(page, many=True, context={'request': request})
#             return self.get_paginated_response(serializer.data)
#
#         serializer = serializer_class(queryset, many=True)
#         return Response(serializer.data)