"""bookInventoryManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stores import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.stores),
    path('loginuser/<int:id>', views.handlelogin,name="login"),
    path('loginuser/', views.handlelogin,name="login"),
    path('logout/', views.handlelogout, ),
    path('registerstore/', views.handleregister),
    path('Mystore/searchbook/searchresult/', views.searchedbook),
    path('Mystore/selectbook/<str:book_id>', views.addInventory, name="selectbook"), 
    path('Mystore/', views.Mystore,name="mystore"),
    path('Mystore/searchbook/', views.addbookpage,),
    path('Mystore/add/', views.addInventory,name="addbook"),
    path('Mystore/updatebookquantity/<str:book_id>/', views.Mystore,name="updatebookquantity"),
    path('Mystore/remove/<str:book_id>/', views.remove,name="remove"),
    
    
    
]
