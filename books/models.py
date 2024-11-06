from django.db import models

# Create your models here.

class Books(models.Model):
    title=models.CharField(max_length=200,null=True)
    author=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    genre=models.CharField(max_length=200)
    language=models.CharField(max_length=200)
    publisher=models.CharField(max_length=300,null=True)
    picture=models.ImageField(upload_to="picture_book",null=True)

    def __str__(self):
        return self.title