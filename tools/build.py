#!/usr/bin/env python3
"""Builds every HTML page of the HitBeatRun site from one template.

    python3 tools/build.py

Outputs (relative to the site root):
    index.html                 main site (hitbeatrun.com)
    subscribe/index.html       Fourthwall subscription landing page (same design)
    songs/index.html, songs/<slug>.html
    become-a-sponsor.html, terms-and-conditions.html, privacy-policy.html,
    refund-policy.html, accessibility-statement.html
"""
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent


def ver(rel):
    """Cache-busting tag: changes whenever the file changes, so browsers fetch the new version."""
    import hashlib
    return hashlib.md5((SITE / rel).read_bytes()).hexdigest()[:8]

SONGS = [
    # slug, title, artist, cover, video, page heading (as on Wix)
    ("where-you-are", "Where You Are (GRiZ Remix)", "John Summit & Hayla", "cover-whereyouare.jpg", "song-where-you-are", "John Summit & Hayla - Where You Are"),
    ("hide-u", "Hide U (Tinlicker Remix)", "Sian Evans", "cover-hideu.jpg", "song-hide-u", "Sian Evans - Hide U (Tinlicker Remix)"),
    ("jungle", "Jungle (Arcando Remix)", "Alok, The Chainsmokers & Mae Stephens", "cover-jungle.webp", "song-jungle", "Jungle - Alok, The Chainsmokers & Mae Stephens"),
    ("hiding", "Hiding", "Avaion (Human remix)", "cover-hiding.jpg", "song-hiding", "Hiding - Avaion (Human remix)"),
    ("leave-it-all-behind", "Leave It All Behind", "Alex LeMirage", "cover-leaveit.jpg", "song-leave-it-all-behind", "Leave It All Behind - Alex LeMirage"),
    ("love-is-gone", "Love is Gone (Kaskade Remix)", "Slander & Dylan Matthew", "cover-loveisgone.jpg", "song-love-is-gone", "Slander & Dylan - Love is Gone (Kaskade)"),
    ("ocean", "Ocean", "Fisher & AR/CO", "cover-ocean.jpg", "song-ocean", "Ocean - Fisher & AR/CO"),
    ("bring-me-joy", "Bring Me Joy", "Rudimental & Karen Harding", "cover-bringmejoy.jpg", "song-bring-me-joy", "Bring Me Joy - Rudimental, Karen Harding"),
]

RUN = "Let's Run"
LABELS = {
    "main": {"tickets": RUN, "get": RUN, "buy": RUN},
    "landing": {"tickets": RUN, "get": RUN, "buy": RUN},
}

CURSOR = ('<svg class="cursor" style="{style}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
          'stroke-linejoin="round"><path d="M4 3l16 7-7 2.5L10.5 20z"/></svg>')


