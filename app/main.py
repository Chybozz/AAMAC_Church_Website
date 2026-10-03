# Import the standard library URL parser for safe redirect validation.
from urllib.parse import urlparse

# Import FastAPI application primitives.
from fastapi import Depends, FastAPI, Form, Request
# Import redirect and HTML response classes.
from fastapi.responses import HTMLResponse, RedirectResponse
# Import static file serving.
from fastapi.staticfiles import StaticFiles
# Import Jinja2 template rendering.
from fastapi.templating import Jinja2Templates
# Import signed session middleware.
from starlette.middleware.sessions import SessionMiddleware
# Import SQLAlchemy query helpers.
from sqlalchemy import delete, select

# Import application configuration.
from .config import settings
# Import database dependency and initialization helpers.
from .database import get_db
# Import database models.
from .models import AdminUser, ChurchTheme, FamilyGroup, Leader, Notice, Service
# Import password and CSRF helpers.
from .security import ensure_csrf_token, require_admin, validate_csrf, verify_password
# Import database seed helpers.
from .seed import create_tables, seed_initial_data


# Create the FastAPI application object.
app = FastAPI(
    title="AAMAC | Adeyinka Adegbite Memorial Anglican Church",
    description="Official church website and content administration system.",
    version="1.0.0",
)


# Add signed session support for secure admin authentication.
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="aamac_admin_session",
    same_site="lax",
    https_only=settings.app_env.lower() == "production",
    max_age=60 * 60 * 8,
)


# Mount the public CSS, JavaScript and image directory.
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Create the Jinja template engine.
templates = Jinja2Templates(directory="app/templates")


# Render templates through the current Starlette request-first API while keeping
# the route handlers simple and consistent across the public and admin pages.
def render_template(template_name, context, status_code=200):
    # Read the request object already supplied by base_context().
    request = context["request"]
    # Use Starlette's current request-first TemplateResponse signature.
    return templates.TemplateResponse(request, template_name, context, status_code=status_code)


# Initialize tables and safe starter content when the application launches.
@app.on_event("startup")
def startup_event():
    # Create missing database tables.
    create_tables()
    # Add starter content without replacing existing content.
    seed_initial_data()


# Provide a small shared template context for public and admin pages.
def base_context(request: Request):
    # Return the current request and CSRF token to templates.
    return {
        "request": request,
        "csrf_token": ensure_csrf_token(request),
        "church_name": "Adeyinka Adegbite Memorial Anglican Church",
        "short_name": "AAMAC",
        "diocese": "Diocese of Ibadan South (Anglican Communion)",
        "phone": "08032597090",
        "email": "adeyinkaadegbitememorial@gmail.com",
        "po_box": "P.O Box 39926 Dugbe Ibadan",
        "facebook": "https://www.facebook.com/groups/aamac",
    }


# Return a safe redirect URL when the admin submits a local link.
def safe_link(value: str | None) -> str | None:
    # Treat an empty value as no link.
    if not value:
        return None
    # Parse the supplied URL.
    parsed = urlparse(value)
    # Allow only HTTPS, HTTP or relative URLs.
    if parsed.scheme in ("", "http", "https"):
        # Return the original safe URL.
        return value
    # Reject unsupported schemes such as javascript:.
    return None


# Render the public home page.
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db=Depends(get_db)):
    # Fetch the current church theme.
    theme = db.scalar(select(ChurchTheme).where(ChurchTheme.is_current.is_(True)))
    # Fetch the latest published notices.
    notices = db.scalars(
        select(Notice)
        .where(Notice.is_published.is_(True))
        .order_by(Notice.created_at.desc())
        .limit(3)
    ).all()
    # Fetch active Sunday and other service records.
    services = db.scalars(
        select(Service)
        .where(Service.is_active.is_(True))
        .order_by(Service.id.asc())
    ).all()
    # Fetch visible leadership records for the compact church presentation.
    leaders = db.scalars(
        select(Leader)
        .where(Leader.is_active.is_(True))
        .order_by(Leader.id.asc())
    ).all()
    # Fetch visible family groups for the church information page.
    groups = db.scalars(
        select(FamilyGroup)
        .where(FamilyGroup.is_active.is_(True))
        .order_by(FamilyGroup.id.asc())
    ).all()
    # Render the home page with dynamic church content.
    return render_template(
        "index.html",
        {**base_context(request), "theme": theme, "notices": notices, "services": services, "leaders": leaders, "groups": groups},
    )


