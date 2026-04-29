# Chithara

Chithara is a Django-based web application containing several interconnected modules including `user`, `listener`, `creator`, `song`, `song_form`, and `library`.

## Project Setup

Follow these instructions to set up the project on your local machine.

### Prerequisites

- Python 3.8+
- `pip` package manager

### Installation Steps

1. **Clone the repository:**
```bash
   git clone https://github.com/peerawattae/Chithara.git
   cd Chithara
```

2. **Create a virtual environment:**
   Using a virtual environment is highly recommended to keep project dependencies isolated.
```bash
   python3 -m venv venv
```

3. **Activate the virtual environment:**
   - **macOS/Linux:**
```bash
     source venv/bin/activate
```
   - **Windows:**
```cmd
     .\venv\Scripts\activate
```

4. **Install dependencies:**
   Install the required packages using the `requirements.txt` file:
```bash
   pip install -r requirements.txt
```

5. **Set up environment variables:**
   Create a `.env` file in the project root (never commit this file):
```env
   # Generation strategy: "mock" (default, no API key) or "suno" (real AI)
   GENERATOR_STRATEGY=mock

   # Suno API key — only needed when GENERATOR_STRATEGY=suno
   SUNO_API_KEY=your_actual_suno_key_here

   # Google OAuth — required for login
   GOOGLE_OAUTH2_KEY=your_google_client_id_here
   GOOGLE_OAUTH2_SECRET=your_google_client_secret_here
```
   `.env` is already listed in `.gitignore` — your keys will not be committed.

6. **Set up Google OAuth credentials:**

   **Step 1 — Create a Google Cloud project:**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Click **Select a project** → **New Project** → give it a name → **Create**

   **Step 2 — Enable the Google+ API:**
   - Go to **APIs & Services** → **Library**
   - Search for `Google+ API` → click it → **Enable**

   **Step 3 — Configure the OAuth consent screen:**
   - Go to **APIs & Services** → **OAuth consent screen**
   - Select **External** → **Create**
   - Fill in **App name** (e.g. `Chitra`) and **User support email**
   - Under **Authorized domains** add `127.0.0.1` for local development
   - Click **Save and Continue** through the remaining steps

   **Step 4 — Create OAuth 2.0 credentials:**
   - Go to **APIs & Services** → **Credentials**
   - Click **Create Credentials** → **OAuth 2.0 Client ID**
   - Application type: **Web application**
   - Name: anything (e.g. `Chitra Local`)
   - Under **Authorized redirect URIs** click **Add URI** and add: