import re
from data.makes import MAKES


yearRe = re.compile(r'(\d{4}) \(')


class SaleVehicle:
    """ Class to represent a vehicle on sale. """

    def __init__(self, search_criteria, soup=None):
        """Inits a SaleVehicle with specific SearchCriteria attributes, and more if present in BeautifulSoup object.

        :param search_criteria: SearchCriteria object
        :param soup: BeautifulSoup object, representing input autotrader.com HTML doc
        """

        self.make = search_criteria.make
        self.model = search_criteria.model
        self.variant = search_criteria.variant
        self.gearbox = search_criteria.gearbox
        self.fuel = search_criteria.fuel
        self.body = search_criteria.body
        self.doors = search_criteria.doors
        self.drivetrain = search_criteria.drivetrain
        self.year = None
        self.cc = None
        self.mileage = None
        self.owners = None
        self.power = None
        self.price = None

        if soup is not None:
            for li in soup.select('section.product-card-details li'):
                txt = li.get_text()
                if txt.endswith(' miles'):
                    self.mileage = int(txt[0:-6].replace(',', ''))
                elif txt.endswith(' owners'):
                    self.owners = int(txt[0:-7].replace(',', ''))
                elif txt.endswith('BHP'):
                    self.power = int(txt[0:-3].replace(',', ''))
                elif txt.endswith('PS'):
                    self.power = int(txt[0:-2].replace(',', ''))
                elif txt.endswith(' owner'):
                    self.owners = 1
                elif txt == 'Manual':
                    self.gearbox = 'Manual'
                elif txt == 'Automatic':
                    self.gearbox = 'Automatic'
                elif txt == 'Camper':
                    self.body = 'Camper'
                elif txt == 'Convertible':
                    self.body = 'Convertible'
                elif txt == 'Coupe':
                    self.body = 'Coupe'
                elif txt == 'Estate':
                    self.body = 'Estate'
                elif txt == 'Hatchback':
                    self.body = 'Hatchback'
                elif txt == 'MPV':
                    self.body = 'MPV'
                elif txt == 'Panel Van':
                    self.body = 'Panel Van'
                elif txt == 'Pickup':
                    self.body = 'Pickup'
                elif txt == 'SUV':
                    self.body = 'SUV'
                elif txt == 'Saloon':
                    self.body = 'Saloon'
                elif txt == 'Petrol':
                    self.fuel = 'Petrol'
                elif txt == 'Diesel':
                    self.fuel = 'Diesel'
                elif txt == 'Bi Fuel':
                    self.fuel = 'Bi Fuel'
                elif txt == 'Electric':
                    self.fuel = 'Electric'
                elif txt == 'Hybrid-Diesel/Electric':
                    self.fuel = 'Hybrid-Diesel/Electric'
                elif txt == 'Hybrid – Diesel/Electric Plug-in':
                    self.fuel = 'Hybrid – Diesel/Electric Plug-in'
                elif txt == 'Hybrid – Petrol/Electric':
                    self.fuel = 'Hybrid – Petrol/Electric'
                elif txt == 'Hybrid – Petrol/Electric Plug-in':
                    self.fuel = 'Hybrid – Petrol/Electric Plug-in'
                elif txt.endswith('L'):
                    self.cc = int(float(txt[0:-1]) * 1000)
                mo = yearRe.match(txt)
                if mo:
                    self.year = int(mo.group(1))

            txt = soup.select('section.product-card-details h3')
            for m in MAKES:
                if m in str(txt):
                    self.make = m

            txt = soup.select('section.product-card-pricing div div span')[0].get_text()
            self.price = int(txt[1:].replace(',', ''))

    def __str__(self):
        """ Formats SaleVehicle object attributes into string.

        :return: Formatted string of SaleVehicle attributes
        :rtype: str
        """

        string = f""
        if self.year:
            string += f"{self.year}"
        if self.make:
            string += f" {self.make}"
        if self.model:
            string += f" {self.model}"
        if self.variant:
            string += f" {self.variant}"
        if self.mileage:
            string += f", {self.mileage} miles, "
        if self.owners:
            string += f"{self.owners} owners, "
        if self.price:
            string += f"£{self.price}"
        if self.gearbox:
            string += f", {self.gearbox} gearbox"
        if self.cc:
            string += f", {self.cc}cc"
        if self.fuel:
            string += f", {self.fuel}"
        if self.body:
            string += f", {self.body}"
        if self.drivetrain:
            string += f", {self.drivetrain}"
        if self.doors:
            string += f", {self.doors} doors"
        if self.power:
            string += f", {self.power}BHP"

        return f'{string}'

