# AVAS Redesign Proposal: Centralized Web Server + Local Announcement Client

## The Problem

Today, AVAS runs as a single application on one Windows PC connected to the hospital speakers. The web server (where staff submit blood requests) and the audio playback (speakers) are tightly coupled in the same process on the same machine. This means:

- Staff must be on the same local network to access the blood request form
- If that one PC goes down, both the web interface and announcements stop working
- Updating the web UI or managing users requires physical access to the speaker machine
- No visibility into whether an announcement actually played

## Proposed Solution

Split AVAS into two components that communicate over the internet via a simple REST API.

### 1. Central Web Server (cloud-hosted)

- Hosts the login page, blood request form, user management, and admin panel
- Accessible from anywhere over the internet — staff can submit requests from any device with a browser
- When a blood request is submitted, it saves it to a database as a "pending" announcement
- Shows real-time status of each request (pending → playing → done)

### 2. Announcement Client (hospital PC connected to speakers)

- Plays background bhajans continuously, exactly as it does today
- Every few seconds, checks the server for pending announcements
- When one is found: pauses music → raises volume → plays the announcement audio → resumes music
- Reports back to the server when the announcement is complete

## Communication Between Components

- The server exposes a simple API (e.g., `GET /api/pending`, `POST /api/done`)
- The client polls the server every 2-3 seconds — simple, reliable, works through any network/firewall
- Only structured data is sent over the network (e.g., `{"blood_groups": ["O+", "B-"]}`) — all audio files remain on the local machine, no large file transfers
- WebSockets or other real-time protocols are unnecessary given announcements happen a few times per day

## Authentication & Security

### Client ↔ Server (polling API)

- A **shared API key** (long random secret string) that the announcement client sends with every request in an `Authorization` header
- The server rejects any request without a valid key
- Only one client exists (the hospital speaker PC), so a shared key is sufficient
- If the key is ever compromised, rotate it on the server and update the client

### Staff ↔ Server (web UI)

- Upgrade from the current plaintext credential file to **proper password hashing** (bcrypt) + session tokens
- **Rate limiting** — e.g., max 5 requests per minute per user to prevent spam
- **HTTPS** — mandatory for all traffic so credentials and the API key are never sent in plaintext

## Why This Approach

| Concern | Why it matters |
|---|---|
| **Accessibility** | Staff can submit blood requests from any device, anywhere — not just the hospital LAN |
| **Reliability** | Server and speaker system are independent. Server going down doesn't stop bhajans; speaker PC rebooting doesn't lose pending requests |
| **Simplicity** | Polling + REST API is the simplest approach to build, debug, and maintain. No complex messaging infrastructure needed for a system that handles single-digit requests per day |
| **Minimal change to audio logic** | The announcement client reuses almost all of the existing audio code (Audio.py). The only change is *what triggers it* — an API response instead of a Flask route handler |
| **Visibility** | The server tracks every announcement's status, giving staff confirmation that their request was actually played |

## Tech Stack

- **Server**: Python / Flask + SQLite
- **Client**: Python script reusing existing audio modules (pyaudio, pygame, pycaw)
- **Communication**: REST API over HTTPS

## Architecture Diagram

```
                          Internet (HTTPS)
                               |
          +--------------------+--------------------+
          |                                         |
  Central Web Server                    Announcement Client
  (Cloud VM / Hosting)                  (Hospital PC + Speakers)
  ----------------------                ----------------------------
  Flask web app                         Bhajan player (pygame/VLC)
    - Login / auth                      Audio.py (pyaudio → speakers)
    - Blood request form                Volume control (pycaw)
    - Admin panel                       Polls: GET /api/pending
    - REST API                          Reports: POST /api/done/{id}
    - SQLite database
    - Request status tracking

  Staff submit requests                 Client picks up pending
  from any browser          -------->   requests, plays announcement,
                            (polling)   reports completion
```

## API Endpoints

| Endpoint | Method | Used By | Purpose |
|---|---|---|---|
| `/api/pending` | GET | Client | Fetch next pending announcement |
| `/api/done/{id}` | POST | Client | Mark announcement as completed |
| `/api/announce` | POST | Web UI | Submit a new blood request |
| `/login` | POST | Web UI | Staff authentication |
| `/admin` | GET | Web UI | User management, audit log |

## Open Questions

- **Fallback**: Should the announcement client have a local web UI as a backup in case internet goes down?
- **Hosting**: Where to host the central server (cloud provider, hospital-managed VM, etc.)?
- **Audit log**: How long to retain announcement history?
