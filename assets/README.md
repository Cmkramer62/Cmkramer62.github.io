# Portfolio assets

Put your image files and downloadable resume PDF in this folder. For example:

- `cursebreakers-gameplay.jpg`
- `cursebreakers-cover.png`
- `Cameron-Kramer-Resume.pdf`

To show the CURSEBREAKERS image, edit the `feature-media` block in `../index.html` and replace its placeholder contents with:

```html
<img class="feature-image" src="assets/cursebreakers-gameplay.jpg" alt="Describe what is happening in this CURSEBREAKERS gameplay image">
```

Add this rule to `styles.css` so the image fills the media frame:

```css
.feature-media { position: relative; }
.feature-image { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
```

Use the exact same filename (including capitalization and extension) in the image's `src` as the file you put here. JPG, PNG, and WebP are good choices for images. For gameplay video, use a video hosting link or an HTML `<video>` element instead of a very large file in this folder.
