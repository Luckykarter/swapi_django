from django.urls import path
import exhaust_port.views as views

urlpatterns = [
    path("xwings/", views.xwinglist.as_view()),

    path('defence_towers/', views.all_towers),
    path('defence_towers/<int:pk>', views.get_tower_by_id),
    path('defence_towers/xwings/<int:pk>', views.get_tower_by_xwing_id),
    path('defence_towers/xwings/my', views.get_tower_by_user),

    path('starships/', views.all_starships),
    path('species/starships/<int:pk>', views.get_species_by_starship),
    path('species/starships/producers/<str:name>', views.get_species_by_producer),
    path('evacuate_planet/<int:planet_id>/starships/<int:starship_id>', views.evacuate_planet),
]

