# Phucprofilo - Personal Portfolio Website

## Overview
This is a personal portfolio and resume website for Le Huu Phuc, featuring a modern, responsive design with smooth animations and a professional layout. The site showcases portfolio work, skills, resume, and contact information.

## Project Architecture

### Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Python 3.11 Simple HTTP Server
- **Styling**: Bootstrap CSS, Custom CSS
- **Animations**: GSAP (GreenSock Animation Platform)
- **Icons**: Phosphor Icons, Font Awesome
- **Libraries**: 
  - Lenis (smooth scrolling)
  - PhotoSwipe (image gallery)
  - imagesLoaded (image loading detection)

### Project Structure
```
.
├── css/                    # Stylesheets
│   ├── loaders/           # Loading animation styles
│   ├── main.css           # Main styles
│   └── plugins.css        # Plugin styles
├── fonts/                 # Font files (Phosphor, Font Awesome)
├── img/                   # Images and assets
│   ├── backgrounds/       # Background images
│   ├── demo/             # Demo images
│   ├── favicon/          # Favicon files
│   └── icons/            # Icon assets
├── js/                    # JavaScript files
│   ├── demo/             # Demo scripts
│   ├── app.js            # Main application script
│   ├── gallery-init.js   # Gallery initialization
│   └── libs.min.js       # Minified libraries
├── index.html            # Main page (English - gradient background)
├── index-vi.html         # Vietnamese version with full translations
├── index-demo.html       # Demo version
├── index-image.html      # Image background version
├── index-solid-color.html # Solid color version
├── index-svg.html        # SVG background version
├── mail.php              # Contact form handler (PHP)
└── server.py             # Python web server
```

## Recent Changes (October 2025)

### Initial Setup for Replit Environment
1. Installed Python 3.11 for running the web server
2. Created .gitignore file with Python-specific entries
3. Configured workflow to run server on port 5000
4. Fixed broken image references in index.html:
   - Replaced missing Adobe Premiere Pro icon with Figma icon
   - Replaced missing Adobe After Effects icon with Sketch icon
5. Updated avatar image with user's personal profile photo (attached_assets/profife_1759309704650.png)
6. Added dynamic avatar switching based on theme:
   - Light mode: Professional profile photo
   - Dark mode: Artistic portrait with purple/orange tones
7. Set up autoscale deployment configuration

### Vietnamese Localization (October 2025)
1. Created full Vietnamese version (index-vi.html) with comprehensive translations:
   - All navigation menus and section titles
   - Hero headline and tagline
   - Portfolio project descriptions (4 projects with detailed context)
   - About Me service cards (4 services)
   - Skills section and technical tools
   - Resume timeline and job descriptions
   - Contact form and footer
   - Meta tags and page title
2. Added language switcher in header:
   - EN button links to index.html
   - VI button links to index-vi.html
3. Replaced all 8 placeholder images with real project assets:
   - Brand Guidelines, Corporate Event, Marketing Campaign, Website Projects
   - Trade Marketing, Event Activation, Digital Marketing, Brand Identity

### CV Download Feature (October 2025)
1. Added downloadable CV files (English and Vietnamese versions) to website
2. CV file locations:
   - English: `assets/Le_Huu_Phuc_CV.pdf`
   - Vietnamese: `assets/Le_Huu_Phuc_CV_VI.pdf`
3. Download buttons integrated in two locations per page:
   - Hero section (main homepage)
   - About Me section
4. Language-specific CVs:
   - English page (index.html) downloads English CV
   - Vietnamese page (index-vi.html) downloads Vietnamese CV
5. Files automatically download when clicked

## Configuration

### Development Server
- **Host**: 0.0.0.0
- **Port**: 5000
- **Features**:
  - Socket reuse enabled for fast restarts
  - Cache-Control headers to prevent caching issues
  - Serves static files from project root

### Deployment
- **Type**: Autoscale
- **Command**: `python server.py`
- **Best for**: Static websites with no persistent state needed

## Portfolio Content
- **Name**: Le Huu Phuc
- **Specialization**: Marketing, Branding & Distribution Strategy
- **Location**: Ha Noi, Viet Nam
- **Skills**: Photoshop, Illustrator, Figma, Sketch, Blender, HTML5, CSS3

## Email Functionality (October 2025)
The contact form now works via SMTP email:
- **Backend**: Flask server with /send-email endpoint
- **Security**: Hardcoded admin recipient, input validation, HTML sanitization, SSL/TLS
- **Configuration**: Uses SMTP_EMAIL and SMTP_PASSWORD environment variables
- **Default SMTP**: Gmail (smtp.gmail.com:587)
- **Recipient**: lehuuphuc.ht2016@gmail.com

### SMTP Setup
To use Gmail:
1. Go to https://myaccount.google.com/apppasswords
2. Create an App Password for "Mail"
3. Set SMTP_EMAIL to your Gmail address
4. Set SMTP_PASSWORD to the 16-character app password

## Cleanup History (October 2025)
Removed unused files to optimize project size:
- Deleted demo folders: `img/demo/`, `js/demo/` (~2.4MB)
- Removed unused attached_assets files (~3.6MB)
- **Total saved: ~5MB** (188MB → 183MB)

## Known Issues
- Minor GSAP warning about `.animate-card-3` selector not found (does not affect functionality)

## Notes
- The site uses imagesLoaded library to wait for all images before hiding the loader
- Multiple HTML versions available for different background styles
- Contact form uses secure SMTP backend with proper validation and sanitization
