// Expand project images into a native dialog. Escape, the close control,
// the image itself, or the dark backdrop closes the expanded view.
const projectImages = document.querySelectorAll('.detail-feature img, .detail-gallery img');

if (projectImages.length && typeof HTMLDialogElement !== 'undefined') {
  const lightbox = document.createElement('dialog');
  lightbox.className = 'image-lightbox';
  lightbox.setAttribute('aria-label', 'Expanded project image');
  lightbox.innerHTML = `
    <button class="lightbox-close" type="button" aria-label="Close expanded image">×</button>
    <img class="lightbox-image" alt="">
  `;
  document.body.append(lightbox);

  const enlargedImage = lightbox.querySelector('.lightbox-image');
  const closeButton = lightbox.querySelector('.lightbox-close');
  const motionDuration = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 180;
  let lastTrigger = null;
  let isClosing = false;

  function openImage(image) {
    if (lightbox.open) return;
    lastTrigger = image;
    enlargedImage.src = image.currentSrc || image.src;
    enlargedImage.alt = image.alt;
    image.setAttribute('aria-expanded', 'true');
    lightbox.showModal();
    closeButton.focus();
    requestAnimationFrame(() => lightbox.classList.add('is-visible'));
  }

  function closeImage() {
    if (!lightbox.open || isClosing) return;
    isClosing = true;
    lightbox.classList.remove('is-visible');
    window.setTimeout(() => lightbox.close(), motionDuration);
  }

  projectImages.forEach((image) => {
    image.classList.add('expandable-image');
    image.tabIndex = 0;
    image.setAttribute('role', 'button');
    image.setAttribute('aria-haspopup', 'dialog');
    image.setAttribute('aria-expanded', 'false');
    image.setAttribute('aria-label', `Expand image: ${image.alt || 'Project image'}`);
    image.addEventListener('click', () => openImage(image));
    image.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openImage(image);
      }
    });
  });

  closeButton.addEventListener('click', closeImage);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox || event.target === enlargedImage) closeImage();
  });
  lightbox.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeImage();
  });
  lightbox.addEventListener('close', () => {
    isClosing = false;
    if (lastTrigger) {
      lastTrigger.setAttribute('aria-expanded', 'false');
      lastTrigger.focus();
    }
  });
}
