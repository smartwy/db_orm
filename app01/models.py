from django.db import models

# Create your models here.

class Business(models.Model):
	# id列
	caption = models.CharField(max_length=32)
	code = models.CharField(max_length=32)


class Host(models.Model):
	nid = models.AutoField(primary_key=True)
	hostname = models.CharField(max_length=32, db_index=True)
	ip = models.GenericIPAddressField(db_index=True, protocol='ipv4')
	port = models.IntegerField()
	bus = models.ForeignKey('Business', to_field='id', on_delete=models.CASCADE)