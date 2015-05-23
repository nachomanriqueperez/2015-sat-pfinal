from django.contrib import admin

# Register your models here.
from .models import Usuario,Actividade

admin.site.register(Usuario)
admin.site.register(Actividade)
