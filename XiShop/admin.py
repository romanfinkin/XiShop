from django.contrib.admin import site
from .models import *


site.register(Currency)
site.register(Product)
site.register(Order)
