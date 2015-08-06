import os
import sys
import math
import random
import time
import requests
from requests.packages.urllib3 import disable_warnings
from bs4 import BeautifulSoup
import django
from django.db import IntegrityError
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
        max_property_id = models.UnclaimedProperty.objects.latest('property_id').property_id
    except ObjectDoesNotExist:
        logger.info('\tNo Data Exists. Setting Default to 979940854')
        max_property_id = 979940854
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
    time.sleep(random.randint(1, 6))
    url = 'https://ucpi.sco.ca.gov/ucp/PropertyDetails.aspx?propertyID=%s' % property_id
    r = requests.get(url, headers=headers)
    if len(r.history) > 0:
        if r.history[0].status_code == 302:
            return -1
    soup = BeautifulSoup(r.content, 'html5lib')

    prop = models.UnclaimedProperty()
    prop.property_id = property_id
    prop.date_added_to_site = soup.find('table', id='tbl_HeaderInformation').tbody.tr.find_all('td')[0].span.text.strip()
    prop.source = soup.find('table', id='tbl_HeaderInformation').tbody.tr.find_all('td')[1].span.text.strip()
    prop.owners_name = strip_spaces(soup.find('td', id='OwnersNameData').text.strip())
    prop.owners_address = strip_spaces(soup.find('td', id='ReportedAddressData').text.strip())
    prop.type_of_property = strip_spaces(soup.find('td', id='PropertyTypeData').text.strip())
    try:
        prop.cash_reported_text = strip_spaces(soup.find('td', id='ctl00_ContentPlaceHolder1_CashReportData').text.strip())
    except AttributeError:
        return 0
    prop.cash_reported = extract_cash_amount(prop.cash_reported_text)
    if prop.cash_reported < 8000:
        return 0
    prop.reported_by = strip_spaces(soup.find('td', id='ReportedByData').text.strip())
    prop.save()
    return 1

def is_running():
    if len(os.popen("ps -aef | grep -i 'ucp_scraper.py' | grep -v 'grep' | awk '{ print $3 }'").read().strip().split('\n')) > 1:
        return True
    else:
        return False

def main():
    if is_running():
        logger.info('Still running, exit!')
        sys.exit(0)

    last_fail_id = -1
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
                logger.info("Doesnt Exist")

                if int(math.fabs(last_fail_id-property_id)) == 1:
                    not_found_count += 1
                else:
                    not_found_count = 1
                last_fail_id = property_id

            if not_found_count > 500:
                logger.info("That's all folks!")
                break
    except:
        logger.exception(sys.exc_info())
    finally:
        logger.info('Done!')


if __name__ == '__main__':
    disable_warnings()
    main()

