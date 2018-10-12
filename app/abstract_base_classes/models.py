# 1. AbstractBaseClasses
#  자식 테이블만 존재
# 2. Multi table inheritance
#  부모, 자식 테이블이 모두 존재
# 3. Proxy model
#  부모 테이블만 존재
from django.db import models


class CommonInfo(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta):
        verbose_name = '학생'
        verbose_name_plural = '학생 목록'
