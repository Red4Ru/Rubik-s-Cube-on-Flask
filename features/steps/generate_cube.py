from behave import given, step, when, then
from selenium.webdriver.common.by import By

from rubiks_cube.color import Color
from rubiks_cube_utils import get_cube, encode


def assert_rendered_cube(data_str, cube):
    get_color_repr = lambda color: "#00b400" if color == Color.GREEN else color.name
    for side in cube.get_sides():
        for row in side:
            for color in row:
                color_repr: str = get_color_repr(color)
                assert color_repr in data_str
                data_str: str = data_str.split(get_color_repr(color), 1)[1]


@given("I navigate to root page")
def step_impl(context):
    """
        Navigate to root page and the url will be http://127.0.0.1:5000/
    :type context: behave.runner.Context
    """
    context.browser.get("http://127.0.0.1:5000/")


@step("I choose size {size:d}")
def step_impl(context, size):
    """
        Find the html element 'size' using the id and input the required data
    :param size: size of cube
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.CSS_SELECTOR, "#size").send_keys(size)


@step("I enter valid seed")
def step_impl(context):
    """
        Find the html element 'seed' using the id and input the required data
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.CSS_SELECTOR, "#seed").send_keys(context.TEST_SEED)


@step('I enter seed "{seed}"')
def step_impl(context, seed):
    """
        Find the html element 'seed' using the id and input the required data
    :param seed: seed for generation of cube
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.CSS_SELECTOR, "#seed").send_keys(seed)


@step("I click on Start button")
def step_impl(context):
    """
        Find the input button on the html page which has id 'start'
        and invoke .click()
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.CSS_SELECTOR, "#start").click()


@then("Cube with size {size:d} is generated")
def step_impl(context, size):
    """
        If the generation is successful we will be redirected to http://127.0.0.1:5000/cube/<sides>/
        and also see the message "Seed: <seed>" on that page and cube with size 3
    :param size: size of cube
    :type context: behave.runner.Context
    """
    cube = get_cube(size, context.TEST_SEED)
    assert context.browser.current_url == f"http://127.0.0.1:5000/cube/{encode(cube)}/"
    assert f"Seed: {context.TEST_SEED}" in context.browser.page_source
    assert_rendered_cube(context.browser.page_source, cube)


@then("Error message is generated")
def step_impl(context):
    """
        If the generation is successful we will not be redirected to http://127.0.0.1:5000/cube/<sides>/
        but will be on the same page: http://127.0.0.1:5000/
        and also see the message "Invalid username or password !!" on that page
    :type context: behave.runner.Context
    """
    assert context.browser.current_url == f"http://127.0.0.1:5000/"
    assert "You can only use 8 digits and/or letters in seed"
