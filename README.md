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

5. **Apply database migrations:**
   Set up your local SQLite database with all the necessary tables for the applications (`creator`, `library`, `listener`, `song`, `user`, etc.):
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   If you want to access the Django admin interface:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The application should now be running. You can view it in your browser at `http://127.0.0.1:8000/`.
