#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from datetime import timedelta, date, datetime
import sys

readernr = sys.argv[1]
passwd = sys.argv[2]
begin = sys.argv[3]
end = sys.argv[4]
bib = sys.argv[5]
seatingArea = sys.argv[6]
def main():
        print("---")
        print("starting")
        print(datetime.now())
        dataLogin = {'readernumber':readernr,'password':passwd}
        login = requests.post('https://seats.ub.uni-leipzig.de/api/booking/login', data = dataLogin)
        token = login.json()['token']
        #print(login.text)
        if(token == None and "Achtung, zuviele Nutzer sind gerade angemeldet." in login.json()['msg']):
                print("two many people on site")
                
        elif(token == None):
                print("something went wrong, token null")
                
        else:
                dataSeat = {'institution':bib,
                                        'area':seatingArea,
                                        'from_date':str(date.today() + timedelta(days=2)),
                                        'from_time':begin,
                                        'until_time':end,
                                        'readernumber':readernr,
                                        'token':token}
                #print(dataSeat)
                booking = requests.post('https://seats.ub.uni-leipzig.de/api/booking/booking',data = dataSeat)
                #print(booking.json())
                if(booking.json()['message'] != "outofreach" and booking.json()['bookingCode'] != ""):
                        print("booking sucessfully")
                elif(booking.json()['bookingCode'] == ""):
                        print("all seats occupied")
                else:
                        print("booking not sucessfull")
        print("terminating")
        print(datetime.now())

main()