# Render the church about page.
@app.get("/about", response_class=HTMLResponse)
def about(request: Request, db=Depends(get_db)):
    # Fetch publicly visible leadership records.
    leaders = db.scalars(select(Leader).where(Leader.is_active.is_(True)).order_by(Leader.id.asc())).all()
    # Fetch visible family groups for the church fellowship section.
    groups = db.scalars(select(FamilyGroup).where(FamilyGroup.is_active.is_(True)).order_by(FamilyGroup.id.asc())).all()
    # Render the focused church information page.
    return render_template(
        "about.html",
        {**base_context(request), "leaders": leaders, "groups": groups},
    )


# Render the services page.
@app.get("/services", response_class=HTMLResponse)
def services(request: Request, db=Depends(get_db)):
    # Fetch all active services.
    items = db.scalars(select(Service).where(Service.is_active.is_(True)).order_by(Service.id.asc())).all()
    # Render the service schedule.
    return render_template(
        "services.html",
        {**base_context(request), "services": items},
    )


# Render the public notices page.
@app.get("/notices", response_class=HTMLResponse)
def notices(request: Request, db=Depends(get_db)):
    # Fetch all published notices from newest to oldest.
    items = db.scalars(
        select(Notice).where(Notice.is_published.is_(True)).order_by(Notice.created_at.desc())
    ).all()
    # Render the notice board.
    return render_template(
        "notices.html",
        {**base_context(request), "notices": items},
    )


# Render the annual theme page.
@app.get("/theme", response_class=HTMLResponse)
def theme_page(request: Request, db=Depends(get_db)):
    # Fetch the current annual theme.
    theme = db.scalar(select(ChurchTheme).where(ChurchTheme.is_current.is_(True)))
    # Render the theme page.
    return render_template(
        "theme.html",
        {**base_context(request), "theme": theme},
    )


# Render the leadership page.
@app.get("/leadership", response_class=HTMLResponse)
def leadership(request: Request, db=Depends(get_db)):
    # Fetch active leaders.
    leaders = db.scalars(select(Leader).where(Leader.is_active.is_(True)).order_by(Leader.id.asc())).all()
    # Render the leadership page.
    return render_template(
        "leadership.html",
        {**base_context(request), "leaders": leaders},
    )


# Render the family groups page.
@app.get("/family-groups", response_class=HTMLResponse)
def family_groups(request: Request, db=Depends(get_db)):
    # Fetch active family groups.
    groups = db.scalars(
        select(FamilyGroup).where(FamilyGroup.is_active.is_(True)).order_by(FamilyGroup.id.asc())
    ).all()
    # Render the family group directory.
    return render_template(
        "family_groups.html",
        {**base_context(request), "groups": groups},
    )


# Render the church contact page.
@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    # Render contact details supplied by the church.
    return render_template(
        "contact.html",
        base_context(request),
    )


# Render the administrator login form.
@app.get("/admin/login", response_class=HTMLResponse)
def admin_login(request: Request):
    # Redirect an already authenticated administrator to the dashboard.
    if request.session.get("admin_user_id"):
        return RedirectResponse("/admin", status_code=303)
    # Render the login page.
    return render_template("admin/login.html", base_context(request))


# Process administrator login.
@app.post("/admin/login")
def admin_login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db=Depends(get_db),
):
    # Validate the submitted CSRF token before checking credentials.
    validate_csrf(request, csrf_token)
    # Find the administrator by username.
    admin = db.scalar(select(AdminUser).where(AdminUser.username == username))
    # Reject invalid or disabled administrator accounts.
    if not admin or not admin.is_active or not verify_password(password, admin.password_hash):
        # Return the login form with a generic error.
        return render_template(
            "admin/login.html",
            {**base_context(request), "error": "Invalid administrator credentials."},
            status_code=401,
        )
    # Store only the database ID in the signed session.
    request.session["admin_user_id"] = admin.id
    # Redirect to the dashboard after successful login.
    return RedirectResponse("/admin", status_code=303)


# Log out the administrator.
@app.post("/admin/logout")
def admin_logout(request: Request, csrf_token: str = Form(...)):
    # Validate the logout form's CSRF token.
    validate_csrf(request, csrf_token)
    # Clear the signed admin session.
    request.session.clear()
    # Redirect to the public home page.
    return RedirectResponse("/", status_code=303)


# Render the administrator dashboard.
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db=Depends(get_db)):
    # Require a valid administrator session.
    require_admin(request)
    # Count all notices.
    notice_count = len(db.scalars(select(Notice)).all())
    # Count all services.
    service_count = len(db.scalars(select(Service)).all())
    # Count all family groups.
    family_count = len(db.scalars(select(FamilyGroup)).all())
    # Count all leaders.
    leader_count = len(db.scalars(select(Leader)).all())
    # Render the dashboard.
    return render_template(
        "admin/dashboard.html",
        {
            **base_context(request),
            "notice_count": notice_count,
            "service_count": service_count,
            "family_count": family_count,
            "leader_count": leader_count,
        },
    )


