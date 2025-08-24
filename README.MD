Django with Vue Project Setup
This guide explains how to set up a new Django project integrated with Vue.js, using a Python virtual environment.
Prerequisites

Python 3.13 installed
Node.js and npm installed (for Vue.js) ['https://docs.npmjs.com/downloading-and-installing-node-js-and-npm']
Basic knowledge of Django and Vue.js

Other tools:
Yarn: (assumping npm installed)
AXIOS (can use fetch but this is better)
```
npm install --global yarn
npm install axios
```

# Setup Instructions
## 1. Create and Activate a Virtual Environment

### Create a directory for the project
```
mkdir django-with-vue
cd django-with-vue
```

### Create a virtual environment
```
\django-with-vue> python -m venv venv
```

### Activate the virtual environment
##### (assumes Windows)
```
venv\Scripts\activate
```

### Initialize your git
```
\django-with-vue> git init
```

- add ```/venv``` to your .gitignore file and any other ide specific files you want to exclude

## 2. Install Dependencies
### Create a folder called ```src```
#### This will reside within the django-with-view dir and where our main django core project and its applications will reside
```
\django-with-vue> mkdir src
cd src
```

### Create a requirements.txt file with the following content:
```
Django==5.2
psycopg2-binary==2.9.10  # postgres -  windows
```

### Install the dependencies
```
\django-with-vue\src> pip install -r .\requirements.txt
```

## 3. Set Up Django Project
 Create a new Django project inside the src dir

```
django-admin startproject tindalldemo tindalldemo .
```


## 4. Set Up Vue.js
VUE website['https://vuejs.org/about/releases']

```
npm init vue@latest
```

give it a project name 
(I am using tindall-frontend)
- do not need to worry too much about that
say No to defaults as prompted for now

## 5. Configure Django and Vue Integration

To avoid confusion, we are going to rename the ```src``` dir in our tindall-frontend.
- (i am using the dir name  ```frontend```)

Find any references to the src folder (e.g. ```src/``` ) in the tindall-frontend folders to the new name (```frontend``` or whatever you chose)

be sure to avoid renaming src references that are not the reference to the folder (e.g.   ```src=```   should not be changed)

Move the newly named frontend folder and the following folders up so they are at the same level as the original ```src``` folder.

```
frontend
public
index.html
package.json
```

### Delete the tindall-frontend folder
Since we moved all the relevant folders inside our django project, we can safely delete those.

### Install Vue with npm
```
npm install
```

Note that we did not run install until AFTER we made those dir changes.

NOTE: If you do not have nvm, you may want to install that to manage node versions - also you may want to install Yarn to get help with commmands.


#### Edit the scripts that will help us with our application (in package.json ) 
change the scripts "dev" to be 
```
    "dev": "vite build --mode development --base /static/vue-dev/ --outDir ./src/static/vue-dev/ -w",
    "build": "vite build --mode production --base /static/vue-prod/ --outDir ./src/static/vue-prod/",
```
so we ensure our build files are put in the staticdirs we want - note this production version is not hardened for prod - we would likely have the outdir be located elsewhere outside of django

the ```-w``` on the ```"dev"``` line is to be able to watch the builds so changes are addressed immediately 

to see what these commands do - e.g.
```
yarn vite build --help
```

now run it with:
```
npm run dev
```
or 
```
yarn dev
```

## update Static Files dirs:
in the settings:
```

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# ensure this is outside our django project
STATIC_ROOT = BASE_DIR.parent / "local-cdn" / "static"

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.parent / "local-cdn" / "media"
```
local-cdn can be whatever you want

then, run the server and navigate to one of the relative file paths to ensure that we are serving those static files
e.g. http://127.0.0.1:8000/static/vue-dev/assets/index-1234567


## Create a context processor to return the vue assets 
### this will be used by the templates to map vue front end assets (js and css files)

```
# do this as a context processor is that it is available on any template
from django.conf import settings

def vue_js_files(request):
    static_base_dir = settings.STATICFILES_BASE_DIR
    vue_dir = 'vue-prod' if settings.VUE_PROD else 'vue-dev'
    vue_dir = static_base_dir / vue_dir / "assets"
    js_files = [x.relative_to(static_base_dir) for x in vue_dir.glob("**/*.js")]
    css_files = [x.relative_to(static_base_dir) for x in vue_dir.glob("**/*.css")]
    print(str(js_files))
    print(str(css_files))
    return {
        "vue_js_paths": list(js_files),
        "vue_css_paths": list(css_files),
    }
```

add a templates folder and a base template
in settings: 

```
TEMPLATES = [
    {
    ...
        'DIRS': [BASE_DIR / "templates"],
    ...
    }
]
```

create the templates dir a base.html and a home.html that extends base


Build the Vue project:
```
cd frontend
npm run build
cd ..
```

## Create templates folder

Create a simple Django view in an app if you have one or create a views.py in the main project
```
pythonfrom django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

Map the view to a URL in tindalldemo/urls.py:

```
pythonfrom django.urls import path
from core import views

urlpatterns = [
    path('home', views.home_view, name='home'),
]
```
### Set your base template 
base.html
```
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        {% block content %}
        {% endblock %}

        {% for file in vue_js_paths %}
          <script src="{% static file%}"></script>
        {% endfor %}
    </body>
</html>
```

you can leave off the vue context process files to see that things are loading

## 6. Run the Development Server
```
python manage.py runserver
```


## 7. Next Steps

Develop your Django backend in the core app.
Build your Vue frontend in the frontend directory.
Use Django REST Framework for API integration with Vue if needed.

# from VUE install readme:
# tindall-frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```
