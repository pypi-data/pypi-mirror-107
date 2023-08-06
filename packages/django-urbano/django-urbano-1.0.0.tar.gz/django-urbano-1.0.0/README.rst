
# django-urbano

## Starting
_These instructions will allow you to install the library in your python project._

### Current features

-   Get tracking info.

### Pre-requisitos

-   Python >= 3.7
-   Django >= 3
-   requests >= 2
***
## Installation

1. To get the latest stable release from PyPi:
```
pip install django-urbano
```
or

2. From a build
```
git clone https://gitlab.com/linets/ecommerce/oms/integrations/django-urbano
```

```
cd {{project}}
```

```
python setup.py sdist
```
and, install in your project django
```
pip install {{path}}/django-urbano/dist/{{tar.gz file}}
```

3. Settings in django project

```
DJANGO_URBANO = {
    'URBANO': {
        'BASE_URL': '<URBANO_BASE_URL>',
        'USER': '<URBANO_USER>',
        'PASSWORD': '<URBANO_PASSWORD>'
    }
}
```

## Usage

1. Get tracking info:
```
from urbano.handler import UrbanoHandler

handler = UrbanoHandler()

tracking_info = handler.get_tracking(<identifier>)
```
