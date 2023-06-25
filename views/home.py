from main import use_hyphen_case


def index():
    return {'message': 'Hello, world!'}


def a_view():
    return {'message': 'a'}


@use_hyphen_case
def b_view():
    return {'message': 'b'}


@use_hyphen_case
def hello_world():
    return {'ping': 'pong'}
