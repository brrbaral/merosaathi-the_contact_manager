from django.shortcuts import render, get_object_or_404, redirect
from . models import Contact
from django.views.generic import ListView,DetailView
from django.db.models import Q     
from django.views.generic.edit import CreateView      
from django.views.generic.edit import UpdateView   
from django.views.generic.edit import DeleteView   
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required                                                                        
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

# Create your views here.
'''def home(request):
    context={
        'contacts':Contact.objects.all()
    }
    return render(request, 'index.html', context)'''
''' def detail(request, id):
    context={
        'contact':get_object_or_404(Contact, pk=id)
    }
    return render(request,'detail.html',context) '''

#CLASS BASED VIEW

class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Contact
    context_object_name = 'contacts'
#TO SHOW THE CONTACTS OF THE CURRENT LOGGED_IN USER
    def get_queryset(self):
        contacts=super().get_queryset()
        return contacts.filter(manager=self.request.user)

class ContactDetailView(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    model = Contact
    context_object_name = 'contact'

@login_required
def search(request):
    if request.GET:
        search_term=request.GET['search_term']
        search_results=Contact.objects.filter(
        Q(name__icontains=search_term) |
        Q(email__icontains=search_term)|
        Q(phone__icontains=search_term)|
        Q(status__icontains=search_term)
        )
        context={
        'search_term':search_term,
        'contacts':search_results.filter(manager=request.user)
        }
        return render(request,'search.html',context)
    else:
        return redirect('home')

class ContactCreateView(LoginRequiredMixin, CreateView):
    model=Contact
    template_name='create.html'
    fields=['name','email','phone','gender','image']
    
    #TO SELECT THE DEFAULT MANAGER
    def form_valid(self, form):
        instance=form.save(commit=False)
        instance.manager=self.request.user
        instance.save()
        #TO SHOW THE ALERT MESSAGES WHILE THE CRREATING  CONTACT IS SUCCESS
        messages.success(self.request, 'Your contact have been successfully created')
        return redirect('home')
        
        

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model=Contact
    template_name='update.html'
    fields=['name','email','phone','gender','image','date_added','info']
    #TO GO TO THE HOMEPAGE
    #success_url='/'
    
    #TO GO TO THAT DETAIL PAGE WHICH IS BEING UPDATED
    def form_valid(self,form):
        instance=form.save()
        messages.success(self.request,'Contact Updated Successfully')
        return redirect('detail',instance.pk)

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model=Contact
    template_name='delete.html'
    #PASSING MESSAGE IN DELETED VIEW THE FOLLWOING WILL NOT WORK WE NEED METHOD FOR THIS
    #messages.success(search.request,'Deleted Successfully')
    success_url='/'

    def delete(self,request, *args, **kwargs):
        messages.success(self.request, 'Contact deleted successfully')
    #WE HAVE TO RUN THE DELETE METHOD TO ACTUALLY DELTED THE CONTACT
        return super().delete(self,request, *args, **kwargs)    

#SIGN UP
class SignUpView(CreateView):
    form_class=UserCreationForm
    email=forms.EmailField(max_length=100,help_text='Required')
    template_name='registration/signup.html'
    success_url= '/'

    class Meta:
        model=User
        fields=['username','email','password1','password2']