# AAMAC Church Website — Vercel Demo Deployment

This package is prepared for deployment of the AAMAC FastAPI/Jinja2 website on Vercel.

## Important database note

The local project can use SQLite for development, but the hosted admin dashboard should use PostgreSQL.
Set the `DATABASE_URL` environment variable in Vercel to a PostgreSQL connection string before deploying.

Vercel currently supports FastAPI directly on its Python runtime, including Python 3.14.

## Required Vercel environment variables

Set these in the Vercel project settings for Production (and Preview if desired):

- `APP_ENV=production`
- `SECRET_KEY=<long-random-secret>`
- `DATABASE_URL=<your-postgresql-connection-string>`
- `ADMIN_USERNAME=<your-admin-username>`
- `ADMIN_PASSWORD=<strong-admin-password>`

Do not commit the real values to GitHub.

## Recommended database

Neon PostgreSQL can be connected through the Vercel Marketplace. The application's existing SQLAlchemy configuration already supports PostgreSQL through `DATABASE_URL`.

## Deployment with Vercel CLI

1. Install the latest Vercel CLI:

   `npm install -g vercel@latest`

2. From this project folder, log in:

   `vercel login`

3. Link the folder to a Vercel project:

   `vercel link`

4. Add the environment variables in the Vercel dashboard.

5. Deploy a preview first:

   `vercel deploy`

6. Test the generated preview URL.

7. Deploy the tested version to production:

   `vercel deploy --prod`

## What to test after deployment

Public pages:

- `/`
- `/about`
- `/services`
- `/notices`
- `/theme`
- `/leadership`
- `/family-groups`
- `/contact`

Admin:

- `/admin/login`
- Login with the configured `ADMIN_USERNAME` and `ADMIN_PASSWORD`.
- Create/edit content and confirm it appears on the public pages.

## Why PostgreSQL is required for the hosted demo

Vercel functions are not a traditional always-running server. The local SQLite file should therefore not be treated as the persistent production database for the hosted admin system. PostgreSQL keeps notices, services, themes, leaders and family groups outside the application function and allows the admin dashboard to update shared data reliably.

## No custom domain required

Vercel automatically provides a deployment URL under `vercel.app`, so a domain is not required for the demo.
