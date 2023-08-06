# Vaccine Notifier with Crontab
It takes input as music/song file path and other filter option for vaccine slot booking (given in usage section), Notifies you when vaccine slots are open for booking by sending desktop notification with song/music playing. 

## Installation
```pip install vaccine-notifier```

## Usage

```
usage: trigger.py [-h] [-p PINCODES] [-d DATES] [-v VACCINE] [-l LOG] music

positional arguments:
  music                 Path of Music or Song file. Play when vaccination
                        center detected

optional arguments:
  -h, --help            show this help message and exit
  -p PINCODES, --pincodes PINCODES
                        Single Pincode OR Comma Sprated Pincodes if multiple
  -d DATES, --dates DATES
                        Single Date OR Comma Seprated dates if multiple (In
                        dd-mm-yyyy)
  -v VACCINE, --vaccine VACCINE
                        Vaccine Names, Comma Seprated if multiple FROM
                        (covishild, covaxin, sputnik)
  -l LOG, --log LOG     Log File to Store Logs (Default siren_log.log file in
                        current directory
```

## License

© 2020 Parth Panchal

This repository is licensed under the MIT license. See LICENSE for details.