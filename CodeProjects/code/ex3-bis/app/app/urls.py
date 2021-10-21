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
from django.urls import path
from crud.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
 
    path('restaurant/', RestaurantListado.as_view(template_name = "restaurant/index.html"), name='r_leer'),
    path('restaurant/detalle/<slug:pk>', RestaurantDetalle.as_view(template_name = "restaurant/detalles.html"), name='r_detalles'),
    path('restaurant/crear', RestaurantCrear.as_view(template_name = "restaurant/crear.html"), name='r_crear'),
    path('restaurant/editar/<slug:pk>', RestaurantActualizar.as_view(template_name = "restaurant/actualizar.html"), name='r_actualizar'), 
    path('restaurant/eliminar/<slug:pk>', RestaurantEliminar.as_view(), name='r_eliminar'),

    path('segment/', SegmentListado.as_view(template_name = "segment/index.html"), name='s_leer'),
    path('segment/detalle/<slug:pk>', SegmentDetalle.as_view(template_name = "segment/detalles.html"), name='s_detalles'),
    path('segment/crear', SegmentCrear.as_view(template_name = "segment/crear.html"), name='s_crear'),
    path('segment/editar/<slug:pk>', SegmentActualizar.as_view(template_name = "segment/actualizar.html"), name='s_actualizar'), 
    path('segment/eliminar/<slug:pk>', SegmentEliminar.as_view(), name='s_eliminar'),

    path('restaurant_segment_association/', RestaurantSegmentAssociationListado.as_view(template_name = "restaurant_segment_association/index.html"), name='rs_leer'),
    path('restaurant_segment_association/detalle/<slug:pk>', RestaurantSegmentAssociationDetalle.as_view(template_name = "restaurant_segment_association/detalles.html"), name='rs_detalles'),
    path('restaurant_segment_association/crear', RestaurantSegmentAssociationCrear.as_view(template_name = "restaurant_segment_association/crear.html"), name='rs_crear'),
    path('restaurant_segment_association/editar/<slug:pk>', RestaurantSegmentAssociationActualizar.as_view(template_name = "restaurant_segment_association/actualizar.html"), name='rs_actualizar'), 
    path('restaurant_segment_association/eliminar/<slug:pk>', RestaurantSegmentAssociationEliminar.as_view(), name='rs_eliminar'),
]  