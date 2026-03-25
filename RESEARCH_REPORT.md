# AUTONOMOUS FAN CHANNEL — Research Report
## How Others Have Approached This Problem

*Compiled from GitHub, Reddit, X/Twitter, Hacker News — March 2026*

---

## EXECUTIVE SUMMARY

We researched every corner of the internet to answer: **How do you build an autonomous Instagram fan channel that posts daily sermon clips without manual effort?**

**The answer is clear:** The safest, most sustainable approach is a **two-layer pipeline**:
1. **AI clipping layer** — Automatically extract the best 30-90 second moments from full sermons
2. **Official API publishing layer** — Schedule and post via Meta's Graph API (zero ban risk)

Trying to do this through unofficial/private APIs or browser automation **will get your account banned** in 2026. Meta has made that abundantly clear.

---

## 1. THE LANDSCAPE: TWO WORLDS

### SAFE WORLD (Official API + Approved Tools)
| What | Risk | How |
|------|------|-----|
| Publishing Reels via Graph API | **ZERO** | Meta officially supports this |
| Scheduling posts via Buffer/Later | **ZERO** | These are Meta Business Partners |
| AI clipping with Opus Clip/Sermon Shots | **ZERO** | Content creation only, no API interaction |
| Cross-posting via Repurpose.io | **LOW** | Uses official APIs |
| Workflow automation via n8n/Make | **LOW** | When using Graph API endpoints |

### DANGEROUS WORLD (Private APIs + Bots)
| What | Risk | How |
|------|------|-----|
| Instagrapi (private API) | **HIGH** | Reverse-engineered mobile API. Maintainers warn: "more suited for testing than a working business" |
| Selenium/browser automation | **VERY HIGH** | Easily detected. InstaPy (17.8K stars) is effectively dead |
| Auto-follow/unfollow bots | **BANNED** | 500K+ accounts actioned in H1 2025 |
| Cold DM automation | **BANNED** | Rate limits cut by 96% (5,000 to 200/hr) |
| GeeLark cloud phones | **HIGH** | Simulates real devices but violates TOS |
| Phone farms | **GREY** | Only engagement method BHW community still trusts, but expensive and fragile |

### What Happened in 2025: The Great Ban Wave
- **May-July 2025**: Meta deployed new AI moderation (LLaMA-based). Tens of thousands of accounts disabled overnight.
- **500,000+ accounts actioned** in H1 2025 for spammy/automated behavior
- **Chain bans** introduced: If one account is banned, connected accounts (same device, IP, payment method) get scrutinized
- Even **legitimate accounts** were caught in false-positive sweeps (30,000+ signed Change.org petitions)

**Bottom line: 2026 is NOT the year to use unofficial automation. The risk/reward is terrible.**

---

## 2. OPEN-SOURCE TOOLS THAT ALREADY EXIST

### A. Instagram API Libraries

| Tool | Stars | What It Does | Verdict |
|------|-------|-------------|---------|
| **instagrapi** | ~5,700 | Best Python wrapper for Instagram private API. Supports all post types. | Powerful but risky for production. Use Graph API instead for posting. |
| **instagrapi-rest** | — | RESTful wrapper around instagrapi | Same risk profile |
| **instagram_private_api** | ~2,800 | Older alternative | Legacy. Use instagrapi if you must. |

### B. AI Video Clipping (Long-Form → Short-Form)

| Tool | Stars | What It Does | Best For Us? |
|------|-------|-------------|-------------|
| **MoneyPrinterTurbo** | ~50,300 | AI generates videos from scratch (script + stock footage + TTS) | NO — generates from scratch, doesn't clip existing sermons |
| **AI-Youtube-Shorts-Generator** | ~2,300 | GPT-4 analyzes transcripts, finds best 2-min segments. Whisper + FFmpeg + OpenCV | **YES — strong candidate for sermon clipping** |
| **reels-clips-automator (Reelsfy)** | — | End-to-end: YouTube download → GPT highlight detection → face tracking → subtitles → vertical crop | **YES — closest to our exact use case** |
| **ClipCrafter AI** | — | Web UI, AWS-based clipping with face tracking | Possible but AWS costs add up |
| **ai-clips-maker** | — | Modular: transcribe → detect speakers → analyze scenes → crop | **YES — speaker diarization useful for sermons** |
| **Clipper** | — | AI moment detection + speaker cropping for podcasts/lectures | **YES — designed for speaker-focused content** |

### C. Subtitle/Caption Tools

