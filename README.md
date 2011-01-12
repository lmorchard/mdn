Mozilla Developer Network
=========================

[Mozilla][Mozilla] Developer Network is the successor of the
[Mozilla Developer Center][MDC]. MDN is a [Django][Django]-based web
application offering resources to developers in the Mozilla Community.

For project goals, specifications, etc., check out the
[MDN Wiki Page][wikimo].

[Mozilla]: http://www.mozilla.org
[MDC]: http://developer.mozilla.org
[Django]: http://www.djangoproject.com/
[wikimo]: https://wiki.mozilla.org/MDN

Getting Started
---------------
### Python
You need Python 2.6. Also, you probably want to run this application in a
[virtualenv][virtualenv] environment.

Run

    easy_install pip

followed by

    pip install -r requirements/prod.txt -r requirements/compiled.txt

to install the required Python libraries.

[virtualenv]: http://pypi.python.org/pypi/virtualenv

### Django
To initialize the database, run:

    ./manage.py syncdb
    schematic migrations/  # run schema migrations and add initial data

and to fetch the initial product details data, run:

    ./manage.py update_product_details

The Internet has plenty of of documentation on setting up a Django application
with any web server. If you need a wsgi entry point, you can find one in
``wsgi/mdn.wsgi``.

[Haystack]: http://haystacksearch.org/

    python manage.py compress_assets

### Django app configuration

The MDN Django app contains a file named `settings.py` which contains many
configuration settings used in the application. However, if you wish to change
any of thses (and you will), you should create a file named `settings_local.py`
starting with the following statement:

    from settings import *

Then, you can place any local overrides to the contents of `settings.py` in
this file, rather than changing the one in revision control.

### Third-party service settings

The Django app relies on a few third-party web services, which require the
configuration of various API keys.

[Recaptcha][] is used to provide abuse prevention measures on some forms. To
enable this, you'll need to register with the site and provide values for
the following settings:
    
    RECAPTCHA_USE_SSL = False # Set to true if using SSL
    RECAPTCHA_PRIVATE_KEY = '(private key from recaptcha)'
    RECAPTCHA_PUBLIC_KEY = '(public key from recaptcha)'

[recaptcha]: http://www.google.com/recaptcha

[bit.ly][] is used to shorten URLs for sharing. To enable this, you'll need to
register at [bit.ly][] and get a username and API key for these settings:

    BITLY_USERNAME = 'lmorchard'
    BITLY_API_KEY = "R_2653e6351e31d02988b3da31dac6e2c0"

[bit.ly]: https://bit.ly/a/your_api_key

### Upload directory for demo submissions

The Demo Room application requires a writable directory for media files that
can be served up to the web.

By default on a development machine, you may not need to make any changes here.

The location of this directory for writing files and building links is based on
the following two settings variables:

    # Filesystem path
    MEDIA_ROOT = path('media') 

    # URL base path
    MEDIA_URL = '/media/'

Under the location specified by `MEDIA_ROOT`, a subdirectory named `uploads` will
be used for storing user-submitted files (ie. screenshots and demo files). So,
make sure whatever is configured in settings has a directory `uploads`
available to which the Django application can write.

The `MEDIA_URL` variable should point to a base URL where the contents of the
`MEDIA_ROOT` directory can be accessed from the web.

### urls.py
Be careful with URI design. Do a search to make sure your top level path foo doesn't 
conflict with any [existing wiki pages][google_site_search]. Dekiwiki captures all traffic not sent 
explicitly to deki based on 

    configs/htaccess

When adding new urls.py paths, be sure to update this htaccess file.

[google_site_search]: http://www.google.com/search?q=site%3A%2F%2Fdeveloper.mozilla.org&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a#sclient=psy&hl=en&client=firefox-a&hs=lod&rls=org.mozilla:en-US%3Aofficial&q=site:%2F%2Fdeveloper.mozilla.org%2Ffoo

### Cron jobs
You want to update your product details periodically:

    ./manage.py update_product_details  # Mozilla Product Details update

The frequency is up to you, but anything quicker than once per hour is probably overkill.

Also, to update RSS feeds:

    ./manage.py update_feeds

### Other Packages
The Production MDN website relies on the following Aliases

* /forums is mapped to a phpBB instance
* / also is serviced by a Dekiwiki instance

License
-------
This software is licensed under the [Mozilla Tri-License][MPL]:

    ***** BEGIN LICENSE BLOCK *****
    Version: MPL 1.1/GPL 2.0/LGPL 2.1

    The contents of this file are subject to the Mozilla Public License Version
    1.1 (the "License"); you may not use this file except in compliance with
    the License. You may obtain a copy of the License at
    http://www.mozilla.org/MPL/

    Software distributed under the License is distributed on an "AS IS" basis,
    WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
    for the specific language governing rights and limitations under the
    License.

    The Original Code is Mozilla Developer Center.

    The Initial Developer of the Original Code is Mozilla.
    Portions created by the Initial Developer are Copyright (C) 2010
    the Initial Developer. All Rights Reserved.

    Contributor(s):
      Frederic Wenzel <fwenzel@mozilla.com>

    Alternatively, the contents of this file may be used under the terms of
    either the GNU General Public License Version 2 or later (the "GPL"), or
    the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
    in which case the provisions of the GPL or the LGPL are applicable instead
    of those above. If you wish to allow use of your version of this file only
    under the terms of either the GPL or the LGPL, and not to allow others to
    use your version of this file under the terms of the MPL, indicate your
    decision by deleting the provisions above and replace them with the notice
    and other provisions required by the GPL or the LGPL. If you do not delete
    the provisions above, a recipient may use your version of this file under
    the terms of any one of the MPL, the GPL or the LGPL.

    ***** END LICENSE BLOCK *****

[MPL]: http://www.mozilla.org/MPL/
