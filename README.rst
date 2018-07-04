# Install
::
    pip install -e .

# Run
::
    export FLASK_APP=seeker
    export FLASK_ENV=development
    flask init-db
    flask run

# Test
::
    pip install '.[test]'
    pytest

# Run with coverage report
::
    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