| Tool | What It Does | Verdict |
|------|-------------|---------|
| **faster-auto-subtitle** | Whisper + FFmpeg subtitle burning. Docker + GPU support. | **Essential component.** 85% of Instagram watched on mute. |
| **AutoSubtitle** | GUI-based, runs on CPU, bilingual support | Good for local/Mac usage |
| **whisper.cpp** | C/C++ port of Whisper. Supports karaoke-style highlighting. | Fastest inference option |

### D. Scheduling & Distribution

| Tool | Stars | What It Does | Verdict |
|------|-------|-------------|---------|
| **Postiz** | ~24,800 | Full scheduling platform. 28+ platforms. REST API. Team collab. Docker. | **Best open-source scheduler. Could be our distribution layer.** |
| **Flask-SocialMedia-Automation** | — | Flask + instagrapi + OpenAI for scheduled posting | Simpler but uses private API |
| **n8n** | — | Open-source workflow automation. Graph API integration. | **Strong for orchestrating the full pipeline** |

---

## 3. COMMERCIAL TOOLS WORTH KNOWING

### AI Clipping Services
| Tool | Price | Reels? | Notes |
|------|-------|--------|-------|
| **Opus Clip** | Free trial, ~$15/mo | Yes | 10M+ users. Best general-purpose clipper. $30M Series A. |
| **Vidyo.ai / Quso** | ~$30/mo | Yes | Rebranded Dec 2024. 4M+ users. Template variety. |
| **Munch** | $49-220/mo | Yes | Best strategy integration but expensive. |
| **Sermon Shots** | Varies | Yes | Built specifically for churches. |
| **ChurchSocial.ai** | Varies | Yes | AI speaker tracking, multi-user, Planning Center integration. |
| **Pulpit AI** (Subsplash) | Varies | Yes | One sermon → 20+ content pieces. |
| **Choppity** | Varies | Yes | Context-aware clipping, transcript editing, face tracking. |

### Scheduling Services
| Tool | Price | Reels? | Notes |
|------|-------|--------|-------|
| **Buffer** | Free–$120/mo | Yes | Simplest. Good free tier. |
| **Later** | $25-80/mo | Yes | Best visual planner. Auto best-time. |
| **Hootsuite** | $199+/mo | Yes | Enterprise. Expensive. |
| **Blotato** | $29-499/mo | Yes | All-in-one. Works with n8n. 0→170K growth case study. |
| **Repurpose.io** | $25-125/mo | Yes | Cross-platform. One ban report. |

---

## 4. INSTAGRAM GRAPH API: THE FACTS

### What You CAN Do (Officially, Zero Risk)
- Publish Reels (up to 15 min/100MB via API, 90 sec recommended)
- Publish feed posts and carousels
- Schedule content up to 75 days in advance
- Read insights/analytics for your own account
- Manage comments on your posts
- Trial Reels (shared to non-followers only)

### What You CAN'T Do
- Post from personal accounts (Business/Creator only)
- Add trending music (API limitation)
- Exceed 25 posts per 24 hours (community consensus: stay under 20)
- Exceed 200 API calls per hour
- Use Google Drive links as media URLs (must be direct public URLs)

### Requirements
- Instagram Business or Creator account
- Linked to a Facebook Page
- Facebook Developer Account with app approval (2-8 weeks)
- Long-lived tokens (expire every 60 days, must auto-refresh)

### Developer Pain Points
- API documentation is notoriously poor
- Frequent breaking changes without notice
- Token management is a common source of pipeline failures
- Graph API v22 (2025) deprecated several endpoints and metrics

---

## 5. FFmpeg VIDEO SPECS FOR INSTAGRAM REELS

```
Codec: H.264 (libx264) + AAC audio
Resolution: 1080x1920 (9:16 vertical)
Frame rate: 30fps
Video bitrate: ~3,500 Kbps
Audio: Stereo, 128 Kbps
Profile: -profile:v main -level:v 3.1
Encoding: 2-pass for best quality/size ratio
Max file: <100MB
Duration: 30-90 seconds (sweet spot for engagement)
```

**Why pre-optimize:** Instagram aggressively re-encodes uploaded video. Properly optimized 1080p uploads look BETTER than raw 4K uploads after Instagram's compression.

---

## 6. WHAT OTHERS GOT WRONG (MISTAKES TO AVOID)

### Mistake 1: Using private API for what the official API can do
If you only need to PUBLISH content, use the Graph API. Don't risk your account with instagrapi for basic posting.

