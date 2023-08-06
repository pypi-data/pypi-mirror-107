# Admin Search Plus

Admin Search Plus is a AdminMixin for Django that limits searches to specific fields which greatly enhances performance when working on large datasets.


## Installation

`$ pip install admin-search-plus`

Or through github:

`$ pip install -e git://github.com/Lenders-Cooperative/admin-search-plus#egg=admin-search-plus`

### Building from source

`$ python -m build`

`$ pip install admin_search_plus.whl`
## Usage

1. Add `admin_search_plus` to your `INSTALLED_APPS` before `django.contrib.admin`:
    
    ```
    INSTALLED_APPS = [
        'app_to_be_overrided',
        ...
        'admin_search_plus',
        ...
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    ```
    NOTE: To override a template, the app should be listed before `admin_search_plus`

2. In `admin.py` import `AdminSearchPlusMixin` to add search functions to `ModelAdmin`. 

    ```
    from admin_search_plus import AdminSearchPlusMixin

    class YourModelAdmin(AdminSearchPlusMixin, admin.ModelAdmin):
        admin_search_plus = True
        show_full_result_count = False
        show_result_count = False

    admin.site.register(YourModel, YourModelAdmin)

    ```

