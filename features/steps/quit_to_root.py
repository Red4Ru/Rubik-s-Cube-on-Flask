import datetime
import random

from behave import given, step, when, then
from selenium.webdriver.common.by import By

from rubiks_cube_utils import encode, get_cube


@given("I navigate to cube page (size={size:d})")
def step_impl(context, size):
    """
        Navigate to cube page and the url will be http://127.0.0.1:5000/cube/<sides>/
        Also we track solving sequence just in case
    :param size: size of cube
    :type context: behave.runner.Context
    """
    cube = get_cube(size, context.TEST_SEED)
    context.browser.get(f"http://127.0.0.1:5000/cube/{encode(cube)}/")
    context.TEST_SOLVING_SEQUENCE = {
        2: "UDDBBL'B'UUR'FL",
        3: "LFF'B'B'BULUFL'F'D'RDU'D'D'B'BL'B'U'URFL",
        4: "RlU'L'u'd'l'D'b'uF'UD'u'F'Db'FFRd'lfFbb'b'u'l'u'f'l'F'dr'duD'd'bbl'buU'r'f'L",
        5: "b'b'LdBdL'd'LF'BuD'dBdlrf'bL'lR'B'LffR'l'U'Lu'd'lD'b'uFUD'uFDbF'FR'dl'fFbb'b'u'l'u'f'l'Fd'rd'u'D'db'blbu'"
           "UrfL",
    }[size]


@when("I click on Quit button")
def step_impl(context):
    """
        Find the input button on the html page which has name 'quit'
        and invoke .click()
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.CSS_SELECTOR, "button[name='quit']").click()


@when("I solve this cube")
def step_impl(context):
    """
        Find the html element 'sequence' using the id and input the solving sequence
        Then find the input button on the html page which has id 'apply'
        and invoke .click()
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.CSS_SELECTOR, "#sequence").send_keys(context.TEST_SOLVING_SEQUENCE)
    context.browser.find_element(By.CSS_SELECTOR, "#apply").click()


@step('I am forced to close "Congratulations!" notification')
def step_impl(context):
    """
        Check alert text and close it
    :type context: behave.runner.Context
    """
    alert = context.browser.switch_to.alert
    assert alert.text == "Congratulations!"
    alert.dismiss()


@then("Root page appears")
def step_impl(context):
    """
        If the quitting is successful we will be redirected to http://127.0.0.1:5000/
    :type context: behave.runner.Context
    """
    assert context.browser.current_url == f"http://127.0.0.1:5000/"


@given("Stability testing loop")
def step_impl(context):
    """
        Set up timer and use existing statements to simulate consecutive redirecting
        on the website until it runs out of time
    :type context: behave.runner.Context
    """
    context.execute_steps(f"Given I navigate to cube page (size={random.randint(2, 5)})")
    duration = datetime.timedelta(minutes=3)
    stability_testing_ends_at = datetime.datetime.now() + duration
    while datetime.datetime.now() < stability_testing_ends_at:
        context.execute_steps("""
        When I click on Quit button
        Then Root page appears
        """)
        size = random.randint(2, 5)
        context.execute_steps(f"""
        When I choose size {size}
        And I enter seed "{context.TEST_SEED}"
        And I click on Start button
        Then Cube with size {size} is generated
        """)
