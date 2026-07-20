from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from base.models import Project
from base.forms.project_form import ProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse
from urllib.parse import urlencode


class IndexListView(LoginRequiredMixin, ListView):
  model = Project
  template_name = 'projects/index.html'
  context_object_name = 'projects'
  paginate_by = 10

  def get_queryset(self):
        query = self.request.GET.get('q', '')

        queryset = Project.objects.all()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(customer_name__icontains=query) |
                Q(service__name__icontains=query)|
                Q(assignee_user__last_name__icontains=query) |
                Q(assignee_user__first_name__icontains=query)
            )

        return queryset.order_by('-created_at')
  
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
  model = Project
  template_name = 'projects/detail.html'

class ProjectCreateView(LoginRequiredMixin, CreateView):
  model = Project
  template_name = 'projects/create.html'
  form_class = ProjectForm

  def get_success_url(self):
      next_url = self.request.POST.get('next')

      if next_url:
          query = urlencode({'project': self.object.pk})
          return f'{next_url}?{query}'

      return reverse('project_detail', kwargs={'pk': self.object.pk})

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
  model = Project
  template_name = 'projects/edit.html'
  form_class = ProjectForm
  
  def get_success_url(self):
        return reverse(
            "project_detail",
            kwargs={"pk": self.object.pk}
        )