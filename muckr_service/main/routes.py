import muckr_service.main

@muckr_service.main.blueprint.route('/')
def index():
    return 'Hello, world!'
