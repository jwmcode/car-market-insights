from urllib.parse import urlencode
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from model.sale_vehicle import SaleVehicle

# needed for headless scraping, chrome detects and blocks otherwise
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'


class Scraper:
    """ Class to represent web scraper. """

    def __init__(self, driver='chrome', headless=False):
        """ Constructor for Scraper.

        :param driver: str, driver type for browser
        :param headless: bool, whether webdriver will launch headless browser or not
        """

        self._driver = None
        self._driver_type = driver
        self._headless = headless

    def __del__(self):
        """ Destructor, quitting web driver. """

        if self._driver:
            self._driver.quit()

    def _make_driver(self):
        """ Launches driver with configs. """

        if self._driver is None:
            if self._driver_type == 'chrome':
                options = webdriver.ChromeOptions()
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--incognito')
                if self._headless:
                    options.add_argument('--headless')
                    options.add_argument(f'user-agent={USER_AGENT}')
                self._driver = webdriver.Chrome(options=options)
                self._driver.implicitly_wait(5)

    def accept_cookies(self):
        """ Switches to iframe to accept cookies popup message.

        :except NoSuchElementException: if no cookies popup found
        """

        try:
            self._driver.switch_to_frame("sp_message_iframe_576092")
            element = self._driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[3]/div[2]/button[2]')
            element.click()

        except NoSuchElementException:
            print('no accept cookies element')

        self._driver.switch_to_default_content()

    def get_sale_vehicles(self, search_criteria, limit, postcode='NR22PP'):
        """ Retrieves sale vehicles from autotrader.com.

        Builds URL with search criteria and postcode, creates web driver and accepts cookies on web page, creates
        SaleVehicles from search results, stops searching when limit has been reached, last page of
        search results reached or no valid elements found.

        :param search_criteria: SearchCriteria object
        :param limit: int, the maximum number of SaleVehicles to be returned
        :param postcode: string, to be encoded in URL
        :return: object, list of SaleVehicles retrieved
        :except ElementClickInterceptedException, NoSuchElementException: fired when element cannot be found or element overlapping desired element (meaning last page of results)

        """

        # sort by descending advert posted date to bypass any weird autotrader relevance sorting
        # write offs not included as irrelevant
        url = 'https://www.autotrader.co.uk/car-search?sort=datedesc&exclude-writeoff-categories=on'
        if search_criteria.make is not None:
            url = url + '&' + urlencode({'make': search_criteria.make.upper()})
        if search_criteria.model is not None:
            url = url + '&' + urlencode({'model': search_criteria.model.upper()})
        if search_criteria.variant is not None:
            url = url + '&' + urlencode({'aggregatedTrim': search_criteria.variant})
        if search_criteria.min_year is not None:
            url = url + '&' + urlencode({'year-from': search_criteria.min_year})
        if search_criteria.max_year is not None:
            url = url + '&' + urlencode({'year-to': search_criteria.max_year})
        if search_criteria.gearbox is not None:
            url = url + '&' + urlencode({'transmission': search_criteria.gearbox})
        if search_criteria.fuel is not None:
            url = url + '&' + urlencode({'fuel-type': search_criteria.fuel})
        if search_criteria.doors is not None:
            url = url + '&' + urlencode({'quantity-of-doors': search_criteria.doors})
        if search_criteria.drivetrain is not None:
            url = url + '&' + urlencode({'drivetrain': search_criteria.drivetrain})
        if search_criteria.body is not None:
            url = url + '&' + urlencode({'body': search_criteria.body})
        url = url + '&' + urlencode({'postcode': postcode})

        self._make_driver()
        self._driver.get(url)
        self.accept_cookies()

        sale_vehicles = []
        while True:
            elements = self._driver.find_elements_by_css_selector(
                'li.search-page__result')
            for element in elements:
                html = element.get_attribute('innerHTML')
                soup = BeautifulSoup(html, 'lxml').select(
                    'div.product-card-content__car-info')[0]
                sale_vehicles.append(SaleVehicle(search_criteria, soup=soup))

                if len(sale_vehicles) == limit:
                    return sale_vehicles

            try:
                element = self._driver.find_element_by_css_selector(
                    'a.paginationMini--right__active')
                element.click()
                time.sleep(2)
            except (ElementClickInterceptedException, NoSuchElementException):
                # Last page has been reached
                break

        return sale_vehicles

