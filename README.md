# Flask Login/Register/Dashboard App

A simple Flask web app with:
- Register
- Login
- Dashboard (protected)
- Logout
- SQLite database

## 🚀 Deployment
1. Push this repo to GitHub.
2. Deploy to [Render](https://render.com) or Heroku.
   - For Render, set `Build Command` = `pip install -r requirements.txt`
   - Set `Start Command` = `gunicorn app:app`

## 🧪 Testing
Run Selenium tests with pytest:
```bash
pytest -v
