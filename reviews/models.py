from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Create your models here.

class Review(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.CASCADE)
  title = models.CharField(max_length=80)
  content = models.TextField()
  movie_name = models.CharField(max_length=30)
  grade = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(500, 400)],
                                format='JPEG',
                                options={'quality': 60})