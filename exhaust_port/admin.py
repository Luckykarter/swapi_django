from django.contrib import admin
from .models import XWing, DefenceTower, Film, Starship, Specie, Planet
# Register Xwings and Defence towers

admin.site.register(XWing)
admin.site.register(DefenceTower)
# register other items
admin.site.register(Film)
admin.site.register(Starship)
admin.site.register(Specie)
admin.site.register(Planet)
