# models.py
from django.db import models
from django.contrib.auth.models import User

class ElementType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    characteristics = models.TextField()
    
    # Element özellikleri
    is_warm = models.BooleanField(default=False)  # Sıcak/Soğuk
    is_moist = models.BooleanField(default=False)  # Nemli/Kuru
    
    def __str__(self):
        return self.name

class Recommendation(models.Model):
    """Mizaç tiplerine göre öneriler"""
    element = models.ForeignKey(ElementType, on_delete=models.CASCADE, related_name='recommendations')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text='Önerilerin sıralaması için kullanılabilir.')
    
    def __str__(self):
        return f"{self.element.name} - {self.text[:30]}"

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    
    # Soru tipini belirlemek için yeni alan
    QUESTION_TYPE_CHOICES = [
        ('WARM', 'Sıcak/Soğuk Sorusu'),
        ('WARM_MOIST', 'Sıcak Mizaçlar için Nemli/Kuru Sorusu'),
        ('COLD_MOIST', 'Soğuk Mizaçlar için Nemli/Kuru Sorusu'),
    ]
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='WARM')
    
    # Sorunun hangi aşamada gösterileceğini belirlemek için
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.text} ({self.get_question_type_display()})"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    score = models.IntegerField()  # +1 veya -1
    
    def __str__(self):
        return f"{self.text} (Puan: {self.score})"

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    
    # Puanlar
    warm_score = models.IntegerField(default=0)  # Sıcaklık puanı (pozitif = sıcak, negatif = soğuk)
    moist_score = models.IntegerField(default=0)  # Nem puanı (pozitif = nemli, negatif = kuru)
    
    # Sonuç olarak belirlenen element
    dominant_element = models.ForeignKey(ElementType, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.dominant_element.name}"
    
    def calculate_dominant_element(self):
        """Sıcaklık ve nem puanlarına göre dominant elementi belirler"""
        is_warm = self.warm_score >= 0  # 0 veya pozitif = sıcak
        is_moist = self.moist_score >= 0  # 0 veya pozitif = nemli
        
        # Mizaç tiplerini belirle
        if is_warm and not is_moist:  # Sıcak ve Kuru = Ateş
            element_name = "Ateş"
        elif is_warm and is_moist:    # Sıcak ve Nemli = Hava
            element_name = "Hava"
        elif not is_warm and is_moist:  # Soğuk ve Nemli = Su
            element_name = "Su"
        else:  # Soğuk ve Kuru = Toprak
            element_name = "Toprak"
        
        dominant_element = ElementType.objects.filter(name=element_name).first()
        if dominant_element:
            self.dominant_element = dominant_element
            self.save()
        return dominant_element

class TestResultDetail(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='details')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    score = models.IntegerField()
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.score} puan"
    
    class Meta:
        verbose_name = "Test Sonuç Detayı"
        verbose_name_plural = "Test Sonuç Detayları"