from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

def create_id():
  return get_random_string(20)

class Service(models.Model):
  slug = models.CharField(max_length=20, primary_key=True)
  name = models.CharField(max_length=20)

  def __str__(self):
    return self.name

class Project(models.Model):
  project_id = models.CharField(verbose_name='案件ID',default=create_id, primary_key=True, max_length=20, editable=False)
  name = models.CharField(verbose_name="案件名", max_length=100)
  customer_name = models.CharField(verbose_name="顧客名",default='', max_length=100)
  service = models.ForeignKey(Service, verbose_name="サービス",on_delete=models.PROTECT)
  assignee_user = models.ForeignKey(User, verbose_name="担当者", on_delete=models.CASCADE)
  note = models.TextField(verbose_name="備考", blank=True)
  created_at = models.DateTimeField(verbose_name='登録日時',auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

  def __str__(self):
    return self.name
