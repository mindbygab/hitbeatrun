# HitBeatRun — static website (hitbeatrun.com)

A self-contained copy of the Wix site, with every image and video stored locally in `assets/`.
No Wix, no hosting bill.

| Page | File |
|---|---|
| Main site (hitbeatrun.com) | `index.html` |
| Fourthwall subscription landing page (same design) | `subscribe/index.html` → hitbeatrun.com/subscribe/ |
| 8 song workout videos | `songs/*.html` |
| Terms of Service + Privacy Policy | on Fourthwall (footer links); `legal.html` forwards there |

## 1. Set your links (once)
Open `assets/js/main.js` and edit the three values at the top:
- `FOURTHWALL_URL` – where every "Let's Run" button goes (https://members-hitbeatrun-shop.fourthwall.com)
- `FOURTHWALL_LOGIN` – where "Log In" goes (members watch the videos on Fourthwall)
- `CONTACT_EMAIL` – shown in the footer and on the Music & Credits page (mindbygab@gmail.com)
- `FORM_ENDPOINT` – optional (e.g. a free Formspree form) so the newsletter form submit without opening the visitor's email app

Put the research paper PDF at `assets/docs/HitBeatRun-Research-Paper.pdf` (the "Download it!" button points there).

## 2. Edit text
All page markup comes from `tools/build.py`. Change text there, then run:

    python3 tools/build.py

Styles live in `assets/css/style.css`.

## 3. Publish for free (GitHub Pages)
1. Create a free GitHub account and a new **public** repository called `hitbeatrun`.
2. Upload everything in this folder (or `git push`).
3. Repo → Settings → Pages → Source: *Deploy from a branch* → `main` / root → Save.
4. Custom domain: `hitbeatrun.com` (the `CNAME` file is already here). Tick **Enforce HTTPS** once it appears.
5. At your domain registrar, add DNS records:
   - `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `<your-github-username>.github.io`

Every video is under 25 MB, so Cloudflare Pages or Netlify (both free) also work if you prefer them.

Original full-quality media from Wix is kept outside the site in `../hitbeatrun-originals/`.
