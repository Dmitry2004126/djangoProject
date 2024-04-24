from django.contrib import admin

# Register your models here.
from Footballer.models import *


admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Project)
admin.site.register(Side)