from django.db import models

# Create your models here.
class Candidate(models.Model) #모델 이름은 단수로 적는다 / 시작은 대문자
	name = models.CharField(max_length=10)
	introduction = models.TextField()
	area = models.CharField(max_length=15)
	party_number = models.IntegerField(default=1)
	