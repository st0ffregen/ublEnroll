#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from datetime import timedelta, date, datetime
import os
from dotenv import load_dotenv
import logging
import sys

load_dotenv()


def login(readeNumber, password, logger):
    logger.info('login to book seat')
    payload = {'readernumber': readeNumber, 'password': password, 'logintype': '0'}
    response = requests.post('https://seats.ub.uni-leipzig.de/api/booking/login', data=payload)
    return response.json()['token']


def bookSeat(readerNumber, begin, end, bib, seatingArea, fitting, days, token, logger):
    logger.info('book seat')

    payload = {'institution': bib,
               'area': seatingArea,
               'fitting': fitting,
               'from_date': str(date.today() + timedelta(days=int(days))),
               'from_time': begin,
               'until_time': end,
               'tslot': '0',
               'preference': '0',
               'readernumber': readerNumber,
               'token': token}

    logger.info(payload)

    response = requests.post('https://seats.ub.uni-leipzig.de/booking-internal/booking/booking', data=payload)

    jsonResponse = response.json()

    logger.info(jsonResponse)

    return jsonResponse['workspaceId'], jsonResponse['bookingCode']


def stornoSeat(begin, end, readerNumber, stornoToken, bookingCode, logger):

    logger.info('storno seat with bookingCode ' + bookingCode)

    payload = {
               'from': begin,
               'until': end,
               'readernumber': readerNumber,
               'token': stornoToken,
        'bookingCode': bookingCode
    }

    logger.info(payload)

    response = requests.post('https://seats.ub.uni-leipzig.de/api/booking/storno', data=payload)

    jsonResponse = response.json()

    logger.info(jsonResponse)

    if jsonResponse['message'] != 'Ihre Buchung wurde gelöscht.':
        # token might be outdated
        return False

    return True


def loginToStorno(readeNumber, password, logger):
    logger.info('login to storno seat')
    payload = {'readernumber': readeNumber, 'password': password, 'logintype': '1'}
    response = requests.post('https://seats.ub.uni-leipzig.de/api/booking/login', data=payload)
    return response.json()['token']


def enforceSeatReservervation(enforceSeatsArray, enforceAttempts, readerNumber, password, begin, end, bib, seatingArea, fitting, days, logger):
    enforceSeatsArray = [seat.strip() for seat in enforceSeatsArray[1:-1].split(',')]
    logger.info('enforce seat reservation in seats set ' + ', '.join(enforceSeatsArray))
    stornoToken = None

    for i in range(0, int(enforceAttempts)):
        token = login(readerNumber, password, logger)
        seat, bookingCode = bookSeat(readerNumber, begin, end, bib, seatingArea, fitting, days, token, logger)
        if bookingCode == '':
            logger.info('something went wrong. exiting')
            sys.exit(1)

        if seat not in enforceSeatsArray and i < int(enforceAttempts) - 1:
            if stornoToken is None:
                stornoToken = loginToStorno(readerNumber, password, logger)
            isTokenValid = stornoSeat(begin, end, readerNumber, stornoToken, bookingCode, logger)
            if isTokenValid is False:
                stornoToken = loginToStorno(readerNumber, password, logger)
        else:
            break


def configureLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    file_handler = logging.FileHandler('logs/ublEnroll.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def main():
    logger = configureLogger()

    logger.info('start ubl enroll script')

    readerNumber = os.environ['readerNumber']
    password = os.environ['password']
    begin = os.environ['begin']
    end = os.environ['end']
    bib = os.environ['bib']
    seatingArea = os.environ['seatingArea']
    days = os.environ['days']
    fitting = os.environ['fitting']
    enforceSeatsArray = os.environ['enforceSeatsArray']
    enforceAttempts = os.environ['enforceAttempts']

    if enforceAttempts != '' and int(enforceAttempts) > 1 and enforceSeatsArray != '':
        enforceSeatReservervation(enforceSeatsArray, enforceAttempts, readerNumber, password, begin, end, bib,
                                  seatingArea, fitting, days, logger)
    else:
        token = login(readerNumber, password, logger)
        bookSeat(readerNumber, begin, end, bib, seatingArea, fitting, days, token, logger)


if __name__ == '__main__':
    main()
