from django.db import models
from .project_models import Project
from django.utils.crypto import get_random_string

def create_id():
  return get_random_string(20)

class CostEstimate(models.Model):
  cost_estimate_id = models.CharField(verbose_name='原価ID',default=create_id, primary_key=True, max_length=20, editable=False)
  project = models.ForeignKey(Project,verbose_name='案件',on_delete=models.CASCADE,related_name='cost_estimates')
  title = models.CharField(verbose_name="件名", max_length=100)
  vendor_name = models.CharField(verbose_name="仕入先", max_length=100)
  quote_date = models.DateField(verbose_name='見積日')
  expiration_date = models.DateField(verbose_name='有効期限')
  note = models.TextField(verbose_name="備考", blank=True)
  pdf_file = models.FileField(verbose_name='PDFファイル',upload_to='cost_estimates/',blank=True,null=True)
  tax_rate = models.PositiveIntegerField(verbose_name='税率',default=10)
  created_at = models.DateTimeField(verbose_name='登録日時',auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

  def __str__(self):
    return self.title
  
  @property
  def subtotal(self):
    return sum(line.amount for line in self.lines.all())
  
  @property
  def tax_amount(self):
    return int(self.subtotal * self.tax_rate / 100)
  
  @property
  def total_amount(self):
    return self.subtotal + self.tax_amount

class CostEstimateLine(models.Model):
  cost_estimate_line_id = models.BigAutoField(verbose_name='原価明細ID',primary_key=True)
  cost_estimate = models.ForeignKey(CostEstimate,verbose_name='原価',on_delete=models.CASCADE,related_name='lines')
  display_order = models.PositiveIntegerField(verbose_name='表示順', default=1)
  item_name = models.CharField(verbose_name='品目',max_length=100)
  quantity = models.PositiveIntegerField(verbose_name='数量')
  unit = models.CharField(verbose_name='単位',max_length=20)
  unit_price = models.DecimalField(verbose_name='単価',max_digits=12,decimal_places=0)
  created_at = models.DateTimeField(verbose_name='登録日時',auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

  class Meta:
    ordering = ['display_order']

  def __str__(self):
      return self.item_name
  
  def save(self, *args, **kwargs):
  
      if not self.pk:
        max_order = (
            CostEstimateLine.objects
            .filter(cost_estimate=self.cost_estimate)
            .aggregate(models.Max('display_order'))
            .get('display_order__max')
            or 0
        )
        self.display_order = max_order + 1

      super().save(*args, **kwargs)

  @property
  def amount(self):
    return self.quantity * self.unit_price