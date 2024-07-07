from django.forms import DecimalField
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q, F, Value, Func, ExpressionWrapper  # short for query
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from store.models import Collection, Product, Customer, OrderItems, Order
from tags.models import TaggedItem

# Create your views here.


def say_hello(request):

    # return render(request, 'helloo.html', {'name': 'deva', 'orders': list(orderset), 'products2': 'product4'})
    return render(request, 'helloo.html', {'name': 'deva'})
