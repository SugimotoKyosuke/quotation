from django.contrib import admin
from django.urls import path
from base import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from base.views import UserLoginView, UserLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/',UserLoginView.as_view(),name='login',),
    path('logout/',UserLogoutView.as_view(),name='logout',),

    path('projects/', views.IndexListView.as_view(), name='project_index'), #案件一覧
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'), #案件登録
    path('projects/<str:pk>/', views.ProjectDetailView.as_view(), name='project_detail'), #案件詳細
    path('projects/<str:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'), #案件編集

    path('cost-estimates/',views.CostEstimateListView.as_view(),name='cost_estimate_index'), #原価一覧
    path('cost-estimates/create/',views.CostEstimateCreateView.as_view(),name='cost_estimate_create'), #原価登録
    path('cost-estimates/<str:pk>/',views.CostEstimateDetailView.as_view(),name='cost_estimate_detail'), #原価詳細
    path('cost-estimates/<str:pk>/edit/',views.CostEstimateUpdateView.as_view(),name='cost_estimate_edit'), #原価編集

    path('cost-estimates/<str:pk>/lines/create/',views.CostEstimateLineCreateView.as_view(),name='cost_estimate_line_create'), #原価明細登録
    path('cost-estimates/lines/<int:pk>/edit/',views.CostEstimateLineUpdateView.as_view(),name='cost_estimate_line_edit'), #原価明細編集
    path('cost-estimates/<str:pk>/lines/order/',views.CostEstimateLineOrderUpdateView.as_view(),name='cost_estimate_line_order'),
    path('cost-estimates/lines/<int:pk>/delete/',views.CostEstimateLineDeleteView.as_view(),name='cost_estimate_line_delete'), #原価明細削除

    path('estimates/',views.EstimateListView.as_view(),name='estimate_index'), #見積一覧
    path('estimates/create/',views.EstimateCreateView.as_view(),name='estimate_create'), #見積登録
    path('estimates/<str:pk>/',views.EstimateDetailView.as_view(),name='estimate_detail'), #見積詳細
    path('estimates/<str:pk>/edit/',views.EstimateUpdateView.as_view(),name='estimate_edit'), #見積編集
    path('estimates/<str:pk>/pdf/',views.EstimatePDFView.as_view(),name='estimate_pdf'), #見積PDF出力

    path('estimates/<str:pk>/lines/create/',views.EstimateLineCreateView.as_view(),name='estimate_line_create'), #見積明細登録
    path('estimates/lines/<int:pk>/edit/',views.EstimateLineUpdateView.as_view(),name='estimate_line_edit'), #見積明細編集
    path('estimates/<str:pk>/lines/order/',views.EstimateLineOrderUpdateView.as_view(),name='estimate_line_order'),
    path('estimates/lines/<int:pk>/delete/',views.EstimateLineDeleteView.as_view(),name='estimate_line_delete'), #見積明細削除
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)