from django.db.models import Q
from django.urls import reverse

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.db import transaction

from base.models import Estimate, EstimateLine
from base.forms.estimate_form import EstimateCreateForm, EstimateUpdateForm, EstimateLineForm
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin


class EstimateListView(LoginRequiredMixin, ListView):
  model = Estimate
  template_name = 'estimates/index.html'
  context_object_name = 'estimates'
  paginate_by = 10

  def get_queryset(self):
      query = self.request.GET.get('q', '')
      status = self.request.GET.get('status', '')

      queryset = Estimate.objects.select_related('project', 'project__assignee_user')

      if query:
          queryset = queryset.filter(
              Q(title__icontains=query) |
              Q(estimate_number__icontains=query) |
              Q(project__name__icontains=query) |
              Q(project__customer_name__icontains=query) |
              Q(project__service__name__icontains=query) |
              Q(project__assignee_user__last_name__icontains=query) |
              Q(project__assignee_user__first_name__icontains=query)
          )

      if status:
          queryset = queryset.filter(status=status)        

      return queryset.order_by('-created_at')

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['query'] = self.request.GET.get('q', '')
      context['status'] = self.request.GET.get('status', '')
      context['status_choices'] = Estimate.Status.choices
      return context


class EstimateDetailView(LoginRequiredMixin, DetailView):
    model = Estimate
    template_name = 'estimates/detail.html'

class EstimateCreateView(LoginRequiredMixin, CreateView):
    model = Estimate
    template_name = 'estimates/create.html'
    form_class = EstimateCreateForm

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project')

        if project_id:
            initial['project'] = project_id

        return initial

    def get_success_url(self):
        return reverse(
            'estimate_edit',
            kwargs={'pk': self.object.pk}
        )
    
class EstimateUpdateView(LoginRequiredMixin, UpdateView):
    model = Estimate
    template_name = 'estimates/edit.html'
    form_class = EstimateUpdateForm

    def get_success_url(self):
        return reverse(
            'estimate_detail',
            kwargs={'pk': self.object.pk}
        )
        
class EstimateLineCreateView(LoginRequiredMixin, CreateView):
    model = EstimateLine
    template_name = 'estimates/lines/create.html'
    form_class = EstimateLineForm

    def form_valid(self, form):
        estimate = get_object_or_404(
        Estimate,
        pk=self.kwargs['pk']
        )

        form.instance.estimate = estimate

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
            'estimate_edit',
            kwargs={'pk': self.object.estimate.pk}
        )

class EstimateLineUpdateView(LoginRequiredMixin, UpdateView):
    model = EstimateLine
    template_name = 'estimates/lines/edit.html'
    form_class = EstimateLineForm

    def get_success_url(self):
        return reverse(
            'estimate_edit',
            kwargs={'pk': self.object.estimate.pk}
        )
    
class EstimateLineOrderUpdateView(LoginRequiredMixin, View):

    def post(self, request, pk):

        orders = request.POST.getlist('orders[]')

        with transaction.atomic():

            for index, line_id in enumerate(orders, start=1):
                line = get_object_or_404(
                    EstimateLine,
                    pk=line_id
                )

                line.display_order = index
                line.save()

        return JsonResponse({
            'status': 'success'
        })
    
class EstimateLineDeleteView(LoginRequiredMixin, DeleteView):
    model = EstimateLine
    template_name = 'estimates/lines/delete.html'

    def get_success_url(self):
        return reverse(
            'estimate_edit',
            kwargs={'pk': self.object.estimate.pk}
        )
    
class EstimatePDFView(LoginRequiredMixin, View):

    def get(self, request, pk):
        estimate = get_object_or_404(
            Estimate,
            pk=pk
        )

        html_string = render_to_string('estimates/pdf.html', {
            'estimate': estimate,
        })

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="estimate_{estimate.pk}.pdf"'

        return response