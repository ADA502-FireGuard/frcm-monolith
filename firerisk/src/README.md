# DEVELOPMENT SETUP OF FIREGUARD CLOUD SERVICE
To set up the development environment, make sure poetry is installed with

```
poetry --version
```

Go into the top directory for the project, where you can see poetry.lock and myproject.toml.

Once you see these, install all dependencies for the project using

'''
poetry install
'''
This will also create a virtual environment that you can run the interpreter through with the dependencies for the project.
Make sure to have the IDE target that environment created by pypoetry.
This should install all dependencies, including fastapi and uvicorn.
To test the rest api, uvicorn has to be run inside the virtual environment. 

'''
poetry run uvicorn main:app --reload
'''

This should start the rest api on 127.0.0.1:8000