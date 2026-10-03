# AAMAC Signature Editorial Design System

This production pass uses the homepage as the visual benchmark and carries the same design language across the entire public site and administrator Content Studio.

## Public experience
- Bright ivory, white, teal and warm-gold palette.
- Floating translucent navigation with readable high-contrast controls.
- Editorial typography using Playfair Display and DM Sans.
- Clearly visible glassmorphism for navigation, hero cards and selected feature panels.
- Clearly visible neumorphism for tactile cards, controls and directory tiles.
- Cinematic hero treatment on internal pages.
- Consistent spacing, rounded geometry, shadows and visual hierarchy.
- Text is never intentionally placed over a low-opacity blur where readability suffers.
- Services, notices, annual theme, leadership, family groups and contact pages all use the same signature system as the homepage.

## Administrator experience
The admin area is a separate light Content Studio rather than a copy of the public navigation. It uses the same AAMAC colours, typography, tactile controls and editorial hierarchy while prioritising fast content management.

## Data and architecture
The redesign keeps the existing FastAPI, SQLAlchemy, SQLite/PostgreSQL configuration, session authentication, CSRF protection and database models. Existing routes remain available so the presentation can be improved without unnecessarily changing the backend contract.
