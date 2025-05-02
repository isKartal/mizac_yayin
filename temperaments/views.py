from django.shortcuts import render
from testing_algorithm.models import TestResult
from profiles.models import RecommendedContent, UserContentInteraction
from django.db.models import Count, Q

def temperaments(request):
    """Tüm mizaçları gösteren genel sayfa"""
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucunu da gönderelim
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Test sonucundan kullanıcının elementini al
            user_element = test_result.dominant_element
            context = {
                'user_element': user_element,
                'has_test_result': True
            }
        else:
            context = {
                'has_test_result': False
            }
    else:
        context = {
            'has_test_result': False
        }
        
    return render(request, 'temperaments/temperaments.html', context)

def fire_more(request):
    """Ateş mizacı detay sayfası"""
    
    # Ateş mizacı için önerileri getir (en fazla 3 tane)
    # İşlem yapılırken beğeni sayısına göre en popüler içerikler ilk 3'te olacak
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Ateş',
        is_active=True
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('-like_count', '-created_at')[:3]
    
    # Kullanıcının giriş yapmış olması durumunda, beğeni bilgilerini ekle
    if request.user.is_authenticated:
        # Kullanıcının etkileşimlerini al
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        # İçerikler için etkileşim bilgilerini hazırla
        for content in element_suggestions:
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
    
    context = {
        'element_name': 'Ateş',
        'element_suggestions': element_suggestions,
    }
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Ateş"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
        
    return render(request, 'temperaments/fire_more.html', context)

def water_more(request):
    """Su mizacı detay sayfası"""
    
    # Su mizacı için önerileri getir (en fazla 3 tane)
    # İşlem yapılırken beğeni sayısına göre en popüler içerikler ilk 3'te olacak
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Su',
        is_active=True
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('-like_count', '-created_at')[:3]
    
    # Kullanıcının giriş yapmış olması durumunda, beğeni bilgilerini ekle
    if request.user.is_authenticated:
        # Kullanıcının etkileşimlerini al
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        # İçerikler için etkileşim bilgilerini hazırla
        for content in element_suggestions:
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
    
    context = {
        'element_name': 'Su',
        'element_suggestions': element_suggestions,
    }
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Su"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
        
    return render(request, 'temperaments/water_more.html', context)

def air_more(request):
    """Hava mizacı detay sayfası"""
    
    # Hava mizacı için önerileri getir (en fazla 3 tane)
    # İşlem yapılırken beğeni sayısına göre en popüler içerikler ilk 3'te olacak
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Hava',
        is_active=True
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('-like_count', '-created_at')[:3]  
    
    # Kullanıcının giriş yapmış olması durumunda, beğeni bilgilerini ekle
    if request.user.is_authenticated:
        # Kullanıcının etkileşimlerini al
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        # İçerikler için etkileşim bilgilerini hazırla
        for content in element_suggestions:
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
    
    context = {
        'element_name': 'Hava',
        'element_suggestions': element_suggestions,
    }
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Hava"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
        
    return render(request, 'temperaments/air_more.html', context)

def earth_more(request):
    """Toprak mizacı detay sayfası"""
    
    # Toprak mizacı için önerileri getir (en fazla 3 tane)
    # İşlem yapılırken beğeni sayısına göre en popüler içerikler ilk 3'te olacak
    element_suggestions = RecommendedContent.objects.filter(
        related_element_name='Toprak',
        is_active=True
    ).annotate(
        like_count=Count('user_interactions', filter=Q(user_interactions__liked=True))
    ).order_by('-like_count', '-created_at')[:3]
    
    # Kullanıcının giriş yapmış olması durumunda, beğeni bilgilerini ekle
    if request.user.is_authenticated:
        # Kullanıcının etkileşimlerini al
        user_interactions = UserContentInteraction.objects.filter(user=request.user)
        interactions_dict = {interaction.content_id: interaction for interaction in user_interactions}
        
        # İçerikler için etkileşim bilgilerini hazırla
        for content in element_suggestions:
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
    
    context = {
        'element_name': 'Toprak',
        'element_suggestions': element_suggestions,
    }
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Toprak"
            context.update({
                'is_users_element': is_users_element,
                'has_test_result': True,
                'dominant_element': test_result.dominant_element
            })
        else:
            context.update({
                'has_test_result': False
            })
    else:
        context.update({
            'has_test_result': False
        })
        
    return render(request, 'temperaments/earth_more.html', context)