def head(R, title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="https://hitbeatrun.com/assets/img/hero-logo.png">
<link rel="icon" href="{R}assets/img/hero-logo.png">
<link rel="stylesheet" href="{R}assets/css/style.css?v={ver("assets/css/style.css")}">
</head>"""


def header(R, mode, home_active=True):
    L = LABELS[mode]
    home = f"{R}index.html" if mode == "main" else "./"
    song_links = "".join(f'<a href="{R}songs/{s[0]}.html">{escape(s[5])}</a>' for s in SONGS)
    return f"""<header class="site-header">
  <a class="logo" href="{home}" aria-label="Home"><img src="{R}assets/img/logo-mind.png" alt="Mind by Gab"></a>
  <nav class="nav" aria-label="Main">
    <a href="{home}" data-home{' class="active"' if home_active else ''}>Home</a>
    <span class="dd"><a href="{R}songs/">Songs</a><span class="dd-menu"><div>{song_links}</div></span></span>
    <a href="{home}#speakers">Speakers</a>
  </nav>
  <div class="header-right">
    <a class="login" href="#" data-fourthwall>Log In</a>
    <a class="btn btn-outline btn-run" href="#" data-cta>{L['tickets']}</a>
    <button class="burger" aria-label="Menu">&#9776;</button>
  </div>
</header>"""


def footer(R, mode):
    L = LABELS[mode]
    home = f"{R}index.html" if mode == "main" else "./"
    song_links = "".join(f'<a href="{R}songs/{s[0]}.html">{escape(s[5])}</a>' for s in SONGS)
    return f"""<footer class="site-footer">
  <div class="foot">
    <div class="f-nav">
      <div class="badge"><img src="{R}assets/img/icon-x.png" alt=""></div>
      <nav>
        <a href="{home}">Home</a>
        <details><summary>Songs <span>&#8964;</span></summary>{song_links}</details>
        <a href="{home}#speakers">Speakers</a>
      </nav>
      <div class="legal">
        <a href="{R}terms-and-conditions.html">Terms &amp; Conditions</a>
        <a href="{R}privacy-policy.html">Privacy Policy</a>
        <a href="{R}refund-policy.html">Refund Policy</a>
        <a href="{R}accessibility-statement.html">Accessibility statement</a>
        <a class="btn btn-black" href="{R}become-a-sponsor.html">Become a Sponsor</a>
      </div>
    </div>
    <div class="f-mid">
      <div class="f-tickets"><a href="#" data-cta><span>&#8853;</span> {L['buy']}</a></div>
      <div class="f-social">
        <a href="https://www.facebook.com/hitbeatrun" target="_blank" rel="noopener" aria-label="HitBeatRun on Facebook"><svg viewBox="0 0 24 24"><path d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.6c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1v1.9H8v3.2h2.6V21H14v-9.3h2.6l.4-3.2z"/></svg></a>
        <a href="https://www.instagram.com/hitbeatrun" target="_blank" rel="noopener" aria-label="HitBeatRun on Instagram"><svg viewBox="0 0 24 24"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm4.9-8.9a1.1 1.1 0 1 0 0 2.2 1.1 1.1 0 0 0 0-2.2zM21.9 7.6c-.1-1.6-.4-3-1.6-4.2S17.7 1.9 16.1 1.8C14.5 1.7 9.5 1.7 7.9 1.8 6.3 1.9 4.9 2.2 3.7 3.4S2.1 6 2 7.6c-.1 1.6-.1 6.6 0 8.2.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.6.1 6.6.1 8.2 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.2-1.6.2-6.6.1-8.2zm-2.1 9.9a3.2 3.2 0 0 1-1.8 1.8c-1.3.5-4.3.4-5.7.4s-4.4.1-5.7-.4a3.2 3.2 0 0 1-1.8-1.8c-.5-1.3-.4-4.3-.4-5.7s-.1-4.4.4-5.7A3.2 3.2 0 0 1 6.6 4.3c1.3-.5 4.3-.4 5.7-.4s4.4-.1 5.7.4a3.2 3.2 0 0 1 1.8 1.8c.5 1.3.4 4.3.4 5.7s.1 4.4-.4 5.7z"/></svg></a>
      </div>
    </div>
    <div class="f-contact">
      <h3>Contact Us</h3>
      <p>For any questions please e-mail<br><a href="#" data-email></a></p>
      <img class="c-img" src="{R}assets/img/footer-c.png" alt="">
      <div class="bottom">
        <p>HitBeatRun<br>Running to the Beat</p>
        <p>&copy; 2026 HitBeatRun by Mind by Gab.</p>
      </div>
    </div>
  </div>
</footer>
<script src="{R}assets/js/main.js?v={ver("assets/js/main.js")}"></script>
</body>
</html>
"""


def bg_video(R, name, poster, cls=""):
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<video{cls_attr} data-src="{R}assets/video/{name}.mp4" '
            f'poster="{R}assets/img/{poster}" muted loop playsinline preload="none"></video>')


def home_page(R, mode):
    L = LABELS[mode]
    S = {s[0]: s for s in SONGS}
    song_rows = "".join(
        f"""<div class="song reveal"><img src="{R}assets/img/{s[3]}" alt="" loading="lazy">
        <div class="meta"><div class="t">{escape(s[1])}</div><div class="a">{escape(s[2])}</div></div>
        <a class="btn btn-outline" href="{R}songs/{s[0]}.html">Play</a></div>"""
        for s in SONGS)
    title = "HitBeatRun | Boost Your Workout by Running to the Beat"
    if mode == "landing":
        title = "Join HitBeatRun | Running to the Beat Video Subscription"
    desc = "HitBeatRun is a running algorithm that syncs your pace to the BPM and energy of the music. Run to the beat."
    return head(R, title, desc) + f"""
<body data-root="{R}" data-mode="{mode}">
{header(R, mode)}
<main>

<!-- ================= HERO ================= -->
<section class="hero">
  <div class="hero-glow"></div>
  <div class="hero-grid"></div>
  <div class="orbits"><div class="orbit orbit-1"><i></i></div><div class="orbit orbit-2"><i></i></div></div>
  <div class="hero-top">
    <h1>HitBeatRun</h1>
    <p class="tagline">Boost Your Workout by<br>Running to the Beat</p>
    <div class="logo-stage">
      <span class="pulse"></span><span class="pulse"></span><span class="pulse"></span>
      <img class="hero-logo" src="{R}assets/img/hero-logo.png" alt="HitBeatRun runner logo">
    </div>
    <div class="slot par s-tech"><p class="pill pill-tech">#Tech</p></div>
    <div class="slot par s-run"><p class="pill pill-run">#Running</p></div>
    <div class="slot par s-bpm"><p class="pill bpm"><b></b>128 BPM</p></div>
    <div class="slot par s-energy"><img class="float-icon" src="{R}assets/img/icon-energy.png" alt=""></div>
    <div class="slot par s-music"><img class="float-icon" src="{R}assets/img/icon-music.png" alt=""></div>
    <div class="slot par s-watch"><img class="float-icon" src="{R}assets/img/icon-watch.png" alt=""></div>
    <div class="slot par s-drink"><img class="float-icon" src="{R}assets/img/icon-drink.png" alt=""></div>
    <div class="slot par s-cur1">{CURSOR.format(style="", color="#da44c1")}</div>
    <div class="slot par s-cur2">{CURSOR.format(style="", color="#fff")}</div>
  </div>

  <div class="stack">
    <article class="stack-card"><header class="g1"><img src="{R}assets/img/icon-brain.png" alt=""><h2>The Science Behind Running to the Beat</h2></header>
      {bg_video(R, "hero-science", "poster-1a175681.jpg")}</article>
    <article class="stack-card"><header class="g2"><img src="{R}assets/img/icon-x.png" alt=""><h2>Integrating HITBEATRUN In Your Daily Workout</h2></header>
      {bg_video(R, "hero-integrating", "poster-5d27d50d.jpg")}</article>
    <article class="stack-card"><header class="g3"><img src="{R}assets/img/icon-o.png" alt=""><h2>1500+<br>Students Using Hitbeatrun</h2></header>
      {bg_video(R, "hero-students", "poster-55d00e39.jpg")}</article>
    <article class="stack-card"><header class="g4"><img src="{R}assets/img/icon-344.png" alt=""><h2>New Songs Analyzed with<br>HITBEATRUN Algorithm</h2></header>
      {bg_video(R, "hero-newsongs", "poster-061d9c62.jpg")}</article>
  </div>
  <div class="hero-cta"><a class="btn btn-white btn-run" href="#" data-cta>{L['get']}</a></div>
</section>

<!-- ================= RUN BANNER ================= -->
<section class="run-banner reveal">
  <h2>Ready to transform your running game?</h2>
  <p>Learn how to set your running speeds, sync with the energy of the music, and optimize every workout for maximum results.</p>
  <a class="btn btn-black btn-run" href="#" data-cta>{RUN}</a>
</section>

<!-- ================= PRICING (Fourthwall membership) ================= -->
<section class="pricing" id="join">
  <div class="intro reveal">
    <span class="eyebrow">HitBeatRun Membership</span>
    <h2>Run every song <span>to the beat.</span></h2>
    <p>Get every HitBeatRun guided running video, with your speed changes timed to the energy of the music. New songs are added as they're analyzed with the HitBeatRun algorithm.</p>
  </div>
  <div class="price-card reveal">
    <div class="inner">
      <div class="tier">Monthly</div>
      <div class="amount"><sup>$</sup>4.99</div>
      <div class="per">per month</div>
      <ul>
        <li>All HitBeatRun running videos</li>
        <li>New songs analyzed with the HitBeatRun algorithm</li>
        <li>Low / medium / max speed cues for every track</li>
        <li>Cancel anytime</li>
      </ul>
      <a class="btn btn-white btn-run" href="#" data-cta>{RUN}</a>
      <small>Secure checkout and billing by Fourthwall</small>
    </div>
  </div>
</section>

<!-- ================= WHAT IS ================= -->
<section class="wrap what" id="what">
  <div class="what-card reveal">
    <h2>What is HitBeatRun?</h2>
    <p>Hit BeatRun is an innovative running algorithm designed to help you harness the power of rhythm to enhance your running experience.</p>
    <p>By syncing your steps to carefully curated beats, it creates a seamless connection between music and movement, improving your pace, endurance, and overall performance.</p>
    <p>Whether you're a beginner or a seasoned runner, Hit BeatRun transforms every run into an energizing and immersive journey.</p>
    <a class="btn btn-black btn-run" href="#" data-cta>{RUN}</a>
  </div>
  <div class="what-right">
    <div class="bars"><div class="bar"><i></i></div><div class="bar"><i></i></div><div class="bar"><i></i></div><div class="bar"><i></i></div></div>
    <div class="navy-card reveal">{bg_video(R, "what-is", "poster-7bd19447.jpg")}</div>
  </div>
</section>

<!-- ================= GETTING STARTED ================= -->
<section class="getting"><h2 class="big-title reveal">Getting Started</h2></section>
<section class="wrap how">
  <figure class="reveal"><div class="shot"><img src="{R}assets/img/gs-tutorial.png" alt="HitBeatRun tutorial: song title, music video, energy boost, speed" loading="lazy"></div>
    <h3>How HitBeatRun<br>Works?</h3>
    <p>HitBeatRun analyzes music's beats per minute (BPM) and energy levels to guide your running pace, signaling when to speed up or slow down.</p></figure>
  <figure class="reveal"><div class="shot"><img src="{R}assets/img/gs-gab.png" alt="Gab, creator of HitBeatRun" loading="lazy"></div>
    <h3>The Mind Behind HitBeatRun</h3>
    <p>As a tech geek with a passion for fitness and music, I developed HitBeatRun to blend the best of all three worlds, creating a tool that keeps you moving, motivated, and in rhythm.</p></figure>
  <figure class="reveal"><div class="shot"><img src="{R}assets/img/gs-speeds.png" alt="Your three speed running intervals" loading="lazy"></div>
    <h3>Unlock Your Perfect Workout</h3>
    <p>Set up your three running speeds, and let the music guide you! With the techniques I'll teach you, you'll master how to use HitBeatRun for an incredible workout.</p></figure>
</section>

<!-- ================= SONGS ================= -->
<section class="wrap songs" id="songs">
  <h2 class="big-title reveal">Songs</h2>
  <div class="song-list">{song_rows}</div>
  <div class="cta-row"><a class="btn btn-white btn-run" href="#" data-cta>{RUN}</a></div>
</section>

<!-- ================= COURSE ================= -->
<section class="wrap course" id="course">
  <h2 class="big-title reveal">What&rsquo;s Inside the 'Running<br>to the Beat' Course?</h2>
  <hr>
  <p class="lead">This course is designed to make your runs fun and effective! You'll learn the science behind running to the beat, sync your steps with music, and use the HITBEATRUN algorithm to match songs to your pace. With strategies for gear, playlists, and pacing, you'll take your running to the next level.</p>
  <div class="course-cards">
    <div class="c-card reveal"><img src="{R}assets/img/course-welcome.jpg" alt="Running with music" loading="lazy">
      <div class="panel cg1"><div class="row"><b>Welcome</b><button aria-label="More" aria-expanded="false">+</button></div>
      <p>What to expect from this course and how to apply this method to your workouts.</p></div></div>
    <div class="c-card reveal"><img src="{R}assets/img/course-science.jpg" alt="Code" loading="lazy">
      <div class="panel cg2"><div class="row"><b>Science behind hitbeatrun</b><button aria-label="More" aria-expanded="false">+</button></div>
      <p>This section explains the scientific foundation of HitBeatRun, detailing how AI, music synchronization, and energy level detection enhance running performance</p></div></div>
    <div class="c-card reveal"><img src="{R}assets/img/course-getting-started.jpg" alt="Track and field practice" loading="lazy">
      <div class="panel cg3"><div class="row"><b>Getting started</b><button aria-label="More" aria-expanded="false">+</button></div>
      <p>This section covers everything you need to begin: essential gear, how to analyze tracks for tempo and energy levels, and much more.</p></div></div>
    <div class="c-card reveal"><img src="{R}assets/img/course-practice.jpg" alt="On the treadmill" loading="lazy">
      <div class="panel cg4"><div class="row"><b>Practice</b><button aria-label="More" aria-expanded="false">+</button></div>
      <p>Learn to adjust your pace based on energy shifts and optimize your performance with step-by-step instructions.</p></div></div>
  </div>
  <div class="cta-row"><a class="btn btn-white btn-run" href="#" data-cta>{RUN}</a></div>
</section>

<!-- ================= ATHLETE (Speakers) ================= -->
<section class="wrap split" id="speakers">
  <div class="copy reveal">
    <h2 class="mid-title">Real-Time Performance Evaluation with an Athlete</h2>
    <p>We tested HitBeatRun with an indoor cycling instructor from Mixed Cycling Arts, evaluating its real-time performance. The algorithm seamlessly adjusted workout speed based on music energy, resulting in optimized performance and a more immersive training experience. This confirms the power of AI in enhancing fitness.</p>
    <a class="btn btn-white" href="#science">Learn More</a>
  </div>
  <div class="phone reveal">{bg_video(R, "athlete-eval", "poster-90e08844.jpg")}</div>
</section>

<!-- ================= AI & COMPUTER VISION ================= -->
<section class="wrap split rev">
  <div class="phone reveal">{bg_video(R, "ai-vision", "poster-67e72562.jpg")}</div>
  <div class="copy reveal">
    <h2 class="mid-title">AI &amp; Computer Vision in Action</h2>
    <p>By processing audio data through motion tracking, feature extraction, and image segmentation, the algorithm detects energy shifts in songs and translates them into real-time speed adjustments. This innovation ensures a fully immersive and efficient HIIT experience, seamlessly syncing your movement with the beat.</p>
    <a class="btn btn-white" href="#science">Learn More</a>
  </div>
</section>

<!-- ================= SCIENCE ================= -->
<section class="science" id="science">
  <div class="wrap reveal">
    <h2 class="mid-title">The Science behind the beat</h2>
    <p>Explore the in-depth findings behind the HitBeatRun algorithm with our comprehensive research paper. It details the development process, the use of AI and computer vision, and the results of performance evaluations with real athletes. Gain insights into how music energy synchronization can revolutionize workouts and enhance fitness outcomes.</p>
    <p><b>Click below to access the full paper and dive into the technology that&rsquo;s changing the way we train!</b></p>
    <a class="btn btn-grey" href="{R}assets/docs/HitBeatRun-Research-Paper.pdf" target="_blank" rel="noopener">Download it!</a>
  </div>
  <div class="science-media">
    <img src="{R}assets/img/research-paper.png" alt="New! Research Paper: Harmonizing Heartbeats" loading="lazy">
    {bg_video(R, "science-runner", "poster-b87224ec.jpg")}
  </div>
</section>

<!-- ================= SPONSORS ================= -->
<section class="sponsors">
  <h2 class="big-title reveal">Sponsors &amp; Partners</h2>
  <p class="sub">We offer a wide variety of partnership plans.</p>
  <div class="carousel">
    <button class="arrow prev" aria-label="Previous">&#10094;</button>
    <div class="track">{"".join(f'<img src="{R}assets/img/sponsor-{i}.jpg" alt="Sponsor logo" loading="lazy">' for i in range(1, 9))}</div>
    <button class="arrow next" aria-label="Next">&#10095;</button>
  </div>
  <a class="btn btn-outline" href="{R}become-a-sponsor.html">Become a Sponsor</a>
</section>

<!-- ================= NEWSLETTER ================= -->
<section class="newsletter">
  <img class="sphere" src="{R}assets/img/sphere.png" alt="" loading="lazy">
  <div class="wrap">
    <form class="news-card" data-form="Newsletter">
      <h2>Subscribe to our newsletter</h2>
      <label for="nl-email">Email *</label>
      <input id="nl-email" name="email" type="email" required>
      <label class="check"><input type="checkbox" name="subscribe" value="yes" required> Yes, subscribe me to your newsletter.</label>
      <button type="submit">Submit</button>
      <p class="form-msg" role="status"></p>
    </form>
  </div>
</section>

</main>
""" + footer(R, mode)


def song_page(R, i):
    s = SONGS[i]
    prev_s, next_s = SONGS[i - 1], SONGS[(i + 1) % len(SONGS)]
    return head(R, f"{s[5]} | HitBeatRun", f"Run to the beat: {s[5]} with the HitBeatRun speed guide.") + f"""
<body data-root="{R}" data-mode="main">
{header(R, "main", home_active=False)}
<main class="song-page">
  <h1>{escape(s[5])}</h1>
  <div class="player">
    <video src="{R}assets/video/{s[4]}.mp4" poster="{R}assets/img/frame-{s[4]}.jpg" controls playsinline preload="metadata"></video>
  </div>
  <div class="song-nav">
    <a class="btn btn-outline" href="{prev_s[0]}.html">&larr; {escape(prev_s[1])}</a>
    <a class="btn btn-outline" href="{next_s[0]}.html">{escape(next_s[1])} &rarr;</a>
  </div>
</main>
""" + footer(R, "main")


def songs_index(R):
    rows = "".join(
        f"""<div class="song"><img src="{R}assets/img/{s[3]}" alt="" loading="lazy">
        <div class="meta"><div class="t">{escape(s[1])}</div><div class="a">{escape(s[2])}</div></div>
        <a class="btn btn-outline" href="{s[0]}.html">Play</a></div>""" for s in SONGS)
    return head(R, "Songs | HitBeatRun", "Songs analyzed with the HitBeatRun algorithm.") + f"""
<body data-root="{R}" data-mode="main">
{header(R, "main", home_active=False)}
<main class="wrap songs page"><h1 class="big-title">Songs</h1><br><br><div class="song-list">{rows}</div></main>
""" + footer(R, "main")


def sponsor_page(R):
    return head(R, "Become a Sponsor | HitBeatRun", "Partner with HitBeatRun.") + f"""
<body data-root="{R}" data-mode="main">
{header(R, "main", home_active=False)}
<main class="wrap page">
  <h1 class="big-title">Become<br>a Sponsor</h1>
  <form class="form-card" data-form="Sponsor request">
    <label>First name *<input name="first_name" required></label>
    <label>Last name *<input name="last_name" required></label>
    <label class="full">Company name<input name="company"></label>
    <label class="full">Email *<input name="email" type="email" required></label>
    <label class="full">Notes<textarea name="notes" rows="4"></textarea></label>
    <button type="submit">Submit</button>
    <p class="form-msg full" role="status"></p>
  </form>
</main>
""" + footer(R, "main")


LEGAL = {
    "terms-and-conditions": ("Terms &amp; Conditions", [
        "By using hitbeatrun.com you agree to these terms. The HitBeatRun videos, course material, research and the HitBeatRun algorithm are the property of Mind by Gab and are provided for personal, non-commercial use.",
        "Running and interval training involve physical exertion. Consult a medical professional before starting any new exercise program, and always run at speeds that are safe for you. You use HitBeatRun at your own risk.",
        "Subscriptions and purchases are processed by Fourthwall and are also subject to Fourthwall's terms.",
        "We may update these terms from time to time. Questions? Contact us at the email address in the footer.",
    ]),
    "privacy-policy": ("Privacy Policy", [
        "We only collect the information you choose to send us, such as your email address when you subscribe to the newsletter or contact us about sponsorship.",
        "We use it to reply to you and to send the newsletter you asked for. We never sell your personal information. You can unsubscribe or ask us to delete your data at any time by emailing us.",
        "Payments and memberships are handled by Fourthwall, which has its own privacy policy.",
    ]),
    "refund-policy": ("Refund Policy", [
        "Subscriptions to the HitBeatRun running videos are sold and billed through Fourthwall. You can cancel your subscription at any time from your Fourthwall account; cancellation stops future renewals.",
        "If you have a billing problem or believe you were charged in error, contact us within 14 days and we will make it right.",
    ]),
    "accessibility-statement": ("Accessibility statement", [
        "We want everyone to be able to use HitBeatRun. This site uses semantic HTML, text alternatives for images, keyboard-accessible controls and respects your device's reduced-motion setting.",
        "If you run into an accessibility barrier, please email us and we will work to fix it.",
    ]),
}


def legal_page(R, slug):
    title, paras = LEGAL[slug]
    body = "".join(f"<p style=\"font-size:17px;line-height:1.7;margin-top:22px\">{p}</p>" for p in paras)
    return head(R, f"{title.replace('&amp;', '&')} | HitBeatRun", title.replace('&amp;', '&')) + f"""
<body data-root="{R}" data-mode="main">
{header(R, "main", home_active=False)}
<main class="wrap page" style="max-width:820px"><h1 class="big-title" style="text-align:left">{title}</h1>{body}</main>
""" + footer(R, "main")


def write(rel, html):
    p = SITE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    print("wrote", rel)


if __name__ == "__main__":
    write("index.html", home_page("", "main"))
    write("subscribe/index.html", home_page("../", "landing"))
    write("songs/index.html", songs_index("../"))
    for i, s in enumerate(SONGS):
        write(f"songs/{s[0]}.html", song_page("../", i))
    write("become-a-sponsor.html", sponsor_page(""))
    for slug in LEGAL:
        write(f"{slug}.html", legal_page("", slug))
