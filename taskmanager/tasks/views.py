# Code for tasks/views.py
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView,UpdateView
from .models import Task
from .mixins import SprintTaskMixin
from .services import create_task_and_add_to_sprint, claim_task



def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)


def claim_task_view(request, task_id):
    # Assuming you have access to the user ID from the request
    user_id = request.user.id

    try:
        claim_task(user_id, task_id)
        return JsonResponse({'message': 'Task successfully claimed.'})
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist.", status=status.HTTP_404_NOT_FOUND)
    except TaskAlreadyClaimedException:
        return HttpResponse("Task is already claimed or completed.", status=status.HTTP_400_BAD_REQUEST)





def create_task_on_sprint(request: HttpRequest, sprint_id:
int) -> HttpResponseRedirect:
    if request.method == 'POST':
        task_data: dict[str, str] = {
        'title': request.POST['title'],
        'description': request.POST.get('description', ""),
        'status': request.POST.get('status', "UNASSIGNED"),
        }
        task = create_task_and_add_to_sprint(task_data, sprint_id,
        request.user)
        return redirect('task-detail', task_id=task.id)
    raise Http404("Not found")

def task_by_date(request: HttpRequest, by_date: date) -> HttpResponse:
    tasks = services.get_task_by_date(by_date)
    context = {"tasks": tasks}
    return render(request, "task_list.html", context)


def check_task(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Extract the 'task_id' parameter from the POST data.
        task_id = request.POST.get("task_id")
        if services.check_task(task_id):
            return HttpResponseRedirect(reverse("success"))
        if task_id:
            return HttpResponseRedirect(reverse("success"))
        else:
        # If no ID was provided, re-render the form with an error  message.
            return render( request, "add_task_to_sprint.html", {"error": "Task ID is required."})
    else:
        # If the request method is not POST, just render the form.
        return render(request, "check_task.html")




class TaskCreateView(SprintTaskMixin, CreateView):
    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk":
        self.object.id})

class TaskUpdateView(SprintTaskMixin, UpdateView):
    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk":
        self.object.id})



class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

class TaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"

class TaskCreateView(CreateView):
    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")
    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk":
        self.object.id})
    
class TaskUpdateView(UpdateView):
    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")
    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk":
        self.object.id})
    
class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task-list")
