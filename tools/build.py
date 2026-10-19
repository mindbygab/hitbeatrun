#!/usr/bin/env python3
"""Builds every HTML page of the HitBeatRun site from one template.

    python3 tools/build.py

Outputs (relative to the site root):
    index.html                 main site (hitbeatrun.com)
    subscribe/index.html       Fourthwall subscription landing page (same design)
    songs/index.html, songs/<slug>.html
    legal.html (forwards to the Terms / Privacy pages on Fourthwall)
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
    return f"""<header class="site-header">
  <a class="logo" href="https://www.mindbygab.com" target="_blank" rel="noopener" aria-label="Mind by Gab website"><img src="{R}assets/img/logo-mind.png" alt="Mind by Gab"></a>
  <nav class="nav" aria-label="Main">
    <a href="{home}"{' class="active"' if home_active else ''}>Home</a>
    <a href="{home}#what">About</a>
    <a href="{home}#songs">Try It Live</a>
  </nav>
  <div class="header-right">
    <a class="btn btn-login" href="#" data-fourthwall><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>Log In</a>
    <a class="btn btn-outline btn-run" href="#" data-cta>{L['tickets']}</a>
    <button class="burger" aria-label="Menu">&#9776;</button>
  </div>
</header>"""


def footer(R, mode):
    home = f"{R}index.html" if mode == "main" else "./"
    words = ["Run to the beat", "128 BPM", "Speed ramps", "New songs", "Low · Medium · Max", "Feel the drop"]
    marquee = "".join(f"<span>{w}</span><i>&#10022;</i>" for w in words) * 2
    return f"""<footer class="site-footer">
  <div class="marquee" aria-hidden="true"><div class="mq-track">{marquee}</div></div>
  <div class="foot-cta reveal">
    <span class="eyebrow">Join HitBeatRun</span>
    <h2>Your next run is<br><span class="grad-text">one beat away.</span></h2>
    <p>Every song, speed ramp and run-along video for <b>$4.99/month</b>. Cancel anytime.</p>
    <a class="btn btn-white btn-run btn-big" href="#" data-cta>{RUN}</a>
    <p class="member-line">Already a member? <a href="#" data-fourthwall>Log in &rarr;</a></p>
  </div>
  <form class="news-strip" data-form="Newsletter">
    <div class="ns-text"><b>Not ready yet?</b> Get new songs and running tips by email.</div>
    <div class="ns-field"><input type="email" name="email" placeholder="Your email" required aria-label="Your email"><button type="submit">Sign up</button></div>
    <p class="form-msg" role="status"></p>
  </form>
  <div class="foot-cols">
    <div class="fc-brand">
      <a class="logo" href="https://www.mindbygab.com" target="_blank" rel="noopener" aria-label="Mind by Gab website"><img src="{R}assets/img/logo-mind.png" alt="Mind by Gab"></a>
      <p>Run to the beat. Pre-recorded running videos with speed cues timed to the music.</p>
      <div class="fb-social">
        <a href="https://www.facebook.com/hitbeatrun" target="_blank" rel="noopener" aria-label="HitBeatRun on Facebook"><svg viewBox="0 0 24 24"><path d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.6c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1v1.9H8v3.2h2.6V21H14v-9.3h2.6l.4-3.2z"/></svg></a>
        <a href="https://www.instagram.com/hitbeatrun" target="_blank" rel="noopener" aria-label="HitBeatRun on Instagram"><svg viewBox="0 0 24 24"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm4.9-8.9a1.1 1.1 0 1 0 0 2.2 1.1 1.1 0 0 0 0-2.2zM21.9 7.6c-.1-1.6-.4-3-1.6-4.2S17.7 1.9 16.1 1.8C14.5 1.7 9.5 1.7 7.9 1.8 6.3 1.9 4.9 2.2 3.7 3.4S2.1 6 2 7.6c-.1 1.6-.1 6.6 0 8.2.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.6.1 6.6.1 8.2 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.2-1.6.2-6.6.1-8.2zm-2.1 9.9a3.2 3.2 0 0 1-1.8 1.8c-1.3.5-4.3.4-5.7.4s-4.4.1-5.7-.4a3.2 3.2 0 0 1-1.8-1.8c-.5-1.3-.4-4.3-.4-5.7s-.1-4.4.4-5.7A3.2 3.2 0 0 1 6.6 4.3c1.3-.5 4.3-.4 5.7-.4s4.4-.1 5.7.4a3.2 3.2 0 0 1 1.8 1.8c.5 1.3.4 4.3.4 5.7s.1 4.4-.4 5.7z"/></svg></a>
      </div>
    </div>
    <div class="fc-col">
      <h4>Explore</h4>
      <a href="{home}">Home</a>
      <a href="{home}#what">About</a>
      <a href="{home}#songs">Try It Live</a>
      <a href="{home}#join">Membership</a>
      <a href="#" data-fourthwall>Log In</a>
    </div>
    <div class="fc-col">
      <h4>Legal</h4>
      <a href="https://members-hitbeatrun-shop.fourthwall.com/pages/terms-of-service" target="_blank" rel="noopener">Terms of Service</a>
      <a href="https://members-hitbeatrun-shop.fourthwall.com/pages/privacy-policy" target="_blank" rel="noopener">Privacy Policy</a>
      <a href="{R}music.html">Music &amp; Credits</a>
    </div>
    <div class="fc-col">
      <h4>Contact Us</h4>
      <p>Questions about HitBeatRun or your membership?</p>
      <a class="fc-email" href="#" data-email></a>
    </div>
  </div>
  <div class="foot-legal">
    <span>&copy; 2026 HitBeatRun by <a class="mg-link" href="https://www.mindbygab.com" target="_blank" rel="noopener">Mind by Gab</a>. All rights reserved.</span>
    <span><a href="https://members-hitbeatrun-shop.fourthwall.com/pages/terms-of-service" target="_blank" rel="noopener">Terms</a> &middot; <a href="https://members-hitbeatrun-shop.fourthwall.com/pages/privacy-policy" target="_blank" rel="noopener">Privacy</a></span>
  </div>
