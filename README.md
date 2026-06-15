# Immigration Law AI

A Streamlit chatbot that answers immigration law questions worldwide and runs automated visa eligibility checks.

**Disclaimer:** This tool provides general information only. It is not a substitute for advice from a licensed immigration lawyer.

## Features

- **Ask mode** — chat about visa types, requirements, and processes for any country
- **Eligibility check** — automated visa eligibility scoring based on your profile and destination country
- **Profile storage** — saves your session profile and chat history locally for continuity

## Requirements

- Python 3.11+
- An [OpenRouter](https://openrouter.ai/) API key

## Local setup

```bash
git clone https://github.com/silatech00/immigration-law-test-app.git
cd immigration-law-test-app

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # add your OPENROUTER_API_KEY
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (see [GITHUB_AUTH.md](GITHUB_AUTH.md) if push fails).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with the **silatech00** GitHub account.
3. Click **New app** → select **silatech00/immigration-law-test-app**.
4. Set **Main file path** to `app.py`.
5. Under **Advanced settings → Secrets**, paste:

```toml
OPENROUTER_API_KEY = "your_openrouter_key"
OPENROUTER_MODEL = "openai/gpt-4o-mini"
```

6. Click **Deploy**.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | Your OpenRouter API key |
| `OPENROUTER_MODEL` | No | Model ID (default: `openai/gpt-4o-mini`) |

Local: set in `.env`. Streamlit Cloud: use **Secrets** (above).

## EU compliance demo

This repo is a sample target for an EU compliance scanner. Upload `docs/privacy_policy.md` alongside the codebase to demo document-vs-code conflict detection.
