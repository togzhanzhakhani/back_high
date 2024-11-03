from django.urls import path
from .views import ReadWithQuorumView, LatestItemView, UpdateItemView, UpdateWithQuorumView

urlpatterns = [
    path('read_with_quorum/<int:item_id>/', ReadWithQuorumView.as_view(), name='read_with_quorum'),
    path('get_latest_item/<int:item_id>/', LatestItemView.as_view(), name='get_latest_item'),
    path('update_item/<int:item_id>/', UpdateItemView.as_view(), name='update_item'),
    path('update_with_quorum/<int:item_id>/', UpdateWithQuorumView.as_view(), name='update_with_quorum'),
]