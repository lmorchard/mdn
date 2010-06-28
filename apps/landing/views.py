import jingo


def home(request):
    """Home page."""
    return jingo.render(request, 'landing/home.html')


def addons(request):
    """Add-ons landing page."""
    return jingo.render(request, 'landing/addons.html')


def apps(request):
    """Applications landing page."""
    return jingo.render(request, 'landing/apps.html')


def docs(request):
    """Docs landing page."""
    return jingo.render(request, 'landing/docs.html')


def mobile(request):
    """Mobile landing page."""
    return jingo.render(request, 'landing/mobile.html')


def web(request):
    """Web landing page."""
    return jingo.render(request, 'landing/web.html')
