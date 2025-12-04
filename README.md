# FlashTick - Flashcard Practice Application

A beautiful, modern flashcard application with **Tick-8 Spaced Repetition System (SRS)** available in both **Python Desktop** and **HTML Web** versions.

<img src="assets/icon.png" alt="FlashTick Logo" width="250"/>

## 📦 Two Versions Available

<table>
<tr>
<td width="50%">

### 🖥️ Python Desktop App
Full-featured desktop application with offline support and direct Google Sheets integration. 

**Features:**
- ✅ Highly configurable
- ✅ Native performance
- ✅ Service account auth

**Quick Links:**
- [📥 Setup Instructions](#-setup-instructions)
- [🎮 Usage Guide](#-usage)
- [🐛 Troubleshooting](#-troubleshooting)

</td>
<td width="50%">

### 🌐 HTML Web App
Browser-based version with Google Sign-In and cloud sync. No installation required!

**Features:**
- ✅ Works anywhere
- ✅ Mobile-friendly
- ✅ Google Sign-In

**Quick Links:**
- [🚀 Quick Start](#-quick-start)
- [🔧 OAuth Setup](#-setup-your-google-cloud-project)
- [🐛 Web Troubleshooting](#-web-version-troubleshooting)

</td>
</tr>
</table>

**🆚 Not sure which to use?  [View comparison table](#-python-vs-html-comparison)**

---

# 🖥️ Python Desktop Version

## ✨ Features

- 📊 **Tick-8 SRS Algorithm** - Master cards in 8 progressive stages
- 🧠 **Smart Card Selection** - Prioritizes failed cards and learning progress
- 📅 **Daily Review System** - Cards become due based on practice history
- ✅ **Real-time Sync** to Google Sheets
- ⚙️ **Configurable Settings** (cards per session, spreadsheet selection)

## 📚 How Tick-8 SRS Works

### Learning Stages (0-8)
- **Stage 0**: Learning/Failed (highest priority)
- **Stages 1-7**: Progressive mastery
- **Stage 8**: Mastered (no longer appears in reviews)

### Card Progression
- ✅ **Correct Answer**: Advance one stage (0→1, 1→2, ...  7→8)
- ❌ **Incorrect Answer**: Reset to Stage 0
- ⏭️ **Skip**: No change to stage (card stays due)

### Review Schedule
- Cards practiced yesterday or before are **due today**
- Consistent daily practice is encouraged
- Mastered cards (Stage 8) never appear again

## 🚀 Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
```txt
PySide6==6.6.1
gspread==6.0.0
google-auth==2.27.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
```

### 2. Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create a **Service Account**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the details and create
5. Create a **Key**:
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create New Key"
   - Choose **JSON** format
   - Download the file
6. **Save the credentials**:
   - Create a `config` folder in your project root
   - Rename the downloaded file to `credentials.json`
   - Place it in `config/credentials.json`
7. **Share your Google Sheet**:
   - Open your Google Sheet
   - Click "Share"
   - Add the service account email (found in `credentials.json` as `client_email`)
   - Give it **Editor** access

### 3. Prepare Your Google Sheet

Your Google Sheet must have exactly these 5 columns:

| Column | Header | Description | Example |
|--------|--------|-------------|---------|
| A | Front | Question/Term | "Hallo" |
| B | Back | Answer/Translation | "Hello" |
| C | Last Practice Date | YYYY-MM-DD format | "2025-01-15" |
| D | SRS Stage | 0-8 | 3 |
| E | Number of Failed | Count of failures | 2 |

**Initial Setup:**
- Fill columns A and B with your flashcard content
- Leave columns C, D, E empty (or set to blank, 0, 0)
- The app will populate these automatically

**Example Sheet:**

| Front | Back | Last Practice Date | SRS Stage | Number of Failed |
|-------|------|-------------------|-----------|-----------------|
| Hallo | Hello | | 0 | 0 |
| Danke | Thank you | | 0 | 0 |
| Tschüss | Goodbye | | 0 | 0 |

### 4. Configure the Application

1. Run the application:
```bash
python main.py
```

2. Click **⚙ Settings**

3. Enter your **Spreadsheet ID**:
   - Open your Google Sheet
   - Copy the ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_HERE/edit
   ```

4. (Optional) Enter **Sheet GID** if using a specific sheet tab:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=SHEET_GID
   ```

5. Click **Connect to Google Sheet**

6. Adjust **Cards per session** (default: 20)

7. Click **Save Settings**

## 🎮 Usage

### Starting a Practice Session

1. **Home Screen**: View cards due for review today
2. **Start Practice**: Click "Start Practice" button
3. **Resume**: If a session is active, click "Resume Practice"
4. **New Session**: Force start a new session with "Start New Session"

### During Practice

1. **View Front**: The front of the card is shown with:
   - 🆕 NEW badge (if never practiced)
   - Stage indicator (e.g., "Stage 3/8")
2. **Reveal Card**: Click anywhere on the card to reveal the back
3. **Answer**:
   - **✓ Correct**: Advance to next stage
   - **✗ Incorrect**: Reset to Stage 0
   - **⏭ Skip**: Skip without changing stage
4. **Progress**: Track your progress with the progress bar

### Session Complete

After completing all cards, view your statistics:
- **Total Cards**: How many cards you reviewed
- **Correct**: Successfully answered
- **Incorrect**: Failed answers
- **Skipped**: Cards you skipped
- **Accuracy**: Percentage correct (excludes skipped)

Options:
- **Home**: Return to home screen
- **Practice Again**: Start a new session immediately

## 📁 Project Structure

```
flashcard-app/
├── main.py                      # Application entry point
├── ui/                          # User interface components
│   ├── main_window.py           # Main window and home view
│   ├── flashcard_view.py        # Card display with animations
│   ├── settings_view.py         # Settings configuration
│   ├── session_complete_view.py # Statistics display
│   └── styles.py                # UI styling constants
├── services/                    # Business logic
│   ├── google_sheets.py         # Google Sheets API integration
│   ├── flashcard_logic.py       # Tick-8 SRS algorithm
│   └── config_manager.py        # Configuration management
├── models/                      # Data models
│   └── flashcard.py             # Flashcard model with SRS
├── config/                      # Configuration files
│   ├── credentials.json         # Google API credentials (you create)
│   └── config.json              # App settings (auto-generated)
├── requirements.txt             # Python dependencies
├── FlashTick.svg                # Application logo (SVG)
├── icon.png                     # Application icon (PNG)
├── icon.ico                     # Application icon (ICO for Windows)
└── README.md                    # This file
```

## 🔧 Configuration Files

### `config/credentials.json`
Google Sheets API service account credentials (you create this). 

### `config/config.json` (auto-generated)
```json
{
  "cards_per_session": 20,
  "spreadsheet_id": "your_spreadsheet_id",
  "sheet_gid": ""
}
```

## 🐛 Troubleshooting

### "Not connected to Google Sheets"
- Verify `config/credentials.json` exists and is valid
- Ensure the service account email has **Editor** access to your sheet
- Check your internet connection
- Try clicking "Connect to Google Sheet" in Settings

### "No words found in the spreadsheet"
- Verify your sheet has the correct 5-column format
- Ensure there is data in columns A and B (beyond the header row)
- Check that columns C, D, E exist (can be empty)
- Verify the Spreadsheet ID is correct

### "No Cards Due"
- All your cards may be mastered (Stage 8)
- Or you've already practiced today
- Check your Google Sheet to see card stages and last practice dates

### Cards appear in wrong order
- Failed cards (Stage 0) should appear first
- Then new cards
- Then in-progress cards by stage
- Check the `flashcard_logic.py` priority calculation if needed

### Window/Taskbar icon not showing
- Ensure `icon.png` or `icon.ico` exists in project root
- Run `python convert_icon.py` to generate from SVG
- Run `python png_to_ico.py` to create ICO for Windows
- Restart the application

### Stats display is cropped
- The font automatically scales to fit available space
- Resize the window to trigger recalculation
- Minimum window size: 900x700 pixels

---

# 🌐 HTML Web Version

## ✨ Features

- 🌍 **Browser-Based** - No installation required, works on any device
- 🔐 **Google Sign-In** - Secure authentication with your Google account
- ☁️ **Cloud Sync** - Your data syncs automatically via Google Sheets
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 📊 **Same SRS System** - Identical Tick-8 algorithm as desktop version
- ⚡ **No Backend Required** - Runs entirely in the browser
- 🔒 **100% Private** - Your data stays in YOUR Google Sheet

## 🚀 Quick Start

### Option 1: Use Directly (Easiest)

1. Open `index.html` in your browser (or if using this repository, go to https://pfarahani.github.io/flashtick/)
2. Click **"Sign in with Google"**
3. Authorize access to your Google Sheets
4. Select or create your flashcard spreadsheet
5. Start practicing!

### Option 2: Host on GitHub Pages

1. Fork this repository
2. Go to **Settings** > **Pages**
3. Select source: **main branch** > **/(root)**
4. Save and wait for deployment
5. Access via: `https://yourusername.github.io/flashtick/`

### Option 3: Host Locally

```bash
# Simple HTTP server (Python 3)
python -m http.server 8000

# Or use Node.js
npx http-server

# Then open: http://localhost:8000
```

## 🔧 Setup Your Google Cloud Project

### 1. Create OAuth 2.0 Client ID

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Enable **Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create **OAuth 2.0 Client ID**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: **Web application**
   - Name: "FlashTick Web App"
   - Authorized JavaScript origins:
     ```
     http://localhost:8000
     https://yourusername.github.io
     ```
   - Authorized redirect URIs: (leave empty for client-side flow)
5. Copy your **Client ID** (looks like: `xxxxx.apps.googleusercontent.com`)

### 2. Configure the HTML File

Configure it in the app:
1. Open the app in browser
2. Click **⚙ Settings**
3.  Enter your Google Client ID
4. Click Save

### 3. Create Your Google Sheet

The sheet format is **identical** to the Python version:

| Front | Back | Last Practice Date | SRS Stage | Number of Failed |
|-------|------|-------------------|-----------|-----------------|
| Hallo | Hello | | 0 | 0 |
| Danke | Thank you | | 0 | 0 |

**Important:**
- You do NOT need to share this sheet with anyone
- You'll select it after signing in with Google
- The app accesses it using YOUR permissions

## 🎮 Using the Web App

### First Time Setup

1. **Sign In**: Click "Sign in with Google"
2. **Authorize**: Grant permissions to Google Sheets
3. **Configure**:
   - Enter your Spreadsheet ID (from the URL)
   - Optionally enter Sheet GID for specific tabs
   - Set cards per session (default: 20)
4. **Start**: Click "Start Practice"

### Daily Use

1. Open the app
2. Sign in if needed (may stay logged in)
3. View cards due for today
4. Click "Start Practice"
5. Review and answer cards
6. View session statistics

### Settings

Access via **⚙ Settings** button:
- **Google Client ID**: Configure OAuth credentials
- **Spreadsheet ID**: Change your active sheet
- **Sheet GID**: Target specific sheet tab
- **Batch Size**: Cards per session (5-100)
- **Theme Toggle**: Switch between light/dark mode

## 📱 Mobile Usage

The web version is fully responsive:
- **Touch-friendly**: Tap to flip cards
- **Swipe gestures**: (optional enhancement)
- **Adaptive layout**: Works on any screen size
- **PWA-ready**: Can be installed as app (future enhancement)

## 🔒 Privacy & Security

### What the App Accesses
- ✅ Your Google Sheets (read/write)
- ✅ Your Google profile (name, email for display)

### What the App Does NOT Access
- ❌ Other Google Drive files
- ❌ Gmail or Calendar
- ❌ Any data outside selected spreadsheet

### Data Storage
- **Local Storage**: Settings only (Client ID, Spreadsheet ID, batch size)
- **No Backend**: All data stays in YOUR Google Sheet
- **No Tracking**: No analytics or third-party services

### Security Best Practices
1. Only use on HTTPS sites (or localhost)
2. Keep your Client ID private (don't commit to public repos)
3. Review OAuth consent screen before authorizing
4. Revoke access anytime: [Google Account > Security > Third-party apps](https://myaccount.google.com/permissions)

## 🐛 Web Version Troubleshooting

### "Sign in failed"
- Check that your OAuth Client ID is correct
- Verify authorized origins include your domain
- Try clearing browser cache and cookies
- Check browser console for errors (F12)

### "Failed to fetch words"
- Ensure you've selected the correct Spreadsheet ID
- Check that the sheet has the 5-column format
- Verify you have edit permissions on the sheet
- Try signing out and back in

### "Redirect URI mismatch"
- Your OAuth Client ID must include your current domain
- Add `http://localhost:8000` for local testing
- Add your GitHub Pages URL for hosted version

### Dark mode not working
- Click the 🌙 icon in top-right
- Check localStorage is enabled in browser
- Try refreshing the page

### Cards not syncing
- Check internet connection
- Verify Google Sheets API is enabled
- Check browser console for API errors
- Try clicking "Refresh" in settings

## 🆚 Python vs HTML Comparison

| Feature | Python Desktop | HTML Web |
|---------|---------------|----------|
| **Installation** | Required | None |
| **Platform** | Windows/Mac/Linux | Any browser |
| **Offline Mode** | Yes (with cache) | No |
| **Authentication** | Service Account | OAuth (Google Sign-In) |
| **Setup Complexity** | Medium | Easy |
| **Mobile Support** | No | Yes |
| **Performance** | Faster | Depends on browser |
| **UI Framework** | PySide6 (Qt) | Pure HTML/CSS/JS |
| **Updates** | Manual | Auto (if hosted) |

## 💡 Tips for Both Versions

1. **Practice Daily**: The Tick-8 system works best with consistent daily practice
2. **Be Honest**: Mark answers truthfully for optimal learning
3. **Don't Skip Too Much**: Skipped cards count toward your session but don't advance
4. **Review Failed Cards**: These appear first in your sessions automatically
5. **Mastery Takes Time**: Expect 8+ days of correct answers to fully master a card
6. **Start Small**: Begin with 10-15 cards per session, increase gradually

## 🎯 Understanding Priority System

Cards are selected for practice in this order:

| Priority | Card Type | Stage | Characteristics |
|----------|-----------|-------|-----------------|
| **Highest** | Failed cards | 0 | Practiced before, got wrong |
| **High** | New cards | 0 | Never practiced |
| **Medium** | Learning cards | 1-3 | Early stages |
| **Low** | Advanced cards | 4-7 | Later stages |
| **Never** | Mastered cards | 8 | Fully learned |

## 📊 Example Learning Journey

**Day 1**: New card "Hallo" (Stage 0) → Answer **Correct** → Stage 1  
**Day 2**: "Hallo" due (Stage 1) → Answer **Correct** → Stage 2  
**Day 3**: "Hallo" due (Stage 2) → Answer **Incorrect** → Stage 0 (Reset!)  
**Day 4**: "Hallo" due (Stage 0, high priority) → Answer **Correct** → Stage 1  
...   
**Day 11**: "Hallo" (Stage 7) → Answer **Correct** → Stage 8 (**Mastered! **)  

The card never appears in reviews again!  🎉

## 🆘 Support

For issues or questions:
1. Check the appropriate troubleshooting section
2. Verify your Google Sheets/Cloud setup
3. Check browser console (F12) for errors (web version)
4. Review configuration files (desktop version)

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

Built with:
- **PySide6** - Qt for Python UI framework (Desktop)
- **gspread** - Google Sheets API wrapper (Desktop)
- **Google Identity Services** - OAuth authentication (Web)
- **Google Sheets API** - Cloud data sync (Both)
- **FlashTick Logo** - Custom SVG mascot

Happy Learning! 📚✨