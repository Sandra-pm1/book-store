from django import forms
from books.models import Books
from django.contrib.auth.models import User

class BookForm(forms.Form):
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    author=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    price=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control mb-3"}))
    genre=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    language=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    publisher=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    picture=forms.ImageField()

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "author":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "genre":forms.TextInput(attrs={"class":"form-control"}),
            "language":forms.TextInput(attrs={"class":"form-control"}),
            "publisher":forms.TextInput(attrs={"class":"form-control"}),
            "picture":forms.FileInput(attrs={"class":"form-control"})
        }

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

class SignInForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    