</footer>
<script src="{R}assets/js/main.js?v={ver("assets/js/main.js")}"></script>
</body>
</html>
"""


def bg_video(R, name, poster, cls=""):
    cls_attr = f' class="{cls}"' if cls else ""
    url = f'{R}assets/video/{name}.mp4?v={ver(f"assets/video/{name}.mp4")}'
    if cls == "direct":  # source given up front so Safari's own autoplay starts it
        return (f'<video class="direct" src="{url}" data-src="{url}" poster="{R}assets/img/{poster}" '
                'muted autoplay loop playsinline webkit-playsinline disablepictureinpicture preload="auto"></video>')
    return (f'<video{cls_attr} data-src="{url}" '
            f'poster="{R}assets/img/{poster}" muted autoplay loop playsinline webkit-playsinline disablepictureinpicture preload="none"></video>')


def home_page(R, mode):
    L = LABELS[mode]
    S = {s[0]: s for s in SONGS}
    song_rows = "".join(
        f"""<div class="song reveal"><img src="{R}assets/img/thumbs/{s[3].rsplit('.', 1)[0]}.jpg" alt="" width="60" height="60">
        <div class="meta"><div class="t">{escape(s[1])}</div><div class="a">{escape(s[2])}</div></div>
        <a class="btn-play" href="{R}songs/{s[0]}.html" data-play="{R}assets/video/{s[4]}.mp4" data-poster="{R}assets/img/frame-{s[4]}.jpg" data-title="{escape(s[5])}" aria-label="Play {escape(s[1])}"><span class="pi"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>Play</a></div>"""
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
      {bg_video(R, "hero-science", "poster-1a175681.jpg", "eager")}</article>
    <article class="stack-card"><header class="g2"><img src="{R}assets/img/icon-x.png" alt=""><h2>Integrating HITBEATRUN In Your Daily Workout</h2></header>
      {bg_video(R, "hero-integrating", "poster-5d27d50d.jpg", "eager")}</article>
    <article class="stack-card"><header class="g3"><img src="{R}assets/img/icon-o.png" alt=""><h2>1500+<br>Students Using Hitbeatrun</h2></header>
      {bg_video(R, "hero-students", "poster-55d00e39.jpg", "eager")}</article>
    <article class="stack-card"><header class="g4"><img src="{R}assets/img/icon-344.png" alt=""><h2>New Songs Analyzed with<br>HITBEATRUN Algorithm</h2></header>
      {bg_video(R, "hero-newsongs", "poster-061d9c62.jpg", "eager")}</article>
  </div>
  <div class="hero-cta"><a class="btn btn-white btn-run" href="#" data-cta>{L['get']}</a></div>
</section>

<!-- ================= RUN BANNER ================= -->
<section class="run-banner reveal">
  <h2>Ready to transform your running game?</h2>
  <p>Find your three running speeds, follow the cues in every video as the music builds and drops, and get more out of every workout.</p>
  <a class="btn btn-black btn-run" href="#" data-cta>Access Now</a>
  <p class="member-line dark">Already a member? <a href="#" data-fourthwall>Log in &rarr;</a></p>
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
        <li>New songs mastered with speed ramps</li>
        <li>Guided run-along videos</li>
        <li>Technique skills &amp; the science behind the beat</li>
        <li>Cancel anytime</li>
      </ul>
      <a class="btn btn-white btn-run" href="#" data-cta>{RUN}</a>
      <small>Secure checkout and billing by Fourthwall</small>
    </div>
  </div>
</section>

<!-- ================= WHAT'S INSIDE THE SUBSCRIPTION ================= -->
<section class="wrap inside" id="inside">
  <div class="inside-head reveal">
    <span class="eyebrow">The HitBeatRun subscription</span>
    <h2 class="big-title">What&rsquo;s Inside Your<br><span class="grad-text">HitBeatRun</span> Subscription?</h2>
    <p class="lead">Everything you need to run to the beat: new songs mastered with speed ramps, the technique to keep up with them, and the science that makes it work.</p>
  </div>
  <div class="perks">
    <article class="perk reveal">
      <div class="perk-img"><img src="{R}assets/img/course-welcome.jpg" alt="Runner with headphones" loading="lazy"><span class="num">01</span></div>
      <div class="perk-body"><span class="bar-accent g1"></span>
        <h3>New songs, mastered for the beat</h3>
        <p>Fresh tracks analyzed with the HitBeatRun algorithm, with speed ramps timed to every build-up and drop.</p></div>
    </article>
    <article class="perk reveal">
      <div class="perk-img"><img src="{R}assets/img/course-practice.jpg" alt="Runners on treadmills" loading="lazy"><span class="num">02</span></div>
      <div class="perk-body"><span class="bar-accent g2"></span>
        <h3>Guided run-along videos</h3>
        <p>Press play and follow the on-screen speed cues (low, medium, max) on the treadmill or outside.</p></div>
    </article>
    <article class="perk reveal">
      <div class="perk-img"><img src="{R}assets/img/course-getting-started.jpg" alt="Sprinters at the start line" loading="lazy"><span class="num">03</span></div>
      <div class="perk-body"><span class="bar-accent g3"></span>
        <h3>Technique skills</h3>
        <p>Cadence, form and breathing drills that keep your steps locked to the beat and every run feeling smoother.</p></div>
    </article>
    <article class="perk reveal">
      <div class="perk-img"><img src="{R}assets/img/course-science.jpg" alt="Code on a screen" loading="lazy"><span class="num">04</span></div>
      <div class="perk-body"><span class="bar-accent g4"></span>
        <h3>The science behind the beat</h3>
        <p>How BPM, music energy and AI-driven analysis shape your pace, straight from the HitBeatRun research.</p></div>
    </article>
  </div>
  <div class="more reveal">
    <span class="more-label">&hellip;and much more</span>
    <ul class="chips"><li>New drops added regularly</li><li>Treadmill or outdoor</li><li>Beginner to advanced</li><li>Watch on any device</li><li>Cancel anytime</li></ul>
  </div>
  <div class="try reveal">
    <a class="btn btn-white btn-run btn-big" href="#" data-cta>Try it now &middot; $4.99/month</a>
    <small>Billed monthly through Fourthwall. Cancel anytime.</small>
  </div>
</section>

<!-- ================= WHAT IS (About) ================= -->
<section class="about" id="what">
  <div class="wrap about-grid">
    <div class="about-copy reveal from-left">
      <span class="eyebrow">About HitBeatRun</span>
      <h2 class="big-title">What is <span class="grad-text">HitBeatRun?</span></h2>
      <p class="about-lead">HitBeatRun is an innovative running algorithm designed to help you harness the power of rhythm to enhance your running experience.</p>
      <ul class="about-points">
        <li><span class="ap-icon"><svg viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg></span>
          <div><b>Steps synced to the beat</b><p>Carefully curated songs create a seamless connection between music and movement.</p></div></li>
        <li><span class="ap-icon"><svg viewBox="0 0 24 24"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg></span>
          <div><b>Better pace and endurance</b><p>Following the music's energy improves your pace, endurance and overall performance.</p></div></li>
        <li><span class="ap-icon"><svg viewBox="0 0 24 24"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg></span>
          <div><b>Made for every runner</b><p>Beginner or seasoned runner, every run becomes an energizing and immersive journey.</p></div></li>
      </ul>
      <a class="btn btn-white btn-run" href="#" data-cta>Access Now</a>
    </div>
    <div class="about-visual">
      <div class="about-glow"></div>
      <div class="screen">
        <div class="screen-bar"><i></i><i></i><i></i><span>hitbeatrun &middot; live analysis</span></div>
        {bg_video(R, "what-is", "poster-7bd19447.jpg", "direct")}
      </div>
      <div class="meter">
        <div class="meter-head"><b>Music energy</b><span class="meter-live"><i></i>128 BPM</span></div>
        <div class="eq" aria-hidden="true">{"".join("<span></span>" for _ in range(24))}</div>
        <div class="levels"><span class="lv lv-1">Low</span><span class="lv lv-2">Medium</span><span class="lv lv-3">Max</span></div>
      </div>
    </div>
  </div>
</section>

<!-- ================= HOW IT WORKS ================= -->
<section class="how-sec" id="how">
  <div class="wrap how-head reveal">
    <span class="eyebrow">Getting started</span>
    <h2 class="big-title">How <span class="grad-text">HitBeatRun</span> Works</h2>
    <p class="lead">The music sets the pace. You just run.</p>
  </div>
  <div class="wrap how-wrap">
    <svg class="beatline" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true">
      <defs><linearGradient id="bl" x1="0" x2="1"><stop offset="0" stop-color="#5e95e5"/><stop offset=".5" stop-color="#9271d0"/><stop offset="1" stop-color="#da44c1"/></linearGradient></defs>
      <path class="bl-base" pathLength="1" d="M0 60 H170 l18 -42 l22 86 l20 -64 l14 20 H560 l18 -48 l22 96 l20 -72 l14 24 H950 l18 -42 l22 86 l20 -64 l14 20 H1200"/>
      <path class="bl-pulse" pathLength="1" d="M0 60 H170 l18 -42 l22 86 l20 -64 l14 20 H560 l18 -48 l22 96 l20 -72 l14 24 H950 l18 -42 l22 86 l20 -64 l14 20 H1200"/>
    </svg>
    <div class="steps">
      <figure class="step reveal">
        <div class="step-in">
          <span class="step-num">01</span>
          <div class="shot"><img src="{R}assets/img/gs-tutorial.png" alt="HitBeatRun tutorial: song title, music video, energy boost and speed" loading="lazy"></div>
          <span class="step-tag">The music leads</span>
          <h3>Follow the beat</h3>
          <p>HitBeatRun analyzes each song's beats per minute (BPM) and energy levels to guide your pace, signaling when to speed up or slow down.</p>
        </div>
      </figure>
      <figure class="step reveal">
        <div class="step-in">
          <span class="step-num">02</span>
          <div class="shot"><img src="{R}assets/img/gs-speeds.png" alt="Your three speed running intervals: 6.5, 7.5 and 8.5 mph" loading="lazy"></div>
          <span class="step-tag">Run at your own pace</span>
          <h3>Your three speeds, one guide</h3>
          <p>Know your own low, medium and max running speeds. Every HitBeatRun video is pre-recorded with on-screen cues, so you just switch to the speed it calls for, right on the beat.</p>
          <a class="step-link" href="#" data-cta>Unlock the videos &rarr;</a>
        </div>
      </figure>
      <figure class="step reveal">
        <div class="step-in">
          <span class="step-num">03</span>
          <div class="shot"><img src="{R}assets/img/gs-gab.png" alt="Gab, creator of HitBeatRun" loading="lazy"></div>
          <span class="step-tag">The mind behind HitBeatRun</span>
          <h3>Built by a runner who codes</h3>
          <p>As a tech geek with a passion for fitness and music, I built HitBeatRun to blend all three worlds into a tool that keeps you moving, motivated and in rhythm.</p>
          <a class="step-link" href="https://www.mindbygab.com" target="_blank" rel="noopener">Visit Mind by Gab &rarr;</a>
        </div>
      </figure>
    </div>
  </div>
</section>

<!-- ================= SONGS ================= -->
<section class="wrap songs" id="songs">
  <div class="songs-head reveal">
    <span class="eyebrow">Free preview</span>
    <h2 class="big-title">Try It <span class="grad-text">Live</span></h2>
    <p class="lead">Check how HitBeatRun works with some popular songs. Press play, follow the speed cues and try it out.</p>
  </div>
  <div class="song-list">{song_rows}</div>
  <div class="music-note reveal">
    <span class="mn-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg></span>
    <p><b>About these preview songs:</b> the tracks above belong to their original artists and rights holders. HitBeatRun does not own them, claims no rights in them and does not sell them; they are shown only as free examples of how the HitBeatRun algorithm reads a song's beat and energy. The music inside the HitBeatRun membership is original, created with a paid Suno plan that permits commercial use.
    <a href="{R}music.html">Learn more about HitBeatRun songs &rarr;</a></p>
  </div>
  <div class="songs-cta reveal">
    <p>Liked it? Members get every song, with new ones added regularly.</p>
    <a class="btn btn-white btn-run" href="#" data-cta>{RUN}</a>
  </div>
</section>

<!-- ================= PROOF: ATHLETE + AI ================= -->
<section class="proof" id="speakers">
  <div class="wrap split">
    <div class="copy reveal from-left">
      <span class="eyebrow">Real-world test</span>
      <h2 class="mid-title">Real-Time Performance Evaluation with an <span class="grad-text">Athlete</span></h2>
      <p>We tested HitBeatRun with an indoor cycling instructor from Mixed Cycling Arts, evaluating its real-time performance. The algorithm adjusted workout speed to the music's energy, resulting in optimized performance and a more immersive training experience.</p>
      <ul class="proof-facts">
        <li><b>Live</b><span>speed changes on the beat</span></li>
        <li><b>Pro</b><span>indoor cycling instructor</span></li>
      </ul>
      <a class="btn btn-white btn-run" href="#" data-fourthwall>Log In to Watch</a>
    </div>
    <div class="phone-stage reveal from-right" data-parallax="40">
      <div class="phone-ring"></div>
      <div class="phone" data-sound role="button" tabindex="0" aria-label="Turn sound on or off">{bg_video(R, "athlete-eval", "poster-90e08844.jpg")}<span class="live-badge"><i></i>Live test</span><button class="sound-btn" type="button" tabindex="-1" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M11 5L6 9H2v6h4l5 4z"/><path class="off" d="M22 9l-6 6M16 9l6 6"/><path class="on" d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg><span class="off">Tap for sound</span><span class="on">Sound on</span></button></div>
      <div class="float-chip fc-a"><b>&uarr; Energy rising</b><span>Speed up to MAX</span></div>
    </div>
  </div>

  <div class="wrap split rev">
    <div class="phone-stage reveal from-left" data-parallax="40">
      <div class="phone-ring ring-b"></div>
      <div class="phone" data-sound role="button" tabindex="0" aria-label="Turn sound on or off">{bg_video(R, "ai-vision", "poster-67e72562.jpg")}<span class="live-badge"><i></i>AI analysis</span><button class="sound-btn" type="button" tabindex="-1" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M11 5L6 9H2v6h4l5 4z"/><path class="off" d="M22 9l-6 6M16 9l6 6"/><path class="on" d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg><span class="off">Tap for sound</span><span class="on">Sound on</span></button></div>
      <div class="float-chip fc-b"><b>Energy shift detected</b><span>Drop in 4 beats</span></div>
    </div>
    <div class="copy reveal from-right">
      <span class="eyebrow">The technology</span>
      <h2 class="mid-title">AI &amp; Computer Vision <span class="grad-text">in Action</span></h2>
      <p>The algorithm processes each song to detect its energy shifts and turns them into real-time speed cues, so your movement stays in sync with the beat for an immersive, efficient HIIT run.</p>
      <ol class="pipeline">
        <li><span>01</span>Motion tracking</li>
        <li><span>02</span>Feature extraction</li>
        <li><span>03</span>Image segmentation</li>
      </ol>
      <a class="btn btn-outline" href="#science">See the science &rarr;</a>
    </div>
  </div>
</section>

<!-- ================= SCIENCE ================= -->
<section class="science" id="science">
  <div class="sci-card reveal">
    <div class="sci-bg">{bg_video(R, "science-runner", "poster-b87224ec.jpg")}</div>
    <div class="sci-copy">
      <span class="eyebrow">Research</span>
      <h2>The Science<br>behind <span class="grad-text">the beat</span></h2>
      <p>Explore the in-depth findings behind the HitBeatRun algorithm: how it was built, how AI and computer vision read the music, and how real athletes performed when their speed followed the song's energy.</p>
      <ul class="sci-points">
        <li><b>AI</b><span>&amp; computer vision</span></li>
        <li><b>BPM</b><span>&amp; energy detection</span></li>
        <li><b>Real</b><span>athlete testing</span></li>
      </ul>
      <div class="sci-btns">
        <a class="btn btn-white" href="#" data-supporters>Download the paper</a>
        <a class="btn btn-outline btn-run" href="#" data-cta>Access Now</a>
      </div>
    </div>
    <div class="sci-paper"><img src="{R}assets/img/research-paper.png" alt="New! Research Paper: Harmonizing Heartbeats" loading="lazy"></div>
  </div>
</section>

</main>

<!-- in-page video player for "Try It Live" -->
<div class="player-modal" id="player" role="dialog" aria-modal="true" aria-label="Song preview" hidden>
  <div class="pm-backdrop" data-close></div>
  <div class="pm-box">
    <div class="pm-head"><b class="pm-title"></b><button class="pm-close" data-close aria-label="Close">&times;</button></div>
    <video class="pm-video" controls playsinline webkit-playsinline preload="auto"></video>
    <div class="pm-foot"><span>Liked it? Members get every song.</span><a class="btn btn-white btn-run" href="#" data-cta>{RUN}</a></div>
  </div>
</div>
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


def music_page(R):
    credits = "".join(f"<li><b>{escape(s[1])}</b><span>{escape(s[2])}</span></li>" for s in SONGS)
    return head(R, "Music & Credits | HitBeatRun", "Where the music on HitBeatRun comes from: preview songs by their original artists, and original member music made with a paid Suno plan.") + f"""
