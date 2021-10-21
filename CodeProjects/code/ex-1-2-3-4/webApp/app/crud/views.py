from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages 
from django.contrib.messages.views import SuccessMessageMixin 
from django import forms
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import connection, transaction

def index(request):
    return HttpResponse("Hello, world. You're at the crud index.")

def SQLformat_comparison(op, value) -> str:

    comp_value = None
    null_is_involved = value in ["null", "NULL"]

    if null_is_involved: comp_value = "NULL"
    else:
        try:
            comp_value = float(value)

            if str(comp_value).indexOf('.') == -1:          # int
                comp_value =  str(int(value))
            else: comp_value = str(comp_value)              # float       
        
        except: pass
            
        if str(value) == "True" or str(value) == "False":   # boolean
            comp_value = str(value)

        comp_value = f"\'{str(value)}\'"                    # string
        
    # compute operator
    operator = None
    if op == "gt" : operator = ">"
    if op == "lt" : operator = "<"
    if op == "ge" : operator = ">="
    if op == "le" : operator = "<="
    if op == "eq" : operator = "IS" if null_is_involved else "="
    if op == "ne" : operator = "IS NOT" if null_is_involved else "<>"
    if operator is None: return None

    return f"{operator} {comp_value}"

def compute_select_query(table, attribute, operator, compared_value):

    comparison = f"{attribute} {SQLformat_comparison(operator, compared_value)}"
    query = f"SELECT * FROM {table} WHERE {comparison};"
    
    return query

# Restaurants

class RestaurantDetalle(DetailView): 
    model = Restaurant

class RestaurantCrear(SuccessMessageMixin, CreateView): 
    model = Restaurant 
    form = Restaurant
    fields = "__all__"
    success_message = 'Restaurant Creado Correctamente !'
 
    def get_success_url(self):        
        return reverse('r_leer') # Redireccionamos a la vista principal 'leer'

class RestaurantActualizar(SuccessMessageMixin, UpdateView): 
    model = Restaurant 
    form = Restaurant
    fields = "__all__"
    success_message = 'Restaurant Actualizado Correctamente !'
 
    def get_success_url(self):               
        return reverse('r_leer') # Redireccionamos a la vista principal 'leer'

class RestaurantEliminar(SuccessMessageMixin, DeleteView): 
    model = Restaurant 
    form = Restaurant
    fields = "__all__"     
 
    def get_success_url(self): 
        success_message = 'Restaurant Eliminado Correctamente !'
        messages.success (self.request, (success_message))       
        return reverse('r_leer') # Redireccionamos a la vista principal 'leer'

class RestaurantListado(ListView): 
    model = Restaurant
    paginate_by = 25
    
    def get_queryset(self):
        
        qs = super().get_queryset()
        
        attribute = self.request.GET.get('attribute')
        operator = self.request.GET.get('operator')
        compared_value = self.request.GET.get('compared_value')
        
        if None in [attribute, operator, compared_value]:
            return qs

        return qs.raw(compute_select_query('Restaurant', attribute, operator, compared_value))


# Segments

class SegmentDetalle(DetailView): 
    model = Segment

class SegmentCrear(SuccessMessageMixin, CreateView): 
    model = Segment 
    form = Segment
    fields = "__all__"
    success_message = 'Segment created successfully!'
 
    def get_success_url(self):        
        return reverse('s_leer') # Redireccionamos a la vista principal 'leer'

class SegmentActualizar(SuccessMessageMixin, UpdateView): 
    model = Segment 
    form = Segment
    fields = "__all__"
    success_message = 'Segment updated successfully!'
 
    def get_success_url(self):               
        return reverse('s_leer') # Redireccionamos a la vista principal 'leer'

class SegmentEliminar(SuccessMessageMixin, DeleteView): 
    model = Segment 
    form = Segment
    fields = "__all__"     
 
    def get_success_url(self): 
        success_message = 'Segment deleted succesfully !'
        messages.success (self.request, (success_message))       
        return reverse('s_leer') # Redireccionamos a la vista principal 'leer'

class SegmentListado(ListView): 
    model = Segment
    paginate_by = 25
    
    def get_queryset(self):
        
        qs = super().get_queryset()
        
        attribute = self.request.GET.get('attribute')
        operator = self.request.GET.get('operator')
        compared_value = self.request.GET.get('compared_value')
        
        if None in [attribute, operator, compared_value]:
            return qs

        return qs.raw(compute_select_query('Segment', attribute, operator, compared_value))

def redirectRestaurant(request):
    return HttpResponseRedirect('/restaurant')

def updateAvgs(request):

    if request.method =='POST':

        cursor = connection.cursor()

        avgPopularityQuery = ("SELECT AVG(R.popularity_rate)\n"
                                "FROM Segment S\n"
                                "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                                "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                                "WHERE S.uidentifier = target.uidentifier")

        cursor.execute(f"UPDATE Segment target SET average_popularity_rate = ({avgPopularityQuery});")

        
        avgSatisfactionQuery = ("SELECT AVG(R.satisfaction_rate)\n"
                                "FROM Segment S\n"
                                "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                                "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                                "WHERE S.uidentifier = target.uidentifier")

        cursor.execute(f"UPDATE Segment target SET average_satisfaction_rate = ({avgSatisfactionQuery});")


        avgPriceQuery = ("SELECT AVG(R.average_price)\n"
                        "FROM Segment S\n"
                        "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                        "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                        "WHERE S.uidentifier = target.uidentifier")

        cursor.execute(f"UPDATE Segment target SET average_price = ({avgPriceQuery});")


        totalReviewsQuery = ("SELECT SUM(R.total_reviews)\n"
                            "FROM Segment S\n"
                            "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                            "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                            "WHERE S.uidentifier = target.uidentifier")
        
        cursor.execute(f"UPDATE Segment target SET total_reviews = ({totalReviewsQuery});")

    return HttpResponseRedirect('/segment')



