from django.db import models
from .project_models import Project
from .cost_estimate_models import CostEstimate
from django.utils.crypto import get_random_string

def create_id():
  return get_random_string(20)

class Estimate(models.Model):

  class Status(models.TextChoices):
    DRAFT = 'draft', '下書き'
    REJECTED = 'rejected', '却下'
    APPROVED = 'approved', '承認済み'
    SUBMITTED = 'submitted', '提出中'
    WON = 'won', '受注'
    LOST = 'lost', '失注'

  estimate_id = models.CharField(verbose_name='見積ID',default=create_id, primary_key=True, max_length=20, editable=False)
  estimate_number = models.CharField(verbose_name='見積番号', max_length=20, unique=True)
  project = models.ForeignKey(Project,verbose_name='案件',on_delete=models.CASCADE,related_name='estimates')
  cost_estimate = models.ForeignKey(CostEstimate,verbose_name='原価',on_delete=models.PROTECT,related_name='estimates',null=True,blank=True,)  
  title = models.CharField(verbose_name='件名', max_length=100)
  quote_date = models.DateField(verbose_name='見積日')
  expiration_date = models.DateField(verbose_name='有効期限')
  status = models.CharField(verbose_name='ステータス',max_length=20,choices=Status.choices,default=Status.DRAFT)
  note = models.TextField(verbose_name='備考', blank=True)
  tax_rate = models.PositiveIntegerField(verbose_name='税率',default=10)
  created_at = models.DateTimeField(verbose_name='登録日時',auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

  def get_status_badge_class(self):
    return {
      self.Status.DRAFT: 'status-draft',
      self.Status.REJECTED: 'status-rejected',
      self.Status.APPROVED: 'status-approved',
      self.Status.SUBMITTED: 'status-submitted',
      self.Status.WON: 'status-won',
      self.Status.LOST: 'status-lost',
    }.get(self.status, 'status-draft')

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
  
  @property
  def cost_amount(self):
      if not self.cost_estimate:
          return None

      return self.cost_estimate.total_amount


  @property
  def profit_amount(self):
      if self.cost_amount is None:
          return None

      return self.total_amount - self.cost_amount


  @property
  def profit_rate(self):
      if self.profit_amount is None:
          return None

      if self.total_amount == 0:
          return 0

      return round(self.profit_amount / self.total_amount * 100,1)  
  

class EstimateLine(models.Model):
  estimate_line_id = models.BigAutoField(verbose_name='見積明細ID',primary_key=True)
  estimate = models.ForeignKey(Estimate,verbose_name='見積',on_delete=models.CASCADE,related_name='lines')
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
            EstimateLine.objects
            .filter(estimate=self.estimate)
            .aggregate(models.Max('display_order'))
            .get('display_order__max')
            or 0
        )
        self.display_order = max_order + 1

      super().save(*args, **kwargs)

  @property
  def amount(self):
    return self.quantity * self.unit_price