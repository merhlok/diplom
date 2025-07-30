from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim,GeocoderNotFound
from django.http import Http404

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    location_query = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Поисковый запрос локации"
    )
    latitude = models.FloatField(
        blank=True, 
        null=True,
        verbose_name="Широта"
    )
    longitude = models.FloatField(
        blank=True, 
        null=True,
        verbose_name="Долгота"
    )
    location_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Название локации"
    )

    def geocode_location(self):
        if not self.location_query:
            return
            
        geolocator = Nominatim(user_agent="social_network")
        try:
            location = geolocator.geocode(self.location_query)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
        except GeocoderNotFound:
            raise Http404('не найдено')

    def reverse_geocode(self):
        if self.latitude and self.longitude:
            geolocator = Nominatim(user_agent="social_network")
            try:
                location = geolocator.reverse((self.latitude, self.longitude))
                if location:
                    self.location_name = location.address
            except GeocoderNotFound:
                raise Http404('не найдено')

    def save(self, *args, **kwargs):
        self.geocode_location()
        self.reverse_geocode()
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pass


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    created_at = models.DateTimeField(auto_now_add=True)
    pass


class ImageModel(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='posts/images/', verbose_name='Изображение')
    pass