<body data-root="{R}" data-mode="main">
{header(R, "main", home_active=False)}
<main class="legal music">
  <div class="legal-head">
    <span class="eyebrow">Music &amp; Credits</span>
    <h1>About <span class="grad-text">HitBeatRun songs</span></h1>
    <p>Last updated: October 19, 2026</p>
    <div class="legal-jump"><a href="#previews">Preview songs</a><a href="#members">Member music</a><a href="#rights">Rights holders</a></div>
  </div>

  <section class="legal-card" id="previews">
    <h2>Preview songs on this website</h2>
    <p>The &ldquo;Try It Live&rdquo; section shows a few popular songs so you can see how the HitBeatRun algorithm works: it reads each song's tempo (BPM) and energy and shows when to switch between your low, medium and max speeds.</p>
    <h3>Who owns them</h3>
    <p>These songs, their recordings, titles and artwork belong to their original artists, songwriters, labels and other rights holders. HitBeatRun does not own them and claims no rights in them. They are credited below by title and artist.</p>
    <h3>How they are used</h3>
    <p>The previews are free to watch and are shown only as examples of the method. They are not sold, not part of the paid membership and not offered for download. Their appearance here does not mean the artists endorse or are affiliated with HitBeatRun.</p>
    <h3>Credits</h3>
    <ul class="credits">{credits}</ul>
  </section>

  <section class="legal-card" id="members">
    <h2>Music inside the HitBeatRun membership</h2>
    <p>The songs in the members-only HitBeatRun videos are original music created by HitBeatRun with <a href="https://suno.com" target="_blank" rel="noopener">Suno</a>, an AI music tool, on a paid subscription plan whose terms allow commercial use of the songs generated and downloaded under that plan.</p>
    <h3>What that means for you</h3>
    <p>Your membership lets you stream these videos for your own personal workouts. The music and videos may not be downloaded, re-uploaded, shared or used commercially, as set out in the <a href="https://members-hitbeatrun-shop.fourthwall.com/pages/terms-of-service" target="_blank" rel="noopener">Terms of Service</a>.</p>
    <h3>AI-generated music</h3>
    <p>We say openly that member music is AI-generated with Suno. Any resemblance to existing songs is unintentional; if you believe a member track is too close to your work, please contact us below.</p>
  </section>

  <section class="legal-card" id="rights">
    <h2>For artists and rights holders</h2>
    <p>We respect artists' rights. If you own or represent any song shown on HitBeatRun and would like it credited differently or removed, email us with the song title and a link to where it appears. We will review your request promptly and remove the content if asked.</p>
    <p>Contact: <a href="#" data-email></a></p>
  </section>
