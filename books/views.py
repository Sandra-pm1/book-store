from django.shortcuts import render,redirect
from django.views.generic import View
from books.forms import BookForm,BookUpdateForm,SignUpForm,SignInForm
from books.models import Books
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from books.decorators import signin_required
from django.utils.decorators import method_decorator

@method_decorator(signin_required,name="dispatch")
class BookCreateView(View):
    template_name="book_add.html"
    form_class=BookForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data,files=request.FILES)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            Books.objects.create(**data)
            messages.success(request,"New Book Added Sucessfully !!")
            return redirect("book-list")
            messages.success(request,"Failed To Add !!")
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class BookListView(View):
    template_name="book_list.html"
    def get(self,request,*args,**kwargs):
        search_text=request.GET.get("filter")
        qs=Books.objects.all()
        all_title=Books.objects.values_list("title",flat=True).distinct()
        all_authors=Books.objects.values_list("author",flat=True).distinct()
        all_genre=Books.objects.values_list("genre",flat=True).distinct()
        all_language=Books.objects.values_list("language",flat=True).distinct()
        all_records=[]
        all_records.extend(all_title)
        all_records.extend(all_authors)
        all_records.extend(all_genre)
        all_records.extend(all_language)
        if search_text:
            qs=qs.filter(
                        Q(title__contains=search_text)|
                        Q(author__contains=search_text)|
                        Q(genre__contains=search_text)|
                        Q(language__contains=search_text)
                        )
        return render(request,self.template_name,{"data":qs,"records":all_records})

@method_decorator(signin_required,name="dispatch")
class BookDetailView(View):
    template_name="book_details.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        return render(request,self.template_name,{"data":qs})

@method_decorator(signin_required,name="dispatch")
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id).delete()
        messages.success(request,"Book Deleted Successfully")
        return redirect("book-list")

# class BookUpdateView(View):
    # template_name="book_update.html"
    # form_class=BookForm
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     book_object=Books.objects.get(id=id)
    #     data={
    #         "title":book_object.title,
    #         "author":book_object.author,
    #         "price":book_object.price,
    #         "genre":book_object.genre,
    #         "language":book_object.language,
    #         "publisher":book_object.publisher
    #     }
    #     form_instance=self.form_class(initial=data)
    #     return render(request,self.template_name,{"form":form_instance})
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     form_data=request.POST
    #     form_instance=self.form_class(form_data,files=request.FILES)
    #     if form_instance.is_valid():
    #         data=form_instance.cleaned_data
    #         Books.objects.filter(id=id).update(**data)
    #         return redirect("book-list")
    #     return render(request,self.template_name,{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class BookUpdateView(View):
    template_name="book_update.html"
    form_class=BookUpdateForm
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        book_object=Books.objects.get(id=id)
        form_instance=self.form_class(instance=book_object)
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        book_object=Books.objects.get(id=id)
        form_data=request.POST
        form_instance=self.form_class(form_data,files=request.FILES,instance=book_object)
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request,"Book Updated Successfully")
            return redirect("book-list")
        messages.error(request,"Failed To Update Book")
        return render(request,self.template_name,{"form":form_instance})

class SignUpView(View):
    template_name="register.html"
    form_class=SignUpForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            User.objects.create_user(**data)
            return redirect("register")
        return render(request,self.template_name,{"form":form_instance})

class SignInView(View):
    template_name="signin.html"
    form_class=SignInForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("book-list")
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
