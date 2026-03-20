# 🚀 VC Pitch Generator

Transform any stupid startup idea into a buzzword-heavy VC pitch with 11 professionally formatted sections. **The perfect tool for content creators, startup enthusiasts, and tech humor lovers.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🎯 What Is This?

VC Pitch Generator takes any simple (or stupid) startup idea and transforms it into a full, buzzword-heavy VC pitch deck. Users input their idea, and the app generates an 11-section pitch including:

1. 🚀 **Startup Name + Tagline**
2. 🎯 **Problem Statement**
3. 💡 **Solution**
4. 🧠 **The Tech** (maximum absurdity)
5. 📈 **Market Opportunity**
6. 💰 **Business Model**
7. 🧲 **Traction**
8. 🆚 **Competitive Advantage**
9. 🛣️ **Roadmap**
10. 💸 **The Ask**
11. 💀 **Reality Check** (the viral hook)

**Example:**
- Input: "Food delivery app for college students"
- Output: "QuickBite AI - Redefining hyperlocal food logistics for Gen Z" with full VC-style pitch

---

## ✨ Features

- ✅ **AI-Powered Pitch Generation** - Uses Groq API (free tier available)
- ✅ **11-Section Structured Output** - Professional, copy-paste ready
- ✅ **Beautiful UI/UX** - Smooth animations, responsive design
- ✅ **Rate Limiting** - 10 req/min per IP (prevents abuse)
- ✅ **Copy & Share** - One-click copy, social sharing, PDF export
- ✅ **Error Handling** - Graceful error messages
- ✅ **Interactive API Docs** - Built-in Swagger UI
- ✅ **Production Ready** - Deployment configs included
- ✅ **Mobile Responsive** - Works on all devices
- ✅ **Viral Potential** - Reality Check section is the shareability hook

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (modern, async, fast)
- **LLM**: Groq API (free tier, 1-2s inference)
- **Language**: Python 3.8+
- **Validation**: Pydantic
- **Rate Limiting**: In-memory (production-ready)

### Frontend
- **Framework**: React 18+ (Vite)
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion / CSS
- **HTTP**: Fetch API
- **Icons**: Lucide React + Emojis

