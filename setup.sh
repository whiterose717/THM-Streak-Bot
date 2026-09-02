#!/bin/bash
# THM Streak Bot - Quick Setup Script
# Run this after forking the repository

echo "🚀 THM Streak Bot Setup"
echo "======================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists. Skipping creation."
else
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "📌 Please edit .env and fill in your credentials:"
    echo "   - THM_EMAIL: Your TryHackMe email"
    echo "   - THM_PASSWORD: Your TryHackMe password"
    echo "   - TELEGRAM_BOT_TOKEN: Bot token from @BotFather"
    echo "   - TELEGRAM_CHAT_ID: Your Telegram chat ID"
    echo "   - GH_TOKEN: GitHub PAT with repo and workflow scopes"
    echo ""
fi

# Check Python version
echo "🐍 Checking Python..."
python3 --version 2>/dev/null || echo "⚠️  Python 3 not found. Please install Python 3.8+"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt 2>/dev/null || pip install -r requirements.txt 2>/dev/null
echo "✅ Dependencies installed"

# Check for Firefox
echo ""
echo "🦊 Checking Firefox..."
if command -v firefox &> /dev/null; then
    echo "✅ Firefox found"
else
    echo "⚠️  Firefox not found. You'll need it to export cookies."
    echo "   Install Firefox, login to tryhackme.com, then run:"
    echo "   python3 export_cookies.py"
fi

# Export cookies
echo ""
echo "🍪 Cookie Export"
echo "================"
echo "To export your THM cookies:"
echo "1. Open Firefox"
echo "2. Login to tryhackme.com"
echo "3. Run: python3 export_cookies.py"
echo "4. Copy the base64 output"
echo "5. Add as GitHub secret: THM_FIREFOX_COOKIES"
echo ""

# Create GitHub secrets reminder
echo "🔑 GitHub Secrets Needed"
echo "========================"
echo "Go to your repo → Settings → Secrets → Actions"
echo ""
echo "Create these secrets:"
echo "  - THM_EMAIL: your@email.com"
echo "  - THM_PASSWORD: your_password"
echo "  - TELEGRAM_BOT_TOKEN: from @BotFather"
echo "  - TELEGRAM_CHAT_ID: your chat ID"
echo "  - THM_GH_PAT: GitHub PAT with repo+workflow scopes"
echo "  - THM_FIREFOX_COOKIES: base64 from export_cookies.py"
echo ""

# Enable actions reminder
echo "⚡ Enable GitHub Actions"
echo "======================="
echo "1. Go to your repo → Actions"
echo "2. Click 'I understand my workflows, go ahead and enable them'"
echo ""

echo "✅ Setup complete!"
echo ""
echo "📱 Telegram Commands:"
echo "   /now      - Maintain streak"
echo "   /new      - Solve new challenge"
echo "   /complete - Solve random room"
echo "   /logs     - Get run logs"
echo "   /status   - Check status"
echo ""
echo "📖 See README.md for detailed instructions"
