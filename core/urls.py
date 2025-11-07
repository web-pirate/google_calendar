from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.calendar_view, name="calendar"),
    path("events/", views.events_list, name="events-list"),
    path("events/create/", views.event_create, name="events-create"),
    path("events/<int:event_id>/", views.event_update,
         name="events-update"),  # PUT/PATCH
    path("events/<int:event_id>/delete/",
         views.event_delete, name="events-delete"),
]
