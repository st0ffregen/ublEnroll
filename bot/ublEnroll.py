#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from datetime import timedelta, date, datetime
import os
from dotenv import load_dotenv
import logging

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

    logger.info(response.json())


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

    token = login(readerNumber, password, logger)
    bookSeat(readerNumber, begin, end, bib, seatingArea, fitting, days, token, logger)


if __name__ == '__main__':
    main()
