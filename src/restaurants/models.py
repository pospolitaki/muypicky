from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from .validators import validate_category
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet):
    def search(self, query): #RestaurantLocation.objects.all().search(query) RestaurantLocation.objects.filter(something).search()
        if query:
            return self.filter(
                                Q(name__icontains=query) | 
                                Q(location__icontains=query) |
                                Q(category__icontains=query) |
                                Q(item__name__icontains=query) |
                                Q(item__contents__icontains=query)
                                    ).distinct()
        return self

class RestaurantLocationManager(models.Manager):
    def get_queryset(self):
            return RestaurantLocationQuerySet(self.model, using=self._db)

    def search(self, query): #RestaurantLocation.objects.search
        return self.get_queryset().search(query)

class RestaurantLocation(models.Model):

    owner       = models.ForeignKey(User) #class_instance.model_set.all()
    name        = models.CharField(max_length=120)
    location    = models.CharField(max_length=120, blank=True, null=True)
    category    = models.CharField(max_length=120, blank=True, null=True, validators=[validate_category])
    timestamp   = models.DateTimeField(auto_now=True)
    slug        = models.SlugField(blank=True, null=True)
    objects     = RestaurantLocationManager() #add to Model.objects.all()
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return f'/restaurants/{self.slug}'
        return reverse('restaurants:detail', kwargs={'slug':self.slug})

    @property
    def title(self):
        return self.name

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


#def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
#    print('saved')
#    print(instance.timestamp)
  
pre_save.connect(rl_pre_save_receiver, sender = RestaurantLocation)
#post_save.connect(rl_post_save_receiver, sender = RestaurantLocation)