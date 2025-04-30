from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Exists, OuterRef, Prefetch, Q
from testing_algorithm.models import TestResult
from .models import RecommendedContent, UserContentInteraction, ContentCategory

@login_required
def profiles(request):
    """ Profil ana sayfasını gösterir """
    return render(request, 'profiles/profiles.html')

@login_required
def my_temperament(request):
    """Kullanıcının mizaç sonucunu gösterir"""
    test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
    
    if test_result:
        # Element bilgisini al
        dominant_element = test_result.dominant_element
        
        context = {
            'result': test_result,
            'dominant_element': dominant_element,
        }
        return render(request, 'profiles/my_temperament.html', context)
    else:
        # Eğer test sonucu yoksa, kullanıcıya bilgi mesajı göster ve test sayfasına yönlendir
        messages.info(request, "Mizaç sonucunuzu görmek için önce mizaç testini çözmelisiniz.")
        return redirect('test_list')

@login_required
def my_suggestions(request):
    """ Kullanıcıya önerilen içerikleri görüntüler """
    # Kullanıcının test sonucunu al
    test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
    
    # Eğer kullanıcı henüz testi çözmemişse test sayfasına yönlendir
    if not test_result:
        messages.warning(request, "Önerileri görmek için önce mizaç testini çözmelisiniz.")
        return redirect('test_list')
    
    # Kullanıcının etkileşimlerini önceden sorgula
    user_interactions = UserContentInteraction.objects.filter(user=request.user)
    interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
    
    # Test sonucundan dominant element ismini al
    dominant_element_name = test_result.dominant_element.name
    
    # SADECE kullanıcının baskın elementine göre içerik önerilerini al
    # Popüler içerikleri dahil etmiyoruz, SADECE mizaç tipine uygun olanlar gösterilecek
    recommended_contents = RecommendedContent.objects.filter(
        is_active=True, 
        related_element_name=dominant_element_name
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('order', '-created_at')
    
    # İçerikler için etkileşim bilgilerini hazırla
    for content in recommended_contents:
        # Etkileşim bilgisini geçici bir özellik olarak ekle (veritabanı ilişkisini değiştirmeden)
        if content.id in interactions_dict:
            # Kullanıcının bu içerikle etkileşimi varsa, özelliklerini kopyalayalım
            interaction = interactions_dict[content.id]
            content.is_liked = interaction.liked
            content.is_saved = interaction.saved
            content.is_viewed = interaction.viewed
        else:
            # Etkileşim yoksa, varsayılan değerleri ayarla
            content.is_liked = False
            content.is_saved = False
            content.is_viewed = False
            
            # Yeni etkileşim oluştur ve kaydet
            interaction = UserContentInteraction(
                user=request.user,
                content=content,
                liked=False,
                saved=False,
                viewed=False
            )
            interaction.save()
            # Dictionary'ye ekle
            interactions_dict[content.id] = interaction
    
    # Tüm kategorileri al
    categories = ContentCategory.objects.all()
    
    context = {
        'contents': recommended_contents,  # Artık sadece kullanıcının mizacına ait içerikler var
        'categories': categories,
        'dominant_element': dominant_element_name,
    }
    
    # my_suggestions.html şablonunu kullanıyoruz
    return render(request, 'profiles/my_suggestions.html', context)

@login_required
def content_detail(request, content_id):
    """ İçerik detaylarını AJAX ile dönen view """
    content = get_object_or_404(RecommendedContent, id=content_id, is_active=True)
    
    # Kullanıcının içerikle etkileşimini güncelle
    interaction, created = UserContentInteraction.objects.get_or_create(
        user=request.user,
        content=content
    )
    
    if not interaction.viewed:
        interaction.viewed = True
        interaction.viewed_at = timezone.now()
        interaction.save()
    
    # İçeriğin beğeni sayısını hesapla
    like_count = UserContentInteraction.objects.filter(content=content, liked=True).count()
    
    # JSON formatında içerik detaylarını döndür
    data = {
        'id': content.id,
        'title': content.title,
        'content': content.content,
        'image': content.image.url if content.image else None,
        'category': content.category.name,
        'category_id': content.category.id,
        'related_element': content.related_element_name,
        'like_count': like_count,
        'liked': interaction.liked,
        'saved': interaction.saved,
    }
    
    return JsonResponse(data)

@login_required
def toggle_like_content(request, content_id):
    """ İçeriği beğenme/beğenmeme durumunu değiştiren view """
    if request.method == 'POST':
        content = get_object_or_404(RecommendedContent, id=content_id, is_active=True)
        interaction, created = UserContentInteraction.objects.get_or_create(
            user=request.user,
            content=content
        )
        
        # Beğenme durumunu değiştir
        interaction.liked = not interaction.liked
        interaction.save()
        
        # Beğeni sayısını hesapla
        like_count = UserContentInteraction.objects.filter(content=content, liked=True).count()
        
        return JsonResponse({
            'success': True, 
            'liked': interaction.liked,
            'like_count': like_count
        })
    
    return JsonResponse({'success': False}, status=400)

@login_required
def toggle_save_content(request, content_id):
    """ İçeriği kaydetme/kaydetmeme durumunu değiştiren view """
    if request.method == 'POST':
        content = get_object_or_404(RecommendedContent, id=content_id, is_active=True)
        interaction, created = UserContentInteraction.objects.get_or_create(
            user=request.user,
            content=content
        )
        
        # Kaydetme durumunu değiştir
        interaction.saved = not interaction.saved
        interaction.save()
        
        return JsonResponse({'success': True, 'saved': interaction.saved})
    
    return JsonResponse({'success': False}, status=400)

@login_required
def restart_test(request):
    """Kullanıcının test sonuçlarını siler ve test listesi sayfasına yönlendirir"""
    # Kullanıcının tüm test sonuçlarını sil
    TestResult.objects.filter(user=request.user).delete()
    
    # Test oturumundaki verileri temizle
    for key in ['test_phase', 'warm_score', 'cold_score', 'moist_score', 'dry_score', 'test_answers']:
        if key in request.session:
            del request.session[key]
    
    # Başarılı mesajı ekle
    messages.success(request, "Test sonuçlarınız silindi. Şimdi testi yeniden çözebilirsiniz.")
    
    # Test listesi sayfasına yönlendir
    return redirect('test_list')