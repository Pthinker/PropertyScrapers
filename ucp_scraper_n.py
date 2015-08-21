import os
import sys
import math
import random
import time
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
        logger.info('No Data Exists. Setting Default to 32640487')
        max_property_id = 32640487
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
    time.sleep(random.randint(0, 3))
    url = 'https://ucpi.sco.ca.gov/ucp/NoticeDetails.aspx?propertyRecID=%s' % property_id
    r = requests.get(url, headers=headers)
    if len(r.history) > 0:
        if r.history[0].status_code == 302:
            return -1
    soup = BeautifulSoup(r.content, 'html5lib')

    prop = models.NTypeUnclaimedProperty()
    prop.property_id = property_id
    notification_date = soup.find('em').text.rstrip('*').strip()

    if notification_date == "as soon as possible":
        return 0

    prop.notification_date = notification_date
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

def is_running():
    if len(os.popen("ps -aef | grep -i 'ucp_scraper_n.py' | grep -v 'grep' | awk '{ print $3 }'").read().strip().split('\n')) > 1:
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

            try:
                res = scrape_single_property(property_id)
            except requests.ConnectionError:
                property_id -= 1
                logger.error("Connection error, sleep 10 minutes...")
                time.sleep(600)
                continue

            if res == -1:
                logger.info("Doesnt Exist")

                if int(math.fabs(last_fail_id-property_id)) == 1:
                    not_found_count += 1
                else:
                    not_found_count = 1
                last_fail_id = property_id

            if not_found_count > 50000:
                logger.info("That's all folks!")
                break
    except:
        logger.exception(sys.exc_info())
    finally:
        logger.info('Done!')


if __name__ == '__main__':
    disable_warnings()
    main()

