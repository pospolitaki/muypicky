from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

@login_required()
def restaurant_createview(request):
    form = RestaurantLocationCreateForm (request.POST or None)    
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect('/restaurants/')
        else:
            return HttpResponseRedirect('/login/')
            # obj = RestaurantLocation.objects.create(
            #     name        = form.cleaned_data.get('name'),
            #     location    = form.cleaned_data.get('location'),
            #     category    = form.cleaned_data.get('category')
            # )
    if form.errors:
        errors = form.errors

    template_name = 'restaurants/form.html'
    context = {'form':form, 'errors':errors}
    return render(request, template_name, context)



'''
def home(request):
    context = {}
    return render(request, 'home.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def contact(request):
    context = {}
    return render(request, 'contact.html', context)

#class ContactView(View):
#    def get(self, request, *args, **kwargs):
#        print(kwargs)
#        context = {}
 #       return render(request, 'contact.html', context)

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs) 
        print(context)
        return(context)   
    
class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'
'''
def restaurant_listview(request):
    template_name = 'restaurants/restaurants_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {'object_list': queryset

    }
    return render(request, template_name, context)

class RestaurantListView(LoginRequiredMixin, ListView): #context variable is always 'object_list'
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

    # def get_queryset(self):
    #     slug = self.kwargs.get('slug')
    #     if slug:
    #         queryset = RestaurantLocation.objects.filter(Q(category__iexact=slug) | Q(category__contains=slug))        
    #     else:
    #         queryset = RestaurantLocation.objects.all()
    #     return queryset

class RestaurantDetailView(LoginRequiredMixin, DetailView): #context variable is always 'object'
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

    #def get_context_data(self, *args, **kwargs):
    #    print(self.kwargs)
    #    context = super().get_context_data(*args, **kwargs)
   #     print(context)
    #    return context
 
    #def get_object(self, *args, **kwargs):
    #    rest_id = self.kwargs.get('rest_id')
    #    obj = get_object_or_404(RestaurantLocation, id = rest_id)
    #    return obj

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/form.html'
    #success_url = '/restaurants/'
    login_url = '/login/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super().form_valid(form)                        

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/detail-update.html'
    #success_url = '/restaurants/'
    login_url = '/login/'
    
    def get_context_data(self, *args, **kwargs):
        name = self.get_object().name
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f'Update Restaurant: {name}'
        return context

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)
