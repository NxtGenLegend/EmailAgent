# Email Agent

Simple Python tool to monitor your Gmail inbox and provide periodic email summaries.

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install email-agent
```

### Option 2: Install from Source

1. Clone or download this repository
2. Install dependencies:

```bash
# Using requirements.txt
pip install -r requirements.txt

# Or manual install
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

3. Run directly:
```bash
python email_agent/agent.py
```

## Setup Gmail API Access

### 1. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### 2. Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Download the JSON file
5. Rename it to `credentials.json`
6. Place it in your working directory

## Usage

### Using PyPI Installation

```bash
# Basic usage (checks every 30s, summary every 3 minutes)
email-agent

# Custom intervals
email-agent --check-interval 60 --summary-interval 300

# Custom email limit
email-agent --max-emails 50

# Show help
email-agent --help
```

### First Run Authentication

- Browser will open for Google authentication
- Grant permissions to read Gmail
- `token.pickle` file will be created for future use

## Command Line Options

- `--check-interval`: How often to check for new emails in seconds (default: 30)
- `--summary-interval`: How often to print summary in seconds (default: 180)
- `--max-emails`: Maximum number of emails to check (default: 20)

## What It Does

The tool will:
- Check for new emails at specified intervals
- Print real-time notifications when new emails arrive
- Provide periodic summaries with sender, subject, date, and preview
- Track processed emails to avoid duplicates
- Continue running until stopped with Ctrl+C

## File Structure (Source Installation)

```
EmailAgent/
  __init__.py
  agent.py
.gitignore
credentials.json    # You download this from Google
LICENSE
MANIFEST.in
pyproject.toml
README.md\
requirements.txt
setup.py 
token.pickle       # Auto-generated after first auth
```

## Development

To contribute or modify:

1. Clone the repository
2. Install in development mode:
```bash
pip install -e .
```
3. Make changes and test
4. Submit pull request

## Troubleshooting

**Authentication Error**: Delete `token.pickle` and run again

**API Error**: Check Gmail API is enabled in Google Cloud Console

**Permission Error**: Ensure `credentials.json` has correct permissions

**Module Not Found**: Make sure you installed the package correctly

**Credentials Not Found**: Make sure `credentials.json` is in your current working directory

## License

MIT License - see LICENSE file for details