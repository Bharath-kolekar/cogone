# Voice-to-App SaaS Platform (India)

A production-ready Voice→App SaaS platform optimized for the Indian market. Convert natural-language/voice commands into working full-stack apps quickly with a free-first approach using local/browser AI.

## 🚀 Features

- **Voice-to-App Generation**: Convert voice commands to working apps in ~30s
- **Multi-Provider Payments**: Razorpay, PayPal, Google Pay, UPI, QR codes
- **Dual OTP Authentication**: Choose between Mobile OTP or Email OTP
- **Gamification**: Points, levels, streaks, referrals, leaderboards
- **Viral Features**: Share-to-earn, templates marketplace, collaborative editing
- **Free-First AI**: Local/browser processing with cloud fallbacks (HF/Together/Groq)
- **Mobile-First**: Optimized for Indian mobile users

## 🏗️ Tech Stack

### Frontend
- **Next.js 14** (App Router) + React Server Components + TypeScript + Turbopack
- **tRPC** for typed backend contracts
- **TanStack Query** for data fetching
- **Jotai** for local state management
- **shadcn/ui + Radix** for components
- **Tailwind CSS** for styling

### Backend
- **FastAPI** (Python 3.10+) with Pydantic, uvicorn, httpx
- **Supabase** (Postgres) with Row-Level Security
- **Upstash Redis** for caching and rate limiting

### AI & Voice
- **Local/Browser**: whisper-wasm, llama.cpp wasm
- **Cloud Fallbacks**: Hugging Face, Together, Groq (NO OpenAI)

### Payments
- **Razorpay**: UPI, cards, netbanking, subscriptions
- **PayPal**: International cards and PayPal checkout
- **Google Pay**: UPI deep-links and gateway integration
- **QR Codes**: Server-side QR generation

### Deployment
- **Frontend**: Vercel (Edge + Server Components)
- **Backend**: Render
- **Database**: Supabase
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker (for local development)

### Environment Setup

1. Copy environment variables:
```bash
cp .env.example .env.local
```

2. Fill in your API keys (see `.env.example` for required variables)

### Local Development

1. **Start Supabase locally:**
```bash
cd supabase
supabase start
```

2. **Start backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

3. **Start frontend:**
```bash
cd frontend
npm install
npm run dev
```

4. **Run tests:**
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# E2E tests
npm run test:e2e
```

## 📁 Project Structure

```
voice-to-app-saas/
├── frontend/                 # Next.js 14 + TypeScript
│   ├── app/                  # App Router
│   ├── components/           # shadcn/ui components
│   ├── lib/                  # tRPC, Supabase, hooks
│   └── styles/               # Tailwind CSS
├── backend/                  # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic
│   │   ├── models/           # Pydantic models
│   │   └── tests/            # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── shared/                   # TypeScript schemas
├── supabase/                 # Database schema & migrations
├── infra/                    # Deployment configs
├── .github/workflows/        # CI/CD
└── README.md
```

## 🔐 Authentication Flow

1. **User chooses OTP method**: Mobile OTP or Email OTP
2. **Mobile OTP**: SMS via Twilio/AWS SNS with country code support
3. **Email OTP**: Supabase Auth email verification
4. **OAuth**: Google, GitHub integration
5. **Protected routes**: Server-side middleware + tRPC auth

## 💳 Payment Integration

- **Razorpay**: Primary for India (UPI, cards, netbanking)
- **PayPal**: International and alternative payment method
- **Google Pay**: UPI deep-links and gateway integration
- **QR Codes**: Server-side generation for UPI payments
- **Webhooks**: Signature verification for payment confirmation

## 🎮 Gamification Features

- **Points System**: Award points for app creation, deployment, sharing
- **Levels & Unlocks**: Unlock templates, priority generation
- **Referrals**: Generate codes, track usage, award bonuses
- **Streaks**: Daily challenges and consistency rewards
- **Leaderboards**: Social competition and recognition

## 🤖 AI Orchestration

1. **Client-side**: whisper-wasm for ASR, local LLM for intent
2. **Server fallback**: HF/Together/Groq for complex generation
3. **Caching**: Redis-based rate limiting and result caching
4. **Privacy**: "Local Processing Only" toggle for sensitive data

## 🧪 Testing

- **Unit Tests**: pytest (backend), vitest (frontend)
- **E2E Tests**: Playwright for critical user flows
- **CI/CD**: GitHub Actions with smoke tests and preview deployments

## 📊 API Documentation

- **Backend API**: Available at `/openapi.json` when running locally
- **tRPC**: Type-safe client-server communication
- **Supabase**: Auto-generated from schema

## 🚀 Deployment

### Frontend (Vercel)
```bash
vercel --prod
```

### Backend (Render)
```bash
# Configure via render.yaml
```

### Database (Supabase)
```bash
supabase db push
```

## 🔧 Development Commands

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run development servers
npm run dev          # Frontend
uvicorn app.main:app --reload  # Backend
supabase start       # Database

# Run tests
npm test             # Frontend tests
pytest               # Backend tests
npm run test:e2e     # E2E tests

# Build for production
npm run build        # Frontend
docker build .       # Backend
```

## 📝 Environment Variables

See `.env.example` for all required environment variables. Key categories:

- **Supabase**: Database and auth configuration
- **Payments**: Razorpay, PayPal, Google Pay keys
- **AI Providers**: HF, Together, Groq API keys (optional)
- **SMS**: Twilio/AWS SNS for mobile OTP
- **Redis**: Upstash for caching and rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: Check this README and API docs
- **Issues**: GitHub Issues for bugs and feature requests
- **Discussions**: GitHub Discussions for questions

---

Built with ❤️ for the Indian market. Making app development accessible to everyone through voice commands.