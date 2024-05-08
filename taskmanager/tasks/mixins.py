# tasks/mixins.py
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .services import can_add_task_to_sprint

#SprintTaskWithinRangeMixin
class SprintTaskMixin:
    """
    Mixin to ensure a task being created or updated is within
    the date range of its associated sprint.
    """

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object() if hasattr(self, "get_object") else None
        sprint_id = request.POST.get("sprint")

        if sprint_id:
        # If a task exists (for UpdateView) or is about to be created (for CreateView)
            if task or request.method == "POST":
                if not can_add_task_to_sprint(task, sprint_id):
                    return HttpResponseBadRequest("Task's creation date is outside the date range of the associated sprint.")
            return super().dispatch(request, *args, **kwargs)