### Mistake 2: Building everything from scratch
Multiple open-source tools already solve individual pieces (clipping, subtitles, cropping). Combine them; don't reinvent.

### Mistake 3: Automating engagement
Likes, follows, comments — all get you banned in 2026. Automate PUBLISHING only. Keep engagement human.

### Mistake 4: Forgetting token refresh
Long-lived tokens expire after 60 days. Without automated refresh, your pipeline silently dies.

### Mistake 5: Posting from brand-new accounts with automation
New accounts have much lower action thresholds. Warm up manually for 2-4 weeks first.

### Mistake 6: Over-automating (100% automated)
Community consensus: automate ~70% of scheduling, keep 30% manual/spontaneous. Fully automated accounts lose authenticity and algorithmic favor.

### Mistake 7: Ignoring video optimization
Uploading non-optimized video = terrible quality after Instagram's re-encoding. Always pre-process with FFmpeg.

### Mistake 8: Building the full pipeline on day one
Start with just scheduling. Prove it works. Then add AI captions. Then clip generation. Iterate.

---

## 7. RECOMMENDED ARCHITECTURE

Based on ALL research across all 4 sources, here is the optimal pipeline:

```
┌─────────────────────────────────────────────────────┐
│                 AUTONOMOUS PIPELINE                  │
│              "You Must Pray" Fan Channel             │
├─────────────────────────────────────────────────────┤
│                                                      │
│  STEP 1: SOURCE                                      │
│  ├── YouTube (Dag Heward-Mills sermons/FLOW)         │
│  ├── yt-dlp (download full sermon)                   │
│  └── Store in content library                        │
│                                                      │
│  STEP 2: TRANSCRIBE                                  │
│  ├── Whisper / faster-whisper (local, free)           │
│  └── Output: Full transcript with timestamps         │
│                                                      │
│  STEP 3: AI HIGHLIGHT DETECTION                      │
│  ├── Claude API / GPT-4 analyzes transcript          │
│  ├── Identifies best 30-90 second moments            │
│  ├── Scores by: emotional peak, quotability,         │
│  │   scripture reference, viral potential             │
│  └── Output: Timestamp pairs for each clip           │
│                                                      │
│  STEP 4: VIDEO PROCESSING                            │
│  ├── FFmpeg extracts clip segments                   │
│  ├── OpenCV face tracking → 9:16 vertical crop       │
│  ├── faster-whisper → burned-in subtitles            │
│  ├── Brand overlay (watermark, colors)               │
│  └── Output: Ready-to-post Reel (.mp4)              │
│                                                      │
│  STEP 5: CAPTION & HASHTAG GENERATION                │
│  ├── Claude/GPT generates caption                    │
│  ├── Pattern-breaking CTA (per brand rules)          │
│  ├── Strategic hashtag set (rotated)                 │
│  └── Output: Caption text                            │
│                                                      │
│  STEP 6: REVIEW QUEUE (Optional)                     │
│  ├── Human approval before posting                   │
│  ├── Web UI or Telegram bot for quick approve/reject │
│  └── Can be bypassed for full autonomy               │
│                                                      │
│  STEP 7: PUBLISH                                     │
│  ├── Meta Graph API (official, zero ban risk)        │
│  ├── Schedule optimal time (from analytics)          │
│  ├── Auto-refresh tokens every 50 days               │
│  └── Cross-post to TikTok via Postiz or Repurpose   │
│                                                      │
│  STEP 8: ANALYTICS                                   │
│  ├── Track: reach, saves, shares, watch time         │
│  ├── Feed winning formats back into Step 3           │
│  └── Weekly performance report                       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Tech Stack Recommendation

| Layer | Tool | Why |
|-------|------|-----|
| Video download | yt-dlp | Best YouTube downloader, actively maintained |
| Transcription | faster-whisper | Fast, accurate, runs locally, free |
| AI Analysis | Claude API | Best at nuanced content analysis |
| Video processing | FFmpeg + OpenCV | Industry standard, free |
| Subtitles | faster-auto-subtitle | Whisper + FFmpeg in one tool |
| Publishing | Meta Graph API | Official. Zero ban risk. |
| Scheduling | n8n or Postiz | Open-source, self-hosted |
| Cross-posting | Postiz | 28+ platforms supported |
| Orchestration | Python + cron or n8n | Simple, reliable |

### Existing Repos to Build On (Don't Reinvent)

1. **reels-clips-automator** — Fork this as the base. It already does: YouTube download → GPT analysis → face tracking → subtitles → vertical crop
2. **AI-Youtube-Shorts-Generator** — Best highlight detection logic to port
3. **faster-auto-subtitle** — Plug in for subtitle burning
4. **Postiz** — Use as the scheduling/distribution backend
5. **instagrapi** — ONLY as fallback if Graph API can't do something specific

---

## 8. COST ESTIMATE

### DIY Open-Source Pipeline
| Component | Cost |
|-----------|------|
| Whisper (local) | Free |
| Claude API (highlight detection + captions) | ~$5-15/month (depending on volume) |
| FFmpeg, OpenCV, yt-dlp | Free |
| Meta Graph API | Free |
| Hosting (small VPS for n8n/cron) | ~$5-10/month |
| **TOTAL** | **~$10-25/month** |

### vs. Commercial All-in-One
| Tool | Cost |
|------|------|
| Opus Clip + Buffer | ~$25-35/month |
| ChurchSocial.ai | ~$30-100/month |
| Blotato | ~$29-97/month |

**The DIY approach is cheaper AND gives full control.** The commercial tools are easier to set up but lock you into their ecosystem and pricing.

---

## 9. PLATFORM DIRECTION (2026 Signals)

- **Adam Mosseri** stated 2026 will swing back to raw, realistic posts (AI content flooded feeds in 2025)
- Instagram's algorithm increasingly favors **content quality over follower count** — reach is decoupled from followers
- Meta's "Original Content Rules" for 2026 raise stakes for repurposed/recycled content
- Stories and Reels now share the same safe zone. Feed video shifting to 9:16.
- The message is clear: **quality > quantity, authenticity > polish**

---

## 10. DECISION MATRIX: BUILD vs BUY vs HYBRID

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Full DIY** (build pipeline) | Cheapest, full control, customizable | Dev time, maintenance burden | Technical teams, unique requirements |
| **Full Commercial** (Opus Clip + Buffer) | Fastest setup, no code | Monthly costs, less control, generic output | Non-technical teams, quick start |
| **Hybrid** (DIY clipping + commercial scheduling) | Best of both, moderate cost | Some integration work | Our recommended approach |

### OUR RECOMMENDATION: HYBRID
- **Build** the AI clipping pipeline (custom, branded, high-quality)
- **Use** Buffer or Meta Business Suite for scheduling (proven, safe, cheap/free)
- **Add** Postiz later for multi-platform distribution as we scale

This gives us full control over content quality (which is what differentiates us) while using battle-tested tools for the commodity parts (scheduling, publishing).

---

---

## 11. HACKER NEWS TECHNICAL DEEP-DIVE (Additional Findings)

### Meta Graph API: The Brutal Reality for Developers
- One developer reported **14 attempts and nearly 3 months** to get App Review approved for a basic use case (fetching comments on their own posts)
- In 2023, a critical token endpoint broke on a Friday evening affecting nearly every company using the API. Support tickets went unanswered. Status page stayed green.
- In 2018, Instagram abruptly retired endpoints without notifying even official Partners
- **HN consensus: Meta is an unreliable partner. Build defensively. Expect breaking changes with zero warning.**

### Technical Architecture Patterns (From Show HN Projects)
Production social media schedulers use:
- **NestJS + Kafka + Redis** (backend) + **Next.js** (landing) + **React + Vite** (frontend)
- Queue-based architecture for decoupling content generation from publishing
- Exponential backoff is mandatory for rate limit handling
- Webhooks over polling to avoid burning API calls

### GPU Processing Is Non-Negotiable
- Whisper transcription and video rendering are GPU-bound
- CPU-only processing is too slow for production video pipelines
- Self-hosting on GPU instances recommended over CPU-only VPS
- Word-level timestamps from Whisper are **essential** (sentence-level is insufficient for accurate clip extraction)

### The Legal Dimension
- Jan 2026: 17.5M Instagram records leaked via API scraping
- EU GDPR applies to any personal data regardless of public visibility
- Private API usage is a black-and-white TOS violation
- "Not getting caught yet is not proof of safety" — HN consensus

### Unified API Services (Alternative to Direct Graph API)
- **Ayrshare**, **Late (getlate.dev)**, **Upload-Post** — handle per-platform OAuth and format requirements
- These abstract away Meta's API complexity and handle token refresh automatically
- Trade-off: another dependency, but significantly less maintenance

---

*Research compiled from 4 parallel research agents scanning GitHub, Reddit, X/Twitter, and Hacker News.*
*Report date: March 2026*
*Next step: System architecture design and implementation plan*
