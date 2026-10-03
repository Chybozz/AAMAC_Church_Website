# AAMAC Church Website

Adeyinka Adegbite Memorial Anglican Church (AAMAC), Diocese of Ibadan South, Anglican Communion.

## What is included

- Responsive public church website.
- Glassmorphism + neumorphism visual system.
- Annual church theme section.
- Sunday and other service schedule.
- Weekly service topic and Bible reference fields.
- Public notice/announcement board.
- Secure administrator login.
- Admin dashboard.
- Admin notice publishing.
- Admin service management.
- Admin annual theme management.
- Admin leadership management.
- Admin family-group management.
- Fourteen initial family-group placeholders.
- Priest/Bishop records without requiring photographs.
- Church contact information.
- SQLite default database.
- PostgreSQL-compatible database configuration.
- Docker deployment support.
- Gunicorn + Uvicorn production configuration.

## Initial church content

The website starts with:

- Church: Adeyinka Adegbite Memorial Anglican Church.
- Short name: AAMAC.
- Diocese: Diocese of Ibadan South (Anglican Communion).
- Address: P.O Box 39926 Dugbe Ibadan.
- Telephone: 08032597090.
- Email: adeyinkaadegbitememorial@gmail.com.
- Facebook: https://www.facebook.com/groups/aamac
- Theme: MEGALEIOS - OUR YEAR OF GREAT THINGS.
- Bible reference: Luke 1:49.

The priest and bishop names are intentionally placeholders because names/photos were not supplied.

## Run locally on Windows

1. Install Python 3.12 or newer.
2. Open PowerShell in this project directory.
3. Create a virtual environment:

   python -m venv venv

4. Activate it:

   .\venv\Scripts\Activate.ps1

5. Install dependencies:

   pip install -r requirements.txt

6. Copy `.env.example` to `.env`.
7. Change `SECRET_KEY`.
8. Change `ADMIN_PASSWORD`.
9. Start the application:

   uvicorn run:application --reload

10. Open:

   http://127.0.0.1:8000

11. Open the administrator portal:

   http://127.0.0.1:8000/admin/login

## First login

The default values are controlled by `.env`.

Default username:

admin

Default password:

ChangeMe123!

Change the password before any production deployment.

## Production with PostgreSQL

Set DATABASE_URL in `.env` to a PostgreSQL connection string.

Example:

postgresql+psycopg://USERNAME:PASSWORD@HOST:5432/DATABASE

Then start with:

gunicorn -c gunicorn.conf.py run:application

For public deployment, put Nginx or another TLS reverse proxy in front of Gunicorn.

## Important production security checklist

- Replace SECRET_KEY with a long random value.
- Change ADMIN_PASSWORD before going live.
- Use HTTPS.
- Use PostgreSQL for a serious multi-user deployment.
- Keep `.env` outside source control.
- Do not commit `aamac.db` if it contains production information.
- Back up the production database.
- Restrict server SSH access.
- Keep Python and dependencies updated.
- Add a second administrator account workflow before expanding the admin team.
- Configure a real domain and SSL certificate.
- Replace the map placeholder after the church confirms the exact map location.
- Replace family-group placeholders with the official names and leaders.
- Replace leadership placeholders with official names/titles if the church wants them publicly displayed.

## Suggested first admin setup

After logging in:

1. Open Annual Theme and confirm the current year's theme.
2. Open Services and replace the seeded service records with the church's exact Sunday schedule.
3. Add the Sunday topic and Bible reference each week.
4. Open Notices and publish announcements.
5. Open Leadership and enter the three priests and bishop if the church wants names displayed.
6. Open Family Groups and replace the fourteen placeholders with official group names and leaders.
7. Preview the public site after each change.

## Project structure

app/
  config.py
  database.py
  main.py
  models.py
  security.py
  seed.py
  static/
    css/style.css
    js/app.js
    img/
  templates/
    base.html
    index.html
    about.html
    services.html
    notices.html
    theme.html
    leadership.html
    family_groups.html
    contact.html
    admin/
      base.html
      login.html
      dashboard.html
      notices.html
      services.html
      theme.html
      leaders.html
      family_groups.html

run.py
requirements.txt
Dockerfile
docker-compose.yml
gunicorn.conf.py
.env.example
README.md
