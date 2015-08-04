import os
import sys
import re

import requests
from requests.packages.urllib3 import disable_warnings
from bs4 import BeautifulSoup
import django
from django.core.exceptions import ObjectDoesNotExist


from myLogger import logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PropertyScrapers.settings")
django.setup()

from UCP import models


headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
}


def fetch_max_property_id_scraped():
    logger.info('Checking the last property scraped...')
    try:
        max_property_id = models.NTypeUnclaimedProperty.objects.latest('property_id').property_id
    except ObjectDoesNotExist:
        logger.info('\tNo Data Exists. Setting Default to 1780000')
        max_property_id = 32604000
    return max_property_id


def strip_spaces(s):
    s = s.strip()
    s = s.replace('\r', ' ').replace('\n', ' ').strip()
    s = ' '.join(s.split())
    return s.strip()


def extract_cash_amount(cash):
    cashamt = ''
    for c in cash:
        if c.isdigit() or c == '.':
            cashamt += c
    cashamt = round(float(cashamt), 2)
    return cashamt


def scrape_single_property(property_id):
    url = 'https://ucpi.sco.ca.gov/ucp/NoticeDetails.aspx?propertyRecID=%s' % property_id
    r = requests.get(url, headers=headers)
    if len(r.history) > 0:
        if r.history[0].status_code == 302:
            return -1
    soup = BeautifulSoup(r.content, 'html5lib')

    prop = models.NTypeUnclaimedProperty()
    prop.property_id = property_id
    prop.notification_date = soup.find('em').text.rstrip('*').strip()
    prop.business_contact_information = soup.find('td', id='HolderNameData').text.strip()
    prop.type_of_property = strip_spaces(soup.find('td', id='PropertyTypeData').text.strip())
    prop.cash_reported = strip_spaces(soup.find('td', id='AmountData').text.strip())
    prop.shares_reported = strip_spaces(soup.find('td', id='SharesData').text.strip())
    prop.name_security_reported = strip_spaces(soup.find('tr', id='SecurityDescriptionRow').find_all('td')[1].text.strip())
    prop.date_reported = strip_spaces(soup.find('td', id='DateReportedData').text.strip())
    prop.date_last_contact = strip_spaces(soup.find('td', id='DateOfLastContactData').text.strip())
    prop.owners_name = strip_spaces(soup.find('td', id='OwnersNameData').text.strip())
    prop.owners_address = strip_spaces(soup.find('td', id='ReportedAddressData').text.strip())
    prop.save()
    return 1


def main():
    try:
        logger.info('Starting Scraper...')
        max_property_id = fetch_max_property_id_scraped()
        property_id = max_property_id
        not_found_count = 0
        while True:
            property_id += 1
            logger.info('Fetching Property %s' % property_id)
            res = scrape_single_property(property_id)
            if res == -1:
                logger.info("\tDoesnt Exist")
                not_found_count += 1
            else:
                not_found_count = 0
            if not_found_count > 5000:
                logger.info("That's all folks!")
                break

    except:
        logger.exception(sys.exc_info())
    finally:
        logger.info('Done!')


if __name__ == '__main__':
    disable_warnings()
    main()
    # scrape_single_property('1780328')
    # scrape_single_property('979650461')
    # scrape_single_property('979650462')
