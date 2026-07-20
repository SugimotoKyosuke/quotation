from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.db import transaction

from base.models import CostEstimate, CostEstimateLine
from base.forms.cost_estimate_form import CostEstimateForm, CostEstimateLineForm
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

class CostEstimateListView(LoginRequiredMixin, ListView):
  model = CostEstimate
  template_name = 'cost_estimates/index.html'
  context_object_name = 'cost_estimates'
  paginate_by = 10

  def get_queryset(self):
      query = self.request.GET.get('q', '')

      queryset = CostEstimate.objects.select_related('project')

      if query:
          queryset = queryset.filter(
              Q(title__icontains=query) |
              Q(vendor_name__icontains=query) |
              Q(project__name__icontains=query)
          )

      return queryset.order_by('-created_at')

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['query'] = self.request.GET.get('q', '')
      return context


class CostEstimateDetailView(LoginRequiredMixin, DetailView):
    model = CostEstimate
    template_name = 'cost_estimates/detail.html'

class CostEstimateCreateView(LoginRequiredMixin, CreateView):
    model = CostEstimate
    template_name = 'cost_estimates/create.html'
    form_class = CostEstimateForm

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project')

        if project_id:
            initial['project'] = project_id

        return initial

    def get_success_url(self):
        return reverse(
            'cost_estimate_edit',
            kwargs={'pk': self.object.pk}
        )

class CostEstimateUpdateView(LoginRequiredMixin, UpdateView):
    model = CostEstimate
    template_name = 'cost_estimates/edit.html'
    form_class = CostEstimateForm

    def get_success_url(self):
        return reverse(
            'cost_estimate_detail',
            kwargs={'pk': self.object.pk}
        )
        
class CostEstimateLineCreateView(LoginRequiredMixin, CreateView):
    model = CostEstimateLine
    template_name = 'cost_estimates/lines/create.html'
    form_class = CostEstimateLineForm

    def form_valid(self, form):
        cost_estimate = get_object_or_404(
        CostEstimate,
        pk=self.kwargs['pk']
        )

        form.instance.cost_estimate = cost_estimate

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
            'cost_estimate_edit',
            kwargs={'pk': self.object.cost_estimate.pk}
        )

class CostEstimateLineUpdateView(LoginRequiredMixin, UpdateView):
    model = CostEstimateLine
    template_name = 'cost_estimates/lines/edit.html'
    form_class = CostEstimateLineForm

    def get_success_url(self):
        return reverse(
            'cost_estimate_edit',
            kwargs={'pk': self.object.cost_estimate.pk}
        )
    
class CostEstimateLineOrderUpdateView(LoginRequiredMixin, View):

    def post(self, request, pk):

        orders = request.POST.getlist('orders[]')

        with transaction.atomic():

            for index, line_id in enumerate(orders, start=1):
                line = get_object_or_404(
                    CostEstimateLine,
                    pk=line_id
                )

                line.display_order = index
                line.save()

        return JsonResponse({
            'status': 'success'
        })
    
class CostEstimateLineDeleteView(LoginRequiredMixin, DeleteView):
    model = CostEstimateLine
    template_name = 'cost_estimates/lines/delete.html'

    def get_success_url(self):
        return reverse(
            'cost_estimate_edit',
            kwargs={'pk': self.object.cost_estimate.pk}
        )