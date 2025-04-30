from django.db import models
from django.contrib.auth.models import User

class ContentCategory(models.Model):
    """İçerik kategorileri için model"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    
    class Meta:
        verbose_name = "İçerik Kategorisi"
        verbose_name_plural = "İçerik Kategorileri"
    
    def __str__(self):
        return self.name

class RecommendedContent(models.Model):
    """Önerilen içerikler için model"""
    ELEMENT_CHOICES = [
        ('Ateş', 'Ateş'),
        ('Hava', 'Hava'),
        ('Su', 'Su'),
        ('Toprak', 'Toprak'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Başlık")
    short_description = models.TextField(verbose_name="Kısa Açıklama")
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(upload_to='content_images/', blank=True, null=True, verbose_name="Görsel")
    category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE, related_name="contents", verbose_name="Kategori")
    related_element_name = models.CharField(
        max_length=50, 
        verbose_name="İlgili Mizaç Elementi", 
        choices=ELEMENT_CHOICES,
        help_text="Ateş, Hava, Su veya Toprak değerlerinden birini seçin"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Önerilen İçerik"
        verbose_name_plural = "Önerilen İçerikler"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class UserContentInteraction(models.Model):
    """Kullanıcı içerik etkileşimleri için model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="content_interactions", verbose_name="Kullanıcı")
    content = models.ForeignKey(RecommendedContent, on_delete=models.CASCADE, related_name="user_interactions", verbose_name="İçerik")
    viewed = models.BooleanField(default=False, verbose_name="Görüntülendi mi?")
    liked = models.BooleanField(default=False, verbose_name="Beğenildi mi?")
    saved = models.BooleanField(default=False, verbose_name="Kaydedildi mi?")
    viewed_at = models.DateTimeField(blank=True, null=True, verbose_name="Görüntülenme Tarihi")
    
    class Meta:
        verbose_name = "Kullanıcı İçerik Etkileşimi"
        verbose_name_plural = "Kullanıcı İçerik Etkileşimleri"
        unique_together = ['user', 'content']
    
    def __str__(self):
        return f"{self.user.username} - {self.content.title}"