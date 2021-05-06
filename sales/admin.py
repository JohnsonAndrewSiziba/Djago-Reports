from django.contrib import admin

# Register your models here.
from sales.models import CSV, Position, Sale

admin.site.register(Position)
admin.site.register(Sale)
admin.site.register(CSV
                    )
