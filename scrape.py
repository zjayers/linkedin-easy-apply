from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

base_url = "https://linkedin.com/jobs"
driver = webdriver.Chrome()
driver.get(base_url)

driver.set_page_load_timeout(1)


class element_to_be_clickable(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, ignored):
        if self.element.is_displayed() and self.element.is_enabled():
            return self.element
        else:
            return False


# Wait for element by class Name
def wait_for_class_name(class_name):
    print('Waiting on class ' + class_name)
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )
    return element


def click(element):
    WebDriverWait(driver, 5).until(element_to_be_clickable(element)).click()


# Scrape the page and apply
def scrape():
    try:

        input('Ready?: ')

        # Get Postings From Page
        postings = driver.find_elements_by_css_selector('.jobs-search-results__list-item')

        # Loop through the postings
        for posting in postings:
            click(posting)
            try:
                # Get the posting button and click it
                click(wait_for_class_name('jobs-apply-button'))

                wait_for_class_name('artdeco-modal')
                applying = True
                counter = 0
                while applying:
                    counter += 1
                    button = wait_for_class_name('artdeco-button--primary')
                    attribute = button.get_attribute('data-control-name')
                    click(button)

                    if attribute == 'submit_unify':
                        print('Submitting Application')
                        applying = False

                    elif counter >= 10:
                        print('Can not submit - Discarding application')
                        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        discard_container = wait_for_class_name('artdeco-modal__actionbar--confirm-dialog')
                        discard_button = discard_container.find_elements_by_css_selector('.artdeco-modal__confirm'
                                                                                         '-dialog-btn')[1]
                        click(discard_button)
                        applying = False

            except TimeoutException as e:
                print("No easy apply button found...moving to next item!!!")

    except Exception as error:
        print(error)

    finally:
        restart = input('Restart?: ')
        if restart == 'y':
            scrape()
        else:
            driver.quit()


scrape()