### Infrastructure
- **Backend Hosting**: Railway, Render, or Heroku
- **Frontend Hosting**: Vercel, Netlify
- **Cost**: ~$5/month (or free tier)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+ (for frontend)
- Groq API key (free from https://console.groq.com/keys)

### Backend Setup (5 minutes)

```bash
# Clone repo
git clone https://github.com/KshaunishHarsha/vc-pitch-generator.git
cd vc-pitch-generator/vc-pitch-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk_your_key_here

# Run server
python main.py
# Visit http://localhost:8000/docs
```

### Frontend Setup

```bash
# In new terminal, navigate to frontend folder
cd vc-pitch-generator/vc-pitch-frontend

# Install dependencies
npm install

# Create .env
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Run dev server
npm run dev
# Visit http://localhost:5173
```

---

## 📡 API Documentation

### Health Check
```bash
GET /health
# Returns: {"status": "healthy", "service": "vc-pitch-generator", "version": "1.0.0"}
```

### Get Example Ideas
```bash
GET /api/examples
# Returns: {"success": true, "examples": ["Food delivery for college students", ...]}
```

### Generate Pitch (Main Endpoint)
```bash
POST /api/generate-pitch
Content-Type: application/json

{
  "idea": "food delivery app for college students"
}

# Response (200):
{
  "success": true,
  "pitch": {
    "input_idea": "food delivery app for college students",
    "sections": [
      {
        "id": 1,
        "emoji": "🚀",
        "title": "STARTUP NAME + TAGLINE",
        "content": "QuickBite AI\n\"Redefining hyperlocal food logistics for Gen Z\""
      },
      ... (sections 2-11)
    ]
  },
  "error": null
}
```

### Interactive API Docs
Visit `http://localhost:8000/docs` for Swagger UI with full endpoint documentation and testing.

---

## 📁 Project Structure

```
vc-pitch-generator/
├── vc-pitch-backend/              # FastAPI backend
│   ├── main.py                   # Entry point
│   ├── config.py                 # Settings
│   ├── models.py                 # Data models
│   ├── requirements.txt          # Dependencies
│   ├── .env.example              # Example env file
│   ├── Procfile                  # Deployment config
│   │
│   ├── services/
│   │   └── groq_service.py       # Groq API integration
│   ├── routes/
│   │   └── pitch.py              # API endpoints
│   ├── utils/
│   │   └── validators.py         # Input validation
│   └── middleware/
│       └── rate_limit.py         # Rate limiting
│
└── vc-pitch-frontend/            # React frontend
    ├── src/
    │   ├── App.jsx               # Main component
    │   ├── api.js                # API calls
    │   ├── components/
    │   │   ├── InputSection.jsx
    │   │   ├── OutputSection.jsx
    │   │   ├── LoadingState.jsx
    │   │   └── PitchCard.jsx
    │   └── styles/
    │       └── globals.css
    ├── package.json
    ├── vite.config.js
    └── .env.example
```

---

## 🚀 Deployment

### Deploy Backend to Railway

```bash
# 1. Create account at https://railway.app
# 2. Connect GitHub repo
# 3. Add environment variable: GROQ_API_KEY=gsk_xxx
# 4. Deploy!
# 5. Get public URL (e.g., https://vc-pitch-api.railway.app)
```

### Deploy Frontend to Vercel

```bash
# 1. Create account at https://vercel.com
# 2. Connect GitHub repo
# 3. Add environment variable: REACT_APP_API_URL=https://your-backend-url.com
# 4. Deploy!
```

---

## 💰 Cost Analysis

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| Groq API | FREE | ~600 req/hour free tier |
| Railway | $0-5 | Free tier available |
| Vercel | FREE | Free tier |
| **Total** | **$0-5** | Scales to ~$10 at 1M req/month |

**vs Claude API**: At scale, saves ~$300/month! 🎉

---

## 🧪 Testing

### Local Testing
```bash
# Terminal 1: Run backend
cd vc-pitch-backend
python main.py

# Terminal 2: Run frontend
cd vc-pitch-frontend
npm run dev

# Visit http://localhost:5173
```

### Test Endpoints with cURL
```bash
# Health check
curl http://localhost:8000/health

# Get examples
curl http://localhost:8000/api/examples

# Generate pitch
curl -X POST http://localhost:8000/api/generate-pitch \
  -H "Content-Type: application/json" \
  -d '{"idea":"Uber for socks"}'
```

---

## 🎨 Features Breakdown

### Input Section
- Large, inviting textarea (10-200 character limit)
- Character counter with visual feedback
- Pre-loaded example suggestions (clickable cards)
- "Surprised Me" button for random example

### Output Display
- 11 expandable/collapsible cards
- Smooth 0.3s animations
- Reality Check card with distinct red styling
- Copy individual sections or all at once
- Download as PDF or share on social media

### Loading State
- Animated spinner
- Rotating loading messages
- Progress indicator
- Estimated time: 2-4 seconds

### Error Handling
- Input validation (10-200 chars)
- Rate limit errors (429)
- Server errors (500) with retry
- Network errors with fallback
- User-friendly error messages

---

## 📊 API Rate Limiting

- **Per IP**: 10 requests/minute
- **Per IP**: 100 requests/hour
- **Response**: 429 Too Many Requests with retry-after header

Example error:
```json
{
  "success": false,
  "error": "Rate limit exceeded. Try again in 45 seconds."
}
```

---

## 🔐 Security

- ✅ API keys stored in `.env` (never committed)
- ✅ CORS configured for frontend origin
- ✅ Input validation on all endpoints
- ✅ Rate limiting to prevent abuse
- ✅ No SQL injection (Pydantic validation)
- ✅ HTTPS enforced in production

---

## 🌟 Example Output

**Input:**
```
"Blockchain-based social network for plants"
```

**Generated Pitch (excerpt):**

**🚀 STARTUP NAME + TAGLINE**
```
GreenChain Social
"Connecting flora through Web3 technology and AI-powered growth optimization"
```

**🧠 THE TECH**
```
Our proprietary blockchain-enabled multi-agent system leverages quantum computing
principles to optimize photosynthesis pathways. Real-time AI monitoring tracks
plant sentiment through biometric leaf analysis. Smart contracts ensure
transparent seed distribution across our decentralized garden network.
```

**💀 REALITY CHECK**
```
What it actually is: a Discord server where plant lovers share photos
```

---

## 🎯 Use Cases

- 📱 **Content Creators** - Generate hilarious startup pitch videos for TikTok/Instagram
- 🎬 **YouTubers** - Create comedy content about startup culture
- 💼 **Startup Enthusiasts** - Parody their own ideas or competitors
- 🎓 **Students** - Learn about VC pitch structure (humorously)
- 🤖 **AI/LLM Demos** - Showcase prompt engineering capabilities

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Development Roadmap

- [ ] User authentication (save favorite pitches)
- [ ] Pitch history & database
- [ ] Investor persona selector (change pitch tone)
- [ ] Actual PowerPoint/Deck generation
- [ ] Community leaderboard (funniest pitches)
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] API rate tier system

---

## 🐛 Known Issues

- Groq API models occasionally deprecate - update in `config.py`
- PDF export styling may vary by browser
- Mobile keyboard may cover textarea on some devices

---

## 📞 Support

- **Issues**: Open a GitHub issue with error logs
- **Docs**: Check `/docs` endpoint in API
- **Email**: [your-email@example.com]

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Groq for amazing free LLM inference
- FastAPI for elegant API framework
- React community for amazing tools
- All the startup founders who inspired this humor

---

## 🎉 Show Your Support

If you find this useful or entertaining, please:
- ⭐ Star the repo
- 🐦 Share on Twitter/LinkedIn
- 💬 Tag us in your TikTok pitches
- 🚀 Deploy it and go viral!

---

## 📊 Project Stats

- **Backend**: ~800 lines of Python
- **Frontend**: ~600 lines of React
- **Setup Time**: 10 minutes
- **Time to Viral**: ...depends on your content 😄

---

**Made with ❤️ by [Kshaunish]**

Happy pitching! 🚀