# RestaurantSegmentAssociation

class RestaurantSegmentAssociationDetalle(DetailView): 
    
    model = Restaurant_Segment_Association
    
    # slug_field = 'restaurantUID'
    # slug_url_kwarg = 'restaurantUID'

    # def get_queryset(self):
    #     return Restaurant_Segment_Association.objects.only('restaurantuid', 'segmentuid')

    # def get_object(self, queryset=None):

    #     # Use a custom queryset if provided; this is required for subclasses
    #     # like DateDetailView
    #     if queryset is None:
    #         queryset = self.get_queryset()

    #     # Next, try looking up by primary key.
    #     restUID = self.kwargs.get('restaurantuid')
    #     segmUID = self.kwargs.get('segmentuid')
        
    #     queryset = queryset.filter(pk=segmUID)
    #     queryset = queryset.filter(**{'restaurantuid': restUID})
            
    #     try:
    #         # Get the single item from the filtered queryset
    #         obj = queryset.get()
    #     except queryset.model.DoesNotExist:
    #         from django.http import Http404
    #         raise Http404(("No %(verbose_name)s found matching the query") %
    #                       {'verbose_name': queryset.model._meta.verbose_name})
    #     return obj

class RestaurantSegmentAssociationCrear(SuccessMessageMixin, CreateView): 
    model = Restaurant_Segment_Association 
    form = Restaurant_Segment_Association
    fields = "__all__"
    success_message = 'RestaurantSegmentAssociation created successfully!'
    
    # def get_queryset(self):
    #     return Restaurant_Segment_Association.objects.only('restaurantuid', 'segmentuid')

    def get_success_url(self):        
        return reverse('rs_leer') # Redireccionamos a la vista principal 'leer'

class RestaurantSegmentAssociationActualizar(SuccessMessageMixin, UpdateView): 
    model = Restaurant_Segment_Association 
    form = Restaurant_Segment_Association
    fields = "__all__"
    success_message = 'RestaurantSegmentAssociation updated successfully!'
    
    # def get_queryset(self):
    #     return Restaurant_Segment_Association.objects.only('restaurantuid', 'segmentuid')

    # def get_object(self, queryset=None):

    #     # Use a custom queryset if provided; this is required for subclasses
    #     # like DateDetailView
    #     if queryset is None:
    #         queryset = self.get_queryset()

    #     # Next, try looking up by primary key.
    #     restUID = self.kwargs.get('restaurantuid')
    #     segmUID = self.kwargs.get('segmentuid')
        
    #     queryset = queryset.filter(pk=segmUID)
    #     queryset = queryset.filter(**{'restaurantuid': restUID})
            
    #     try:
    #         # Get the single item from the filtered queryset
    #         obj = queryset.get()
    #     except queryset.model.DoesNotExist:
    #         from django.http import Http404
    #         raise Http404(("No %(verbose_name)s found matching the query") %
    #                       {'verbose_name': queryset.model._meta.verbose_name})
    #     return obj

    def get_success_url(self):               
        return reverse('rs_leer') # Redireccionamos a la vista principal 'leer'

class RestaurantSegmentAssociationEliminar(SuccessMessageMixin, DeleteView): 
    model = Restaurant_Segment_Association 
    form = Restaurant_Segment_Association
    fields = "__all__"     
    
    # def get_queryset(self):
    #     return Restaurant_Segment_Association.objects.only('restaurantuid', 'segmentuid')

    # def get_object(self, queryset=None):

    #     # Use a custom queryset if provided; this is required for subclasses
    #     # like DateDetailView
    #     if queryset is None:
    #         queryset = self.get_queryset()

    #     # Next, try looking up by primary key.
    #     restUID = self.kwargs.get('restaurantuid')
    #     segmUID = self.kwargs.get('segmentuid')
        
    #     queryset = queryset.filter(**{'segmentuid': segmUID})
    #     queryset = queryset.filter(**{'restaurantuid': restUID})
        
    #     print(f"Cantidates to delete: {len(queryset)}\n {queryset}")
    #     try:
    #         # Get the single item from the filtered queryset
    #         obj = queryset.get()
    #     except queryset.model.DoesNotExist:
    #         from django.http import Http404
    #         raise Http404(("No %(verbose_name)s found matching the query") %
    #                       {'verbose_name': queryset.model._meta.verbose_name})
    #     return obj

    def get_success_url(self): 
        success_message = 'RestaurantSegmentAssociation deleted succesfully !'
        messages.success (self.request, (success_message))       
        return reverse('rs_leer') # Redireccionamos a la vista principal 'leer'

class RestaurantSegmentAssociationListado(ListView): 
    model = Restaurant_Segment_Association
    paginate_by = 25
    
    def get_queryset(self):
        
        # qs = Restaurant_Segment_Association.objects.only('restaurantuid', 'segmentuid') 
        qs = super().get_queryset()
        
        attribute = self.request.GET.get('attribute')
        operator = self.request.GET.get('operator')
        compared_value = self.request.GET.get('compared_value')
        
        if None in [attribute, operator, compared_value]:
            return qs

        return qs.raw(compute_select_query('Restaurant_Segment_Association', attribute, operator, compared_value))

