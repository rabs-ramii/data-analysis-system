from django.db import models

# Create your models here.

class File(models.Model):
    id=models.BigAutoField(primary_key=True)
    file=models.FileField(upload_to="csvfiles",max_length=250, null=False)
