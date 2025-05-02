document.addEventListener('DOMContentLoaded', function() {
    // Kullanıcının giriş yapmış olup olmadığını daha güvenilir bir şekilde kontrol et
    // Birkaç farklı yöntem deneyerek kullanıcı giriş durumunu tespit et
    const userElement = document.querySelector('.user-info') || 
                        document.getElementById('user-dropdown') || 
                        document.querySelector('.logged-in-user');
    
    // Sayfada kullanıcı bilgilerini içeren meta tag ekleyebiliriz
    // <meta name="user-auth-status" content="authenticated">
    const metaAuth = document.querySelector('meta[name="user-auth-status"]');
    
    // HTML body'sine class ekleyebiliriz: <body class="authenticated">
    const bodyAuth = document.body.classList.contains('authenticated');
    
    // Herhangi bir kullanıcı bilgisi elementi veya sınıfı bulunduysa kullanıcı giriş yapmış demektir
    const isAuthenticated = userElement !== null || 
                           (metaAuth && metaAuth.getAttribute('content') === 'authenticated') || 
                           bodyAuth;
    
    console.log("Kullanıcı giriş durumu:", isAuthenticated ? "Giriş yapılmış" : "Giriş yapılmamış");
    
    // Öneri kartlarına tıklama olayı ekle
    const suggestionCards = document.querySelectorAll('.suggestion-card');
    suggestionCards.forEach(card => {
      card.addEventListener('click', function(e) {
        // Eğer tıklanan eleman bir buton değilse modal aç
        if (!e.target.closest('.suggestion-button')) {
          const contentId = this.dataset.contentId;
          openContentModal(contentId);
          // Sayfa yönlendirmesini engelle
          e.preventDefault();
          return false;
        }
      });
    });
    
    // Beğenme butonlarına tıklama olayı ekle
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation(); // Olay yayılımını durdur
        
        // Kullanıcı giriş yapmamışsa, giriş sayfasına yönlendir
        if (!isAuthenticated) {
          alert('Beğenmek için giriş yapmanız gerekmektedir.');
          window.location.href = '/accounts/login/?next=' + window.location.pathname;
          return;
        }
        
        const contentId = this.dataset.contentId;
        toggleLike(contentId, this);
      });
    });
    
    // Devamını Oku butonlarına tıklama olayı ekle
    const readMoreButtons = document.querySelectorAll('.read-more');
    readMoreButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation(); // Olay yayılımını durdur
        const contentId = this.dataset.contentId;
        openContentModal(contentId);
      });
    });
    
    // Modal kapat butonuna tıklama olayı ekle
    const closeModalBtn = document.getElementById('closeModal');
    if (closeModalBtn) {
      closeModalBtn.addEventListener('click', function() {
        const contentModal = document.getElementById('contentModal');
        contentModal.classList.remove('active');
        document.body.style.overflow = '';
      });
    }
    
    // Modal dışına tıklama ile kapatma
    const contentModal = document.getElementById('contentModal');
    if (contentModal) {
      contentModal.addEventListener('click', function(e) {
        if (e.target === contentModal) {
          contentModal.classList.remove('active');
          document.body.style.overflow = '';
        }
      });
    }
    
    // Modal butonlarına olay ekle
    const modalLikeBtn = document.getElementById('modalLikeBtn');
    if (modalLikeBtn) {
      modalLikeBtn.addEventListener('click', function() {
        // Kullanıcı giriş yapmamışsa, giriş sayfasına yönlendir
        if (!isAuthenticated) {
          alert('Beğenmek için giriş yapmanız gerekmektedir.');
          window.location.href = '/accounts/login/?next=' + window.location.pathname;
          return;
        }
        
        const contentId = this.dataset.contentId;
        toggleLike(contentId, this);
      });
    }
    
    const modalSaveBtn = document.getElementById('modalSaveBtn');
    if (modalSaveBtn) {
      modalSaveBtn.addEventListener('click', function() {
        // Kullanıcı giriş yapmamışsa, giriş sayfasına yönlendir
        if (!isAuthenticated) {
          alert('Kaydetmek için giriş yapmanız gerekmektedir.');
          window.location.href = '/accounts/login/?next=' + window.location.pathname;
          return;
        }
        
        const contentId = this.dataset.contentId;
        toggleSave(contentId, this);
      });
    }
    
    // İçerik modalını açma fonksiyonu
    function openContentModal(contentId) {
      console.log("Opening modal for content ID: " + contentId);
  
      // İçeriği AJAX ile çek
      fetch(`/profiles/content/${contentId}/detail/`)
        .then(response => {
          // Hata durumunda
          if (!response.ok) {
            if (response.status === 403) {
              throw new Error('İçeriği görüntülemek için giriş yapmanız gerekebilir');
            } else {
              throw new Error('İçerik yüklenirken hata oluştu');
            }
          }
          return response.json();
        })
        .then(data => {
          console.log("Received data:", data);
          
          // Modal başlığını ayarla
          document.getElementById('modalTitle').textContent = data.title;
          
          // Kategori bilgisini göster
          document.getElementById('modalCategory').textContent = data.category;
          
          // İçeriği göster
          document.getElementById('modalContent').innerHTML = data.content;
          
          // Element bilgisini göster
          document.getElementById('modalElement').textContent = data.related_element;
          document.getElementById('modalElement').className = `modal-element ${data.related_element.toLowerCase()}`;
          
          // Beğenme ve kaydetme butonlarını kullanıcı durumuna göre ayarla
          if (isAuthenticated) {
            // Beğenme durumunu güncelle
            const likeBtn = document.getElementById('modalLikeBtn');
            likeBtn.dataset.contentId = contentId;
            likeBtn.className = `modal-action-btn${data.liked ? ' liked' : ''}`;
            likeBtn.innerHTML = data.liked ? 
              '<i class="fas fa-heart"></i> Beğenildi' : 
              '<i class="far fa-heart"></i> Beğen';
            
            // Kaydetme durumunu güncelle
            const saveBtn = document.getElementById('modalSaveBtn');
            saveBtn.dataset.contentId = contentId;
            saveBtn.className = `modal-action-btn${data.saved ? ' saved' : ''}`;
            saveBtn.innerHTML = data.saved ? 
              '<i class="fas fa-bookmark"></i> Kaydedildi' : 
              '<i class="far fa-bookmark"></i> Kaydet';
          } else {
            // Giriş yapmamış kullanıcılar için butonları farklı göster
            const likeBtn = document.getElementById('modalLikeBtn');
            likeBtn.dataset.contentId = contentId;
            likeBtn.className = 'modal-action-btn';
            likeBtn.innerHTML = '<i class="far fa-heart"></i> Giriş Yap & Beğen';
            
            const saveBtn = document.getElementById('modalSaveBtn');
            saveBtn.dataset.contentId = contentId;
            saveBtn.className = 'modal-action-btn';
            saveBtn.innerHTML = '<i class="far fa-bookmark"></i> Giriş Yap & Kaydet';
          }
          
          // Modalı göster
          const modal = document.getElementById('contentModal');
          modal.classList.add('active');
          document.body.style.overflow = 'hidden';
          
          console.log("Modal should be active now");
        })
        .catch(error => {
          console.error('Hata:', error);
          alert(error.message || 'İçerik yüklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.');
        });
    }
    
    // Beğenme işlevi
    function toggleLike(contentId, button) {
      fetch(`/profiles/content/${contentId}/toggle_like/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Beğenme durumunu güncelle
          updateLikeStatus(contentId, data.liked, data.like_count);
        }
      })
      .catch(error => console.error('Hata:', error));
    }
    
    // Kaydetme işlevi
    function toggleSave(contentId, button) {
      fetch(`/profiles/content/${contentId}/toggle_save/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Kaydetme durumunu güncelle
          updateSaveStatus(contentId, data.saved);
        }
      })
      .catch(error => console.error('Hata:', error));
    }
    
    // Beğenme durumunu güncelle
    function updateLikeStatus(contentId, isLiked, likeCount) {
      // Kart butonlarını güncelle
      const likeButtons = document.querySelectorAll(`.like-button[data-content-id="${contentId}"]`);
      likeButtons.forEach(btn => {
        btn.classList.toggle('liked', isLiked);
        const icon = btn.querySelector('i');
        icon.className = isLiked ? 'fas fa-heart' : 'far fa-heart';
        
        const countSpan = btn.querySelector('.like-count');
        if (countSpan) {
          countSpan.textContent = likeCount;
        }
      });
      
      // Modal butonunu güncelle
      const modalLikeBtn = document.getElementById('modalLikeBtn');
      if (modalLikeBtn && modalLikeBtn.dataset.contentId === contentId) {
        modalLikeBtn.classList.toggle('liked', isLiked);
        modalLikeBtn.innerHTML = isLiked ? 
          '<i class="fas fa-heart"></i> Beğenildi' : 
          '<i class="far fa-heart"></i> Beğen';
      }
    }
    
    // Kaydetme durumunu güncelle
    function updateSaveStatus(contentId, isSaved) {
      // Modal butonunu güncelle
      const modalSaveBtn = document.getElementById('modalSaveBtn');
      if (modalSaveBtn && modalSaveBtn.dataset.contentId === contentId) {
        modalSaveBtn.classList.toggle('saved', isSaved);
        modalSaveBtn.innerHTML = isSaved ? 
          '<i class="fas fa-bookmark"></i> Kaydedildi' : 
          '<i class="far fa-bookmark"></i> Kaydet';
      }
    }
    
    // CSRF token'ı almak için yardımcı fonksiyon
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    
    // Animasyon için IntersectionObserver
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('appear');
        }
      });
    }, { threshold: 0.1 });
    
    // Animasyon için öğeleri gözlemle
    const animatedElements = document.querySelectorAll('.suggestion-card, .water-personality-text, .water-personality-image, .fire-personality-text, .fire-personality-image, .air-personality-text, .air-personality-image, .earth-personality-text, .earth-personality-image');
    
    animatedElements.forEach(el => {
      observer.observe(el);
    });
  });