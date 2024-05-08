from django.urls import path, register_converter
from . import views, converters
register_converter(converters.DateConverter, "yyyymmdd")
from django.views.generic import TemplateView
from .views import (
TaskCreateView,
TaskDeleteView,
TaskDetailView,
TaskListView,
TaskUpdateView,
create_task_on_sprint
)

app_name = 'tasks' # This is for namespacing the URLS
handler404 = 'tasks.views.custom_404'



urlpatterns = [
    path('', TemplateView.as_view(template_name='tasks/home.html'), name='home'),
    path('help/', TemplateView.as_view(template_name='tasks/help.html'), name='help'),
    path("tasks/", TaskListView.as_view(), name="task-list"), # GET
    path("tasks/new/", TaskCreateView.as_view(), name="taskcreate"), # POST
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="taskdetail"), # GET
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"), # PUT/PATCH
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"), # DELETE

    path("tasks/sprint/add_task/<int:pk>/", create_task_on_sprint, name="task-add-to-sprint")

   # path("tasks/<yyyymmdd:date>/", views.task_by_date),
]