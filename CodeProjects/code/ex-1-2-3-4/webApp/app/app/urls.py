"""app URL Configuration

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
from django.urls import path, include
from crud import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
     
    path('', views.redirectRestaurant, name='home'),
    path('restaurant/', views.RestaurantListado.as_view(template_name = "restaurant/index.html"), name='r_leer'),
    path('restaurant/detalle/<slug:pk>', views.RestaurantDetalle.as_view(template_name = "restaurant/detalles.html"), name='r_detalles'),
    path('restaurant/crear', views.RestaurantCrear.as_view(template_name = "restaurant/crear.html"), name='r_crear'),
    path('restaurant/editar/<slug:pk>', views.RestaurantActualizar.as_view(template_name = "restaurant/actualizar.html"), name='r_actualizar'), 
    path('restaurant/eliminar/<slug:pk>', views.RestaurantEliminar.as_view(), name='r_eliminar'),

    path('segment/', views.SegmentListado.as_view(template_name = "segment/index.html"), name='s_leer'),
    path('segment/detalle/<slug:pk>', views.SegmentDetalle.as_view(template_name = "segment/detalles.html"), name='s_detalles'),
    path('segment/crear', views.SegmentCrear.as_view(template_name = "segment/crear.html"), name='s_crear'),
    path('segment/editar/<slug:pk>', views.SegmentActualizar.as_view(template_name = "segment/actualizar.html"), name='s_actualizar'), 
    path('segment/eliminar/<slug:pk>', views.SegmentEliminar.as_view(), name='s_eliminar'),
    path('segment/update_avgs', views.updateAvgs, name='s_updateavgs'),

    path('restaurant_segment_association/', views.RestaurantSegmentAssociationListado.as_view(template_name = "restaurant_segment_association/index.html"), name='rs_leer'),
    path('restaurant_segment_association/detalle/<slug:pk>', views.RestaurantSegmentAssociationDetalle.as_view(template_name = "restaurant_segment_association/detalles.html"), name='rs_detalles'),
    path('restaurant_segment_association/crear', views.RestaurantSegmentAssociationCrear.as_view(template_name = "restaurant_segment_association/crear.html"), name='rs_crear'),
    path('restaurant_segment_association/editar/<slug:pk>', views.RestaurantSegmentAssociationActualizar.as_view(template_name = "restaurant_segment_association/actualizar.html"), name='rs_actualizar'), 
    path('restaurant_segment_association/eliminar/<slug:pk>', views.RestaurantSegmentAssociationEliminar.as_view(), name='rs_eliminar'),
]  