# Show the administrator notice manager.
@app.get("/admin/notices", response_class=HTMLResponse)
def admin_notices(request: Request, db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Fetch all notices.
    items = db.scalars(select(Notice).order_by(Notice.created_at.desc())).all()
    # Render the notice manager.
    return render_template(
        "admin/notices.html",
        {**base_context(request), "notices": items},
    )


# Create a new notice.
@app.post("/admin/notices")
def admin_notice_create(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    link_url: str | None = Form(None),
    link_label: str | None = Form(None),
    is_published: bool = Form(False),
    csrf_token: str = Form(...),
    db=Depends(get_db),
):
    # Require administrator authentication.
    require_admin(request)
    # Validate the form's CSRF token.
    validate_csrf(request, csrf_token)
    # Add the new notice to the database.
    db.add(
        Notice(
            title=title.strip(),
            content=content.strip(),
            link_url=safe_link(link_url),
            link_label=(link_label or "").strip() or None,
            is_published=is_published,
        )
    )
    # Commit the new notice.
    db.commit()
    # Return to the notice manager.
    return RedirectResponse("/admin/notices", status_code=303)


# Delete a notice.
@app.post("/admin/notices/{notice_id}/delete")
def admin_notice_delete(request: Request, notice_id: int, csrf_token: str = Form(...), db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Delete the selected notice.
    db.execute(delete(Notice).where(Notice.id == notice_id))
    # Commit the deletion.
    db.commit()
    # Return to the notice manager.
    return RedirectResponse("/admin/notices", status_code=303)


# Show the administrator service manager.
@app.get("/admin/services", response_class=HTMLResponse)
def admin_services(request: Request, db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Fetch all service records.
    items = db.scalars(select(Service).order_by(Service.id.asc())).all()
    # Render the service manager.
    return render_template(
        "admin/services.html",
        {**base_context(request), "services": items},
    )


# Create a new service record.
@app.post("/admin/services")
def admin_service_create(
    request: Request,
    name: str = Form(...),
    day: str = Form(...),
    time: str = Form(...),
    topic: str | None = Form(None),
    bible_reference: str | None = Form(None),
    description: str | None = Form(None),
    is_active: bool = Form(False),
    csrf_token: str = Form(...),
    db=Depends(get_db),
):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Add the new service.
    db.add(
        Service(
            name=name.strip(),
            day=day.strip(),
            time=time.strip(),
            topic=(topic or "").strip() or None,
            bible_reference=(bible_reference or "").strip() or None,
            description=(description or "").strip() or None,
            is_active=is_active,
        )
    )
    # Persist the service.
    db.commit()
    # Return to the service manager.
    return RedirectResponse("/admin/services", status_code=303)


# Toggle a service's public visibility.
@app.post("/admin/services/{service_id}/toggle")
def admin_service_toggle(request: Request, service_id: int, csrf_token: str = Form(...), db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Find the selected service.
    item = db.get(Service, service_id)
    # Toggle it when it exists.
    if item:
        # Reverse the current public visibility state.
        item.is_active = not item.is_active
        # Save the change.
        db.commit()
    # Return to the service manager.
    return RedirectResponse("/admin/services", status_code=303)


# Delete a service.
@app.post("/admin/services/{service_id}/delete")
def admin_service_delete(request: Request, service_id: int, csrf_token: str = Form(...), db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Delete the selected service.
    db.execute(delete(Service).where(Service.id == service_id))
    # Persist the deletion.
    db.commit()
    # Return to the service manager.
    return RedirectResponse("/admin/services", status_code=303)


# Render the annual theme manager.
@app.get("/admin/theme", response_class=HTMLResponse)
def admin_theme(request: Request, db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Fetch all themes.
    themes = db.scalars(select(ChurchTheme).order_by(ChurchTheme.year.desc())).all()
    # Render the theme manager.
    return render_template(
        "admin/theme.html",
        {**base_context(request), "themes": themes},
    )


# Create or update an annual theme.
@app.post("/admin/theme")
def admin_theme_create(
    request: Request,
    year: int = Form(...),
    title: str = Form(...),
    subtitle: str = Form(...),
    bible_reference: str = Form(...),
    description: str | None = Form(None),
    is_current: bool = Form(False),
    csrf_token: str = Form(...),
    db=Depends(get_db),
):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # When the submitted theme is current, clear the previous current theme.
    if is_current:
        # Load all current themes and deactivate them.
        for current in db.scalars(select(ChurchTheme).where(ChurchTheme.is_current.is_(True))).all():
            current.is_current = False
    # Find an existing theme for the year.
    existing = db.scalar(select(ChurchTheme).where(ChurchTheme.year == year))
    # Update an existing year instead of creating duplicates.
    if existing:
        # Update the theme title.
        existing.title = title.strip()
        # Update the theme subtitle.
        existing.subtitle = subtitle.strip()
        # Update the Bible reference.
        existing.bible_reference = bible_reference.strip()
        # Update the description.
        existing.description = (description or "").strip() or None
        # Update current status.
        existing.is_current = is_current
    # Otherwise create a new theme.
    else:
        # Add the new annual theme.
        db.add(
            ChurchTheme(
                year=year,
                title=title.strip(),
                subtitle=subtitle.strip(),
                bible_reference=bible_reference.strip(),
                description=(description or "").strip() or None,
                is_current=is_current,
            )
        )
    # Save the theme.
    db.commit()
    # Return to the theme manager.
    return RedirectResponse("/admin/theme", status_code=303)


# Render the leadership manager.
@app.get("/admin/leaders", response_class=HTMLResponse)
def admin_leaders(request: Request, db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Fetch all leaders.
    leaders = db.scalars(select(Leader).order_by(Leader.id.asc())).all()
    # Render the leader manager.
    return render_template(
        "admin/leaders.html",
        {**base_context(request), "leaders": leaders},
    )


# Create a leader record.
@app.post("/admin/leaders")
def admin_leader_create(
    request: Request,
    name: str = Form(...),
    title: str = Form(...),
    bio: str | None = Form(None),
    is_active: bool = Form(False),
    csrf_token: str = Form(...),
    db=Depends(get_db),
):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Add the leader record.
    db.add(
        Leader(
            name=name.strip(),
            title=title.strip(),
            bio=(bio or "").strip() or None,
            is_active=is_active,
        )
    )
    # Persist the record.
    db.commit()
    # Return to the leader manager.
    return RedirectResponse("/admin/leaders", status_code=303)


# Toggle a leader's public visibility.
@app.post("/admin/leaders/{leader_id}/toggle")
def admin_leader_toggle(request: Request, leader_id: int, csrf_token: str = Form(...), db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Find the selected leader.
    leader = db.get(Leader, leader_id)
    # Toggle the visibility when found.
    if leader:
        # Reverse the active flag.
        leader.is_active = not leader.is_active
        # Persist the change.
        db.commit()
    # Return to the leader manager.
    return RedirectResponse("/admin/leaders", status_code=303)


# Delete a leader.
@app.post("/admin/leaders/{leader_id}/delete")
def admin_leader_delete(request: Request, leader_id: int, csrf_token: str = Form(...), db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Delete the leader record.
    db.execute(delete(Leader).where(Leader.id == leader_id))
    # Persist the deletion.
    db.commit()
    # Return to the leader manager.
    return RedirectResponse("/admin/leaders", status_code=303)


# Render the family group manager.
@app.get("/admin/family-groups", response_class=HTMLResponse)
def admin_family_groups(request: Request, db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Fetch all family groups.
    groups = db.scalars(select(FamilyGroup).order_by(FamilyGroup.id.asc())).all()
    # Render the family group manager.
    return render_template(
        "admin/family_groups.html",
        {**base_context(request), "groups": groups},
    )


# Create a family group.
@app.post("/admin/family-groups")
def admin_family_group_create(
    request: Request,
    name: str = Form(...),
    leader_name: str = Form(...),
    description: str | None = Form(None),
    is_active: bool = Form(False),
    csrf_token: str = Form(...),
    db=Depends(get_db),
):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Add the family group.
    db.add(
        FamilyGroup(
            name=name.strip(),
            leader_name=leader_name.strip(),
            description=(description or "").strip() or None,
            is_active=is_active,
        )
    )
    # Save the group.
    db.commit()
    # Return to the group manager.
    return RedirectResponse("/admin/family-groups", status_code=303)


# Toggle a family group's public visibility.
@app.post("/admin/family-groups/{group_id}/toggle")
def admin_family_group_toggle(request: Request, group_id: int, csrf_token: str = Form(...), db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Find the family group.
    group = db.get(FamilyGroup, group_id)
    # Toggle the group when found.
    if group:
        # Reverse the public visibility.
        group.is_active = not group.is_active
        # Save the change.
        db.commit()
    # Return to the family group manager.
    return RedirectResponse("/admin/family-groups", status_code=303)


# Delete a family group.
@app.post("/admin/family-groups/{group_id}/delete")
def admin_family_group_delete(request: Request, group_id: int, csrf_token: str = Form(...), db=Depends(get_db)):
    # Require administrator authentication.
    require_admin(request)
    # Validate the CSRF token.
    validate_csrf(request, csrf_token)
    # Delete the selected family group.
    db.execute(delete(FamilyGroup).where(FamilyGroup.id == group_id))
    # Save the deletion.
    db.commit()
    # Return to the family group manager.
    return RedirectResponse("/admin/family-groups", status_code=303)
