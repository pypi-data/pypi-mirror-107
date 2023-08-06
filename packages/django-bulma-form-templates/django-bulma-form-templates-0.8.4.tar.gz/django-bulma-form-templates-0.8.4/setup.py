# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bulma',
 'bulma.management',
 'bulma.management.commands',
 'bulma.templatetags',
 'bulma.tests']

package_data = \
{'': ['*'],
 'bulma': ['static/bulma/css/*',
           'static/bulma/sass/*',
           'templates/*',
           'templates/_layouts/*',
           'templates/bulma/*',
           'templates/bulma/forms/*',
           'templates/bulma/forms/fields/*',
           'templates/registration/*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'django-bulma-form-templates',
    'version': '0.8.4',
    'description': 'Bulma CSS Framework for Django projects',
    'long_description': '## Fork of [Django Bulma (timonweb)](https://github.com/timonweb/django-bulma) \nThis fork moves more functionality into the templates, instead of adding CSS in python code.  \nIt is also more extensible, since templates can be included and blocks can be overriden.\n\nFor the added functionality, look at section [New Additions](#new-additions)\n\n# A Bulma Theme for Django Projects\n\n![Django Bulma](https://raw.githubusercontent.com/timonweb/django-bulma/master/test_project/static/images/django-bulma-logo.png)\n\nA Django base theme based on Bulma ([bulma.io](https://bulma.io/)). Bulma is a modern CSS framework based on Flexbox.\n\n*** work in progress ***\n\n## Installation\n\n1. Install the python package django-bulma from pip\n\n  ``pip install django-bulma``\n\n  Alternatively, you can install download or clone this repo and call ``pip install -e .``.\n\n2. Add to INSTALLED_APPS in your **settings.py**:\n\n  `\'bulma\',`\n\n3. If you want to use the provided base template, extend from **bulma/base.html**:\n\n  ```\n  {% extends \'bulma/base.html\' %}\n\n  {% block title %}Bulma Site{% endblock %}\n\n  {% block content %}\n    Content goes here...\n  {% endblock content %}\n\n  ```\n  \n4. If you want to customize bulma sass and your own components:\n\n    4.1 Copy bulma static files into your project\'s **STATIC_ROOT**:\n\n    ```\n    python manage.py copy_bulma_static_into_project\n    ```  \n    You should see **bulma** dir appeared in your **STATIC_ROOT**. It contains\n    two dirs:\n    * **sass** - this is the place where you can put your own sass code and customize\n    bulma variables\n    * **css** - this is where compiled sass output goes, you should link this file\n    in your base.html \n\n    4.2 Install npm packages for sass compilation to work:    \n    \n    ```\n    python manage.py bulma install\n    ```\n    \n    4.3 Start sass watch mode:\n    ```\n    python manage.py bulma start\n    ```\n\n5. For forms, in your templates, load the `bulma_tags` library and use the `|bulma` filters:\n\n    ##### Example template\n    \n    ```django\n\n    {% load bulma_tags %}\n\n    {# Display a form #}\n\n    <form action="/url/to/submit/" method="post">\n       {% csrf_token %}\n       {{ form|bulma }}\n       <div class="field">\n         <button type="submit" class="button is-primary">Login</button>\n       </div>\n       <input type="hidden" name="next" value="{{ next }}"/>\n    </form>\n    ```\n\n## Included templates\n\n**django-bulma** comes with:\n* a base template,\n* django core registration templates,\n\n## Bugs and suggestions\n\nIf you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.\n\n[https://github.com/nkay08/django-bulma/issues](https://github.com/nkay08/django-bulma/issues)\n\n# New Additions\nThe form and fields can be rendered in exactly the same way as before. \nHowever, fields can now also be used by simply including a template. \n## Templates\n- `bulma/forms/field.html`: The basic field template that is included by django-bulma\'s `form.html`\n- `bulma/forms/field_include.html`: Can be included directly with a `with field=form.<your_field>` statement. Does NOT add markup classes, but they can be provided manually.\n- `bulma/forms/bulma_field_include.html`: Can be included directly with a `with field=form.<your_field>` statement, and adds markup classes like the `bulma` template filter\n- `bulma/forms/bulma_inline_field_include.html`: Can be included directly with a `with field=form.<your_field>` statement, and adds markup classes like the `bulma_inline` template filter\n- `bulma/forms/bulma_horizontal_field_include.html`: Can be included directly with a `with field=form.<your_field>` statement, and adds markup classes like the `bulma_horizontal` template filter\n\nYou can customize the fields, e.g. by extending `bulma/forms/field_include.html` and overriding its blocks and then changing the respective setting.\n\n## Settings\nYou can specify which templates `django-bulma` uses for rendering forms and fields, and thus allow extensibility and customization.\nThese affect `django-bulma`\'s rendering template filters, but also all field templates that are prefixed with `bulma_`.\n\nOptions for `settings.py`:\n- `BULMA_FIELD_TEMPLATE`: Specifies which field template is used by bulma rendering. Default `"bulma/forms/field_include.html"`.\n- `BULMA_FIELD_WRAPPER_TEMPLATE`: Specifies which field wrapper template is used by bulma rendering. This wrapper coverts some context dicts to flat variables. Default `"bulma/forms/field.html"`.\n- `BULMA_FORM_TEMPLATE`: Specifies which form template is used by bulma rendering. Default `"bulma/forms/form.html"`.\n- `BULMA_FORMSET_TEMPLATE`: Specifies which formset template is used by bulma rendering. Default `"bulma/forms/formset.html"`. \n    \n## Bulma CSS\n\n- Inline icons: You can now generate inputs that have inline icons\n    - Add `has-icons-left` or `has-icons-right` or both as `classes_value` when including or providing them as parameter when using the `bulma` template tag \n    - You can specify the icon css class with the context `icon_left_class` and `icon_right_class` (currently only possible when including template)\n\n\n',
    'author': 'NKay',
    'author_email': 'n.klipp@nkay.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
