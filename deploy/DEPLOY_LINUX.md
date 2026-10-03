# AAMAC Linux VPS Deployment

## 1. Copy the project

Copy the AAMAC project to:

`/var/www/aamac`

## 2. Create the virtual environment

Run:

`python3 -m venv /var/www/aamac/venv`

Then:

`/var/www/aamac/venv/bin/pip install -r /var/www/aamac/requirements.txt`

## 3. Configure production settings

Copy `.env.example` to `.env`.

Set:

- `APP_ENV=production`
- a long random `SECRET_KEY`
- a strong `ADMIN_PASSWORD`
- the production `DATABASE_URL`

For a serious production installation, use PostgreSQL.

## 4. Test Gunicorn

From `/var/www/aamac`:

`/var/www/aamac/venv/bin/gunicorn -c gunicorn.conf.py run:application`

Confirm the application responds on `127.0.0.1:8000`.

## 5. Install systemd service

Copy `deploy/aamac.service` to:

`/etc/systemd/system/aamac.service`

Then run:

`sudo systemctl daemon-reload`

`sudo systemctl enable aamac`

`sudo systemctl start aamac`

Check:

`sudo systemctl status aamac`

## 6. Configure Nginx

Copy `deploy/nginx.conf` into your Nginx site configuration and replace the example domain.

Enable the site, test Nginx:

`sudo nginx -t`

Then reload:

`sudo systemctl reload nginx`

## 7. Enable HTTPS

Use Certbot or the certificate tooling provided by the VPS host.

After HTTPS is active, keep:

`APP_ENV=production`

The application will then mark the administrator session cookie as HTTPS-only.

## 8. First admin setup

Visit:

`https://YOUR-DOMAIN/admin/login`

Use the credentials configured in `.env`.

Immediately change the initial administrator password to a unique production password.

## 9. Enter official church information

Replace the seeded placeholders with:

- the official three priest names and titles, if desired;
- the bishop's official name/title, if desired;
- the fourteen official family-group names;
- each family-group leader;
- the exact Sunday service times;
- the current weekly Sunday topic;
- the current Bible reference;
- church notices and announcements.

## 10. Exact location

The current contact page deliberately uses the supplied P.O. Box and Dugbe, Ibadan information without inventing a street address.

Once the church supplies the exact street address or Google Maps location, the map section can be connected to it.
