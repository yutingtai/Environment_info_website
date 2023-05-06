from django.contrib import admin
from .models import AqiDataDbModel,EqDataDbModel,IntensityDbModel
# Register your models here.

admin.site.register(AqiDataDbModel)
admin.site.register(EqDataDbModel)
admin.site.register(IntensityDbModel)