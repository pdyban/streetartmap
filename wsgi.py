from app import create_app

# create app object that can be called by WSGI server
application = create_app('production')