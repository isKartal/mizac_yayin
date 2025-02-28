# models.py
from django.db import models
from django.contrib.auth.models import User

class ElementType(models.Model):
    name = models.CharField(max_length=50)  # Ateş, Hava, Su, Toprak
    description = models.TextField()
    image = models.ImageField(upload_to='elements/', null=True, blank=True)
    characteristics = models.TextField()
    recommendations = models.TextField()
    
    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE)
    score = models.IntegerField()
    
    def __str__(self):
        return f"{self.text} ({self.element_type.name})"

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    
    # Sonuçlar
    fire_score = models.IntegerField(default=0)
    air_score = models.IntegerField(default=0)
    water_score = models.IntegerField(default=0)
    earth_score = models.IntegerField(default=0)
    
    # Dominant element
    dominant_element = models.ForeignKey(ElementType, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.dominant_element.name}"
    
    def calculate_dominant_element(self):
        scores = {
            'Ateş': self.fire_score,
            'Hava': self.air_score,
            'Su': self.water_score,
            'Toprak': self.earth_score
        }
        
        dominant = max(scores, key=scores.get)
        self.dominant_element = ElementType.objects.get(name=dominant)
        self.save()
