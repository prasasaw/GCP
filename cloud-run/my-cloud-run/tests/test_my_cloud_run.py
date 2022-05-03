from my_cloud_run import __version__ 
from my_cloud_run import main

def test_version():
    assert __version__ == '0.1.0'

def test_message():
    message = main.hello_there()
    assert message == "hello there"