</main>
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
    write("music.html", music_page(""))
    # Terms + Privacy live on Fourthwall; legal.html forwards there so old links keep working
    write("legal.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Terms of Service | HitBeatRun</title>
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=https://members-hitbeatrun-shop.fourthwall.com/pages/terms-of-service">
<script>location.replace(location.hash === "#privacy" ? "https://members-hitbeatrun-shop.fourthwall.com/pages/privacy-policy" : "https://members-hitbeatrun-shop.fourthwall.com/pages/terms-of-service");</script></head>
<body style="background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:60px">
<p><a style="color:#da44c1" href="https://members-hitbeatrun-shop.fourthwall.com/pages/terms-of-service">Terms of Service</a> &middot; <a style="color:#da44c1" href="https://members-hitbeatrun-shop.fourthwall.com/pages/privacy-policy">Privacy Policy</a></p></body></html>
""")
    # hitbeatrun.com/supporters -> Fourthwall shop (old links keep working)
    fw = "https://members-hitbeatrun-shop.fourthwall.com"
    write("supporters/index.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>HitBeatRun membership</title>
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={fw}">
<link rel="canonical" href="{fw}"><script>location.replace("{fw}" + location.search);</script></head>
<body style="background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:60px">
<p>Taking you to HitBeatRun membership&hellip; <a style="color:#da44c1" href="{fw}">Continue</a></p></body></html>
""")
