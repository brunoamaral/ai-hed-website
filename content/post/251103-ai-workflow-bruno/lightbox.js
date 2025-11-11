/**
 * Simple Lightbox for images in this post
 * Converts image links that open in new tabs to lightbox functionality
 */

(function() {
  'use strict';

  // CSS for the lightbox
  const style = document.createElement('style');
  style.textContent = `
    .lightbox-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.9);
      z-index: 9999;
      align-items: center;
      justify-content: center;
      animation: fadeIn 0.3s ease-in-out;
    }

    .lightbox-overlay.active {
      display: flex;
    }

    .lightbox-content {
      position: relative;
      max-width: 90%;
      max-height: 90%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .lightbox-image {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      animation: slideIn 0.3s ease-in-out;
    }

    .lightbox-close {
      position: absolute;
      top: 20px;
      right: 30px;
      color: #628c68;
      font-size: 40px;
      font-weight: bold;
      cursor: pointer;
      background: none;
      border: none;
      padding: 0;
      z-index: 10000;
      transition: color 0.2s;
    }

    .lightbox-close:hover {
      color: #7da478;
    }

    .lightbox-nav {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: #628c68;
      font-size: 30px;
      cursor: pointer;
      padding: 10px 20px;
      z-index: 10000;
      transition: color 0.2s;
    }

    .lightbox-nav:hover {
      color: #7da478;
    }

    .lightbox-prev {
      left: 20px;
    }

    .lightbox-next {
      right: 20px;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }

    @keyframes slideIn {
      from {
        transform: scale(0.8);
        opacity: 0;
      }
      to {
        transform: scale(1);
        opacity: 1;
      }
    }

    @media (max-width: 768px) {
      .lightbox-nav {
        font-size: 20px;
        padding: 5px 10px;
      }

      .lightbox-close {
        font-size: 30px;
        top: 10px;
        right: 10px;
      }
    }
  `;
  document.head.appendChild(style);

  // Create lightbox HTML
  const lightboxHTML = `
    <div class="lightbox-overlay" id="lightboxOverlay">
      <div class="lightbox-content">
        <button class="lightbox-close" id="lightboxClose">&times;</button>
        <button class="lightbox-nav lightbox-prev" id="lightboxPrev">&#10094;</button>
        <img class="lightbox-image" id="lightboxImage" src="" alt="">
        <button class="lightbox-nav lightbox-next" id="lightboxNext">&#10095;</button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', lightboxHTML);

  // Get elements
  const overlay = document.getElementById('lightboxOverlay');
  const image = document.getElementById('lightboxImage');
  const closeBtn = document.getElementById('lightboxClose');
  const prevBtn = document.getElementById('lightboxPrev');
  const nextBtn = document.getElementById('lightboxNext');

  let currentImageIndex = 0;
  let lightboxImages = [];

  // Function to open lightbox
  function openLightbox(imageSrc, index) {
    image.src = imageSrc;
    currentImageIndex = index;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  // Function to close lightbox
  function closeLightbox() {
    overlay.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  // Function to show next image
  function showNext() {
    currentImageIndex = (currentImageIndex + 1) % lightboxImages.length;
    image.src = lightboxImages[currentImageIndex];
  }

  // Function to show previous image
  function showPrev() {
    currentImageIndex = (currentImageIndex - 1 + lightboxImages.length) % lightboxImages.length;
    image.src = lightboxImages[currentImageIndex];
  }

  // Event listeners
  closeBtn.addEventListener('click', closeLightbox);
  nextBtn.addEventListener('click', showNext);
  prevBtn.addEventListener('click', showPrev);
  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) {
      closeLightbox();
    }
  });

  // Keyboard navigation
  document.addEventListener('keydown', function(e) {
    if (!overlay.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') showNext();
    if (e.key === 'ArrowLeft') showPrev();
  });

  // Initialize - find all image links in the post
  window.addEventListener('load', function() {
    const imageLinks = document.querySelectorAll('a[href$=".png"], a[href$=".jpg"], a[href$=".jpeg"], a[href$=".gif"], a[href$=".webp"]');
    
    // Filter to only image links that don't go to external sites
    lightboxImages = [];
    const imageElements = [];
    
    imageLinks.forEach((link) => {
      const href = link.getAttribute('href');
      // Only process links to images in this post (relative paths or containing 'images')
      if (href && (href.startsWith('images/') || href.startsWith('./images/'))) {
        lightboxImages.push(href);
        imageElements.push(link);
      }
    });

    // Add click handlers to image links
    imageElements.forEach((link, index) => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        openLightbox(lightboxImages[index], index);
      });
      // Remove target="_blank" to prevent default behavior
      link.removeAttribute('target');
    });

    // Hide navigation buttons if only one image
    if (lightboxImages.length <= 1) {
      prevBtn.style.display = 'none';
      nextBtn.style.display = 'none';
    }
  });
})();
