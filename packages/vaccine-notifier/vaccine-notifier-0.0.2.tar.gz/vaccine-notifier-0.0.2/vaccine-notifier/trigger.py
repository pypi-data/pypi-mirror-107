#!/usr/bin/python
import requests
import os
import logging
import time
from argparse import ArgumentParser
from pydub import AudioSegment
from requests.exceptions import HTTPError
from pydub.playback import play
from datetime import datetime
from notifypy import Notify
import shelve

os.environ.setdefault('DISPLAY', ':0.0')

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-p', '--pincodes', help="Single Pincode OR Comma Sprated Pincodes if multiple")
    parser.add_argument('-d', '--dates', help="Single Date OR Comma Seprated dates if multiple (In dd-mm-yyyy)")
    parser.add_argument('-v','--vaccine', help="Vaccine Names, Comma Seprated if multiple \
                         FROM (covishild, covaxin, sputnik)")
    parser.add_argument('music', help="Path of Music or Song file. Play when vaccination center detected")
    parser.add_argument('-l', '--log', help="Log File to Store Logs (Default siren_log.log file in current directory")
    return parser.parse_args()

def api_call(pincode):
    current_date = datetime.today().strftime('%d-%m-%Y')
    base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    query_parms = "?pincode={0}&date={1}".format(pincode, current_date)
    api_url = base_url+query_parms
    header = {'User-Agent': 'My User Agent 1.0'}
    try:
        response = requests.get(api_url, headers=header)
    except HTTPError as e:
        logging.error("Exception Occured "+str(e))
    
    return response.json()

def check_available_slot(response_dict, selected_dates = [], 
                            selected_vaccine = []):
    is_available = False
    for center in response_dict.get("centers", []):
        for session in center.get("sessions", []):
            
            if  (((not selected_vaccine) or session["vaccine"].lower().startswith(tuple(selected_vaccine)) )  
                and ((not selected_dates) or session["date"] in selected_dates)
                and (session["min_age_limit"] == 18 and session["available_capacity"] > 0)) :
                if _check_and_update_cache(session, center):
                    is_available = True
                    alert_text = """
                                ***Alert***
                                    Vaccine = {0}
                                    Available capacity = {1}
                                    pincode = {2}
                                    Available date = {3}
                                    From {4} To {5}
                                    Address = {6}
                                    Fee type = {7}
                        """.format(session["vaccine"], session["available_capacity"],
                            center["pincode"], session["date"], center["from"], 
                            center["to"], center["address"], center["fee_type"])
                    send_notification(session["date"], center["address"], center["pincode"])
                    logging.info(alert_text)

    return is_available

def _check_and_update_cache(session, center):
    vdb = shelve.open("vaccinedb.db", writeback=True)
    key = str(center["center_id"])+","+session["session_id"]
    current_ts = int(time.time())
    
    try:
        if key in vdb:
            if vdb[key]["available_capacity"] <  session["available_capacity"]:
                vdb[key]["available_capacity"] =  session["available_capacity"]
                return True
            elif vdb[key]["timestamp"] - current_ts > 300:
                del vdb[key]
                return True
            else:
                return False
        else:
            vdb[key] = {"available_capacity": session["available_capacity"], "timestamp": current_ts}
            return True
    finally:
        vdb.close()
        

def send_notification(date, address, pincode):
    notification = Notify()
    notification.title = "Vaccine Alert-"+date+","+str(pincode)
    notification.message = address
    notification.send()

def play_siren(music_path):
    song = AudioSegment.from_mp3(music_path)
    play(song)
        
def main():
    args = get_arguments()
    
    log_file = args.log or 'siren_log.log'    
    
    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s'
                    )

    if args.pincodes:
        
        selected_dates_ls = []
        selected_vaccine_ls = []
        
        if args.dates:
            selected_dates = args.dates
            selected_dates_ls = selected_dates.split(",")
        
        if args.vaccine:
            selected_vaccine = args.vaccine
            selected_vaccine_ls = [x.lower() for x in selected_vaccine.split(",")]

        pincodes = args.pincodes
        count = 0
        for pincode in pincodes.split(","):
            resp = api_call(pincode)
            if check_available_slot(resp, selected_dates=selected_dates_ls, 
                            selected_vaccine=selected_vaccine_ls):
                count += 1
            
        if count>0:
            logging.info("Vaccination Center detected!")
            play_siren(args.music)
        else:
            logging.info("No vaccination Center Detected!")

    else:
        print("Pincode Not Entered!")

if __name__ == '__main__':
    main()