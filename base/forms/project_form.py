from django import forms
from base.models import Project

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    fields = [
      "name",
      "customer_name",
      "service",
      "assignee_user",
      "note",
    ]

    widgets = {
      "name": forms.TextInput(attrs={"class": "form-control",}),
      "customer_name": forms.TextInput(attrs={"class": "form-control",}),
      "service": forms.Select(attrs={"class": "form-select",}),
      "assignee_user": forms.Select(attrs={"class": "form-select",}),
      "note": forms.Textarea(attrs={"class": "form-control","rows": 4,}),
      }
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields["assignee_user"].label_from_instance = (
      lambda user: f"{user.last_name} {user.first_name}"
    )