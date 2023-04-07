import threading
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler

from selenium import webdriver

from main import app

binary_yandex_driver_file = 'yandexdriver'

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--no-proxy-server')
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")


def setup_constants(context):
    context.TEST_SEED = "someSeed"


def before_all(context):
    context.server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()
    context.browser = webdriver.Chrome(binary_yandex_driver_file, options=options)
    context.browser.set_page_load_timeout(time_to_wait=200)
    setup_constants(context)


def after_all(context):
    context.browser.quit()
    context.server.shutdown()
    context.pa_app.join()
