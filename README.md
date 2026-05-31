<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0a,100:1a1a2e&height=200&section=header&text=MP3X&fontSize=80&fontColor=00d4ff&fontAlignY=38&desc=Lightweight+music+downloading+for+the+real+internet&descColor=888888&descSize=16&animation=fadeIn" width="100%"/>

[![Visits](https://img.shields.io/badge/dynamic/json?color=00d4ff&label=Website&query=%24.status&url=https%3A%2F%2Fmusic.mp3x.xo.je&style=flat-square&logo=googlechrome&logoColor=white&labelColor=0a0a0a)](https://music.mp3x.xo.je)
![GitHub Actions](https://img.shields.io/badge/Powered_by-GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white&labelColor=0a0a0a)
![Static](https://img.shields.io/badge/Zero-Backend-00ff88?style=flat-square&logo=html5&logoColor=white&labelColor=0a0a0a)
![Size](https://img.shields.io/badge/Page_Weight-Ultra_Lite-ff6b35?style=flat-square&logo=speedtest&logoColor=white&labelColor=0a0a0a)

</div>

---
```
  [ music for every phone. every network. every person. ]
 Works on any devices. 
```

---

## 🌍 Built For

> MP3X is designed for people **often ignored** by modern web design.

| Device / Condition | Status |
|---|---|
| 📱 Keypad phones (JioBharat, etc.) | ✅ Fully supported |
| 🌐 Opera Mini browser | ✅ Fully supported |
| 🛰️ Slow / 2G connections | ✅ Optimized |
| 💾 Low storage devices | ✅ Small file focused |
| 🎵 Offline music listeners | ✅ Direct download |
| ⚡ Lightweight web enthusiasts | ✅ No bloat |

---

## ✨ Philosophy

Modern music platforms became:

```diff
- Heavy JavaScript bundles
- Autoplay ads
- Account walls
- 10MB+ pages
- Unusable on slow networks
```

**MP3X follows a different path:**

```
  Open Website
       ↓
  Select Music
       ↓
    Download
       ↓
     Done.
```

```
  No accounts.    No tracking.    No complexity.
```

---

## ⚙️ How It Works

```
  ┌──────────────────────────────────────┐
  │                                             │
  │   You upload:   Billie-Jean.mp3             │
  │                        ↓                    │
  │   GitHub Action triggers automatically      │
  │                        ↓                    │
  │   generator.py scans repository root        │
  │                        ↓                    │
  │   Filename parsed  →  "Billie Jean"        │
  │                        ↓                    │
  │   index.html rebuilt with new music lis     │
  │                        ↓                    │
  │   GitHub Pages publishes updated site       │
  │                        ↓                    │
  │   Visitor taps link  →  MP3 downloads  ✓   │
  │                                             │
  └──────────────────────────────────────┘
```

**Zero manual editing. Zero playlist files. Zero database.**

The website updates itself.

---

## 🧠 Smart Filename Parsing

Just name your file correctly — MP3X does the rest.

```python
  "Billie-Jean.mp3"                    →  "Billie Jean"
  "Village-Ghost-Story.mp3"            →  "Village Ghost Story"
  "I-Thought-I-Saw-Your-Face.mp3"      →  "I Thought I Saw Your Face"
```

**Coming soon — tag prefix support:**

```python
  "[NEW]-Ghost-Story.mp3"              →  🆕  Ghost Story
  "[SPECIAL]-Village-River.mp3"        →  ⭐  Village River
```

Rules applied automatically:
- Strip `.mp3` extension
- Replace `-` with spaces
- Title Case the result
- Preserve numbers
- Strip `[TAG]` prefixes into metadata

---

## 🚀 Features

<div align="center">

| Feature | Detail |
|---|---|
| ⚡ Ultra Lightweight | Pure HTML + CSS. No JS required |
| 📥 Direct MP3 Downloads | One tap. File saves instantly |
| 📱 Mobile Optimized | Works on any screen size |
| 🎹 Keypad Phone Ready | Navigable without touchscreen |
| 🌐 Opera Mini Compatible | No fetch(), no JS dependencies |
| ☁️ GitHub Pages Hosted | Free. Fast. Always online |
| 🧠 Zero Frameworks | No React. No Vue. No overhead |
| 🔋 Low Data Mode | 32–48kbps mono audio supported |
| 🤖 Auto Music Discovery | Drop MP3 → site updates itself |
| 🛠️ GitHub Actions CI | Automated static generation |
| 🔒 Safe HTML Escaping | UTF-8 filenames handled correctly |
| 📶 Offline Ready | Downloaded files play without internet |

</div>

---

## 🛠️ Tech Stack

```
  ╔════════════════════════════╗
  ║  FRONTEND    →  HTML  +  CSS    ║
  ║  GENERATOR   →  Python 3.12     ║
  ║  AUTOMATION  →  GitHub Actions  ║
  ║  HOSTING     →  GitHub Pages    ║
  ║  BACKEND     →  none            ║
  ║  DATABASE    →  none            ║
  ║  SERVER      →  none            ║
  ║  COST        →  $0.00           ║
  ╚════════════════════════════╝
```

---

## 📂 Repository Structure

```
  mp3x/
  ├── index.html              ← auto-updated by generator
  ├── generator.py            ← scans MP3s, builds HTML
  ├── .nojekyll               ← disables Jekyll on GitHub Pages
  ├── .github/
  │   └── workflows/
  │       └── update.yml      ← triggers on every MP3 upload
  │
  ├── Billie-Jean.mp3
  ├── Ghost-Story.mp3
  └── Village-River.mp3
```

---

## 📡 Audio Optimization

For best compatibility with slow networks and low-end devices:

```
  Recommended encoding:

  ┌──────────────┬─────────┬──────────┐
  │ Bitrate      │ Channels│ Best for       │
  ├──────────────┼─────────┼──────────┤
  │ 32 kbps      │ Mono    │ 2G / JioBharat │
  │ 48 kbps      │ Mono    │ Slow 3G        │
  │ 64 kbps      │ Mono    │ Standard 3G    │
  └──────────────┴─────────┴────────────────┘
```

---

## 🌐 Live Website

<div align="center">

### 🔗 [VISIT SITE](https://music.mp3x.xo.je)

</div>

---

## 🎯 Goal

> Build a music platform that remains **accessible regardless of device quality, internet speed, or location.**
>
> Because music belongs to everyone — not just people with fast phones.

---

## 👤 Creator

<div align="center">

[![Instagram](https://img.shields.io/badge/Instagram-%40real.ximanta-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/real.ximanta)
[![Portfolio](https://img.shields.io/badge/Portfolio-about.ximanta.xyz-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://about.ximanta.xyz)
[![Backup GitHub](https://img.shields.io/badge/Backup_GitHub-%40realtuku-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/realtuku)
[![Email](https://img.shields.io/badge/Email-realximanta%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:realximanta@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-%2B856_20_51_701_854-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/85620517018540)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:0a0a0a&height=120&section=footer&text=Technology+should+work+for+everyone&fontSize=14&fontColor=555555&fontAlignY=65&animation=fadeIn" width="100%"/>

</div>
