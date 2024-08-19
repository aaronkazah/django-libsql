# Django + LibSQL / Turso

This project integrates Turso/Libsql with Django, allowing you to use Libsql as a database backend for your Django
applications.

## Installation

To install the package, use pip:

```
pip install django-libsql
```

## Configuration

To use Libsql as your database backend, update your Django settings as follows:

```python
DATABASES = {
    "default": {
        "ENGINE": "libsql.db.backends.sqlite3",
        "NAME": "libsql://${your-db-name}.turso.io?authToken=${your-auth-token}",
    }
}
```

Replace `${your-db-name}` and `${your-auth-token}` with your actual database name and authentication token.

## Usage

After configuration, you can use Django's ORM as usual. The Libsql backend will handle the database operations.

### Running a Local LibSQL Server

To start a local LibSQL server for development or testing, use the provided script:

```
./scripts/docker.sh
```

This script will start a LibSQL server in a Docker container.

### Running Django app

You can also clone this repository and run the example Django app:

```
git clone https://github.com/aaronkazah/django-libsql.git
cd django-libsql
./scripts/docker.sh
python manage.py migrate
python manage.py runserver
```

Feel free to modify the DATABASES configuration in `settings.py` to point to your local LibSQL server or turso.io.

### Running Tests

To run tests and verify the integration, use the provided script:

```
./scripts/test.sh
```

This script performs a self-lifecycle test:

1. It starts a local LibSQL server using Docker.
2. Runs the tests against this server.
3. Destroys the server at the end of the test run.

This process confirms that the integration is working correctly with an actual LibSQL server.

## Self-Hosting

If you want to host your own Libsql server, refer to the provided Docker script (`./scripts/docker.sh`). This script
includes a working server setup along with key generation.

## Known Issues

The current implementation has some limitations due to the lack of support for custom functions in the `libsql_client`:

1. Custom Django functions registered via `create_function` are not supported.
2. Certain Django ORM features that rely on these custom functions will not work. For example:
    - Date/time operations using `F()` objects
    - `dates()` queryset method

For a complete list of unsupported functions, query the `pragma_function_list` table in your database.

### Examples of Unsupported Operations

1. Date difference annotation:
   ```python
   Company.objects.annotate(date_diff=F("valid_until") - F("made_at"))
   ```

2. Date truncation in queryset:
   ```python
   Company.objects.dates("last_updated", "year")
   ```

These operations will raise `django.db.utils.OperationalError` due to missing functions.

## License

This project is distributed under the MIT license.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.