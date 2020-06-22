#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from datetime import timedelta, date, datetime
import sys



def login(cardnumber, password):
        dataLogin = {'readernumber':cardnumber,'password':password}
        login = requests.post('https://seats.ub.uni-leipzig.de/api/booking/login', data = dataLogin)
        token = login.json()['token']

        if(token == "null" and "Achtung, zuviele Nutzer sind gerade angemeldet." in login.json()['msg']):
                print("two many people on site")
                print(login.text)
                return 1
        elif(token == "null"):
                print("something went wrong, token null")
                print(login.text)
                return 1
        else:
                return token
      
def main():

        #processing cli arguments
        readernr = sys.argv[1]
        passwd = sys.argv[2]
        begin = sys.argv[3]
        end = sys.argv[4]
        bib = sys.argv[5]
        seatingArea = sys.argv[6]
        seatingAreaFallback  = sys.argv[7]
        days = sys.argv[8]

        print("---")
        print("starting")
        print(datetime.now())
        token = login(readernr, passwd)
        
        if(token != 1):
                return bookSeat(readernr, begin,end,bib,seatingArea,seatingAreaFallback, days, token, False)
        else:
                print("terminating")
                print(datetime.now())
                return 1

def bookSeat(cardnumber, begin, end, bib, seatingArea, seatingAreaFallback, days, token, fallback):
        
        print("sending query")

        dataSeat = {'institution':bib,
                'area':seatingArea,
                'from_date':str(date.today() + timedelta(days=int(days))),
                'from_time':begin,
                'until_time':end,
                'readernumber':cardnumber,
                'token':token
                }
        
        booking = requests.post('https://seats.ub.uni-leipzig.de/api/booking/booking',data = dataSeat)
       
        if(booking.json()['message'] != "outofreach" and booking.json()['bookingCode'] != ""):
                print("booking sucessfully")
                print("terminating")
                print(datetime.now())
                return 0
        elif(booking.json()['message'] == "outofreach"):
                print(booking.text)
                print("time or date is not valid")
                print("terminating")
                print(datetime.now())
                return 1
        elif(booking.json()['bookingCode'] == "" and fallback == False):
                print("all seats occupied")
                print("try second seating area")
                return bookSeat(cardnumber, begin, end, bib, seatingAreaFallback, seatingAreaFallback, days, token, True)
        else:
                print("booking not sucessfull")
                print("terminating")
                print(datetime.now())
                return 1
        

main()
