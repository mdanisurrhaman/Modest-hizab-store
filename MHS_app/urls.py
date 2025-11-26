from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static

from MHS_app.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib.auth.views import PasswordResetView
# from django.contrib.auth.views import PasswordResetConfirmView





urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('product/', product_view),
    path('product/<int:id>/', product_view),
    path('customer/', customer_view),
    path('customer/<int:id>/', customer_view),
    path('register/', Register),
    path('logout/', logout_view),
    path('cart/', cart_view),
    path('cartitem/', cartt_item),
    path('cartitem/<int:id>/', cartt_item),
    path('employee/', Emp_view),
    path('employee/<int:id>', Emp_view),
    path('category/<int:id>', category_view),
    path('category/', category_view),
    path('subcategory/<int:id>', sub_view),
    path('subcategory/', sub_view),
    
    path('pro_variation/', Pro_variation),
    path('pro_variation/<int:id>', Pro_variation),

    
    path('Variation/', variation_views),
    path('Variation/<int:id>', variation_views),
    
    path('option/', variation_option),
    path('option/<int:id>', variation_option),
    
    path('address/', Addresss),
    path('address/<int:id>', Addresss),
    
    path('order/', Order_view),
    path('order/<int:id>', Order_view),
    
    path('collection/', Collections_View),
    path('collection/<int:id>/', Collections_View),


    
    path('quotes/', Quotation_view),
    path('quotes/<int:id>', Quotation_view),
    path('qygy/', U_view),

    path('password-reset/', ResetRequestView.as_view()),
    path('reset/<int:user_id>/<str:token>/', PasswordResetConfirmView.as_view()),
    # path('reset-password/<int:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),



    path('search/', ProductListView.as_view()),
    path('search_s/', Sub_ListView.as_view()),
    path('search_c/', Category_ListView.as_view()),
    path('reverse_s/', SubCategoryViewSet.as_view()),

    path('place-order/', OrderCreateView.as_view(), name='place-order'),

  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)