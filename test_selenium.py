import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


# page-model section (this should be in a separate file then import here, but for illustration, I put here for easier checking)
class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def fill_form_by_id(self, form_element_id, value):
        elem = self.driver.find_element_by_id(form_element_id)
        elem.send_keys(value)
        return elem

    def navigate(self):
        self.driver.get(self.url)

    def click_button(self, method, button):
        elem = self.driver.find_element(method, button)
        elem.click()

    def select_option(self, method, selector, option):
        elem = self.driver.find_element(method, selector)
        elem.click()
        Select(elem).select_by_value(option)

    def get_current_url(self):
        return self.driver.current_url


class FormPage(BasePage):
    url = "https://fs28.formsite.com/ecnvietnam/form1/index.html"

    def setPassword(self, password):
        self.fill_form_by_id("Password", password)

    def submit(self):
        self.click_button(By.CLASS_NAME, 'submit_button')

    def setName(self, first, last):
        self.fill_form_by_id("RESULT_TextField-1", first)
        self.fill_form_by_id("RESULT_TextField-2", last)

    def setAddress(self, address_1, address_2):
        self.fill_form_by_id("RESULT_TextField-3", address_1)
        self.fill_form_by_id("RESULT_TextField-4", address_2)

    def setCity(self, city):
        self.fill_form_by_id("RESULT_TextField-5", city)

    def setZip(self, zip_code):
        self.fill_form_by_id("RESULT_TextField-7", zip_code)

    def setPhone(self, phone):
        return self.fill_form_by_id("RESULT_TextField-8", phone)

    def setEmail(self, email):
        return self.fill_form_by_id("RESULT_TextField-9", email)

    def selectState(self, state):
        self.select_option(By.ID, "RESULT_RadioButton-6", state)

    def setYear(self, year):
        self.click_button(By.CLASS_NAME, "popup_button")
        self.select_option(By.CLASS_NAME, "ui-datepicker-year", year)

    def setDay(self, day):
        self.click_button(
            By.XPATH, '//*[@class="ui-state-default" and text() = "%s"]' % day)

    def setDate(self, date):
        return self.fill_form_by_id("RESULT_TextField-10", date)

    def get_required_fields(self):
        elems = self.driver.find_elements_by_css_selector('.q.required')
        return elems

    def get_invalid_message(self, obj):
        return obj.find_element_by_class_name('invalid_message')


# test case section
class FormTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        page = FormPage(self.browser)
        page.navigate()
        page.setPassword('secret')
        page.submit()

    def test_submit_all_data(self):
        page = FormPage(self.browser)
        page.setName('Hung', 'Tran')
        page.setAddress('test 1', 'test 2')
        page.setCity('HCM')
        page.setZip('123456')
        page.setPhone('3567543432453')
        page.setEmail('trannguyenhung011086@gmail.com')
        page.selectState('Radio-1')
        page.setYear('1986')
        page.setDay('16')
        page.submit()
        assert 'showSuccessPage' in page.get_current_url()

    def test_submit_empty_data(self):
        page = FormPage(self.browser)
        page.submit()
        for elem in page.get_required_fields():
            elem = page.get_invalid_message(elem)
            assert 'Response required' in elem.text

    def test_wrong_phone_format(self):
        page = FormPage(self.browser)
        phone = page.setPhone('asd%@#$@#')
        page.submit()
        phone = page.setPhone('asd%@#$@#')  # call again due to stale status
        elem = page.get_invalid_message(phone.find_element_by_xpath('..'))
        assert 'Invalid phone number' in elem.text

    def test_wrong_email_format(self):
        page = FormPage(self.browser)
        email = page.setEmail('asd%@af')
        page.submit()
        email = page.setEmail('asd%@af')  # call again due to stale status
        elem = page.get_invalid_message(email.find_element_by_xpath('..'))
        assert 'Invalid email address' in elem.text

    def test_wrong_date_format(self):
        page = FormPage(self.browser)
        date = page.setDate('3423423')
        page.submit()
        date = page.setDate('3423423')  # call again due to stale status
        elem = page.get_invalid_message(date.find_element_by_xpath('..'))
        assert 'Invalid date' in elem.text

    def tearDown(self):
        self.browser.close()


if __name__ == "__main__":
    unittest.main()
