from datetime import datetime
import requests
import argparse
import json
import time
import os


class HandlerException(Exception):
    """Base Exception Catcher"""
    pass


class RateLimited(HandlerException):
    """Rate limited by the Ip-Api exception"""
    pass


class NoIPProvided(HandlerException):
    """No IP provided to lookup"""
    pass


class Nipher:
    def __init__(self):
        self.BASEURL = 'http://ip-api.com'  # https://ip-api.com/docs/api:json
        self.remain = 45
        self.remain_time = 60
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--ip", nargs='+', help="List of IPs that will be resolved.")
        self.parser.add_argument("--ipfile", help="File that contains the list of IPs that will be resolved.")
        self.parser.add_argument("--json", action="store_true", help="Saves the lookup to a .json file on the current directory.")
        self.parser.add_argument("-o", "--output", help="The path where to save the .json files.")
        self.parser.add_argument("-v", "--verbose", action="store_true", help="Force complete output in the terminal.")
        self.args = self.parser.parse_args()
        self.h = {'user-agent': 'ipapi.co/#ipapi-python-v1.0.4'}

    @staticmethod
    def banner():
        print("""
        \033[96m888b    888 d8b          888                       
        8888b   888 Y8P          888                       
        88888b  888              888                       
        888Y88b 888 888 88888b.  88888b.   .d88b.  888d888 
        888 Y88b888 888 888 "88b 888 "88b d8P  Y8b 888P"   
        888  Y88888 888 888  888 888  888 88888888 888     
        888   Y8888 888 888 d88P 888  888 Y8b.     888     
        888    Y888 888 88888P"  888  888  "Y8888  888     
                        888                                
                        888                                
                        888\033[0m
          
        \033[92m*--------------------------------------------------*
        |       IP lookup tool to avoid manual check       |
        |  avaible in:  https://github.com/Slyrack/Nipher  |
        |       created by Slyrack | Free to use :D        |
        *--------------------------------------------------*\033[0m                                                  
        """)

    # Method that makes the request to the API
    def get_request(self, ip):
        req = requests.get(f'{self.BASEURL}/json/{ip}?fields=66322431', headers=self.h)
        self.remain = int(req.headers["X-Rl"])  # Header that contains the remaining lookups
        self.remain_time = int(req.headers["X-Ttl"])  # Header that contains the time to receive the next 45 lookups
        return req.text

    def formatter(self, ip):
        # Creating the master json to output informations
        if self.remain == 0:
            print(f'        \033[93m\033[1m[!] Being rate limited by the API. Waiting for {self.remain_time} seconds!')
            time.sleep(self.remain_time + 1)  # Waiting the time remaining to receive the next 45 lookups
        op_json = {}  # Master json
        j = json.loads(self.get_request(ip))  # Making the request
        op_json[f"{ip}"] = j

        # Appending/creating the json if param "json" passed
        if self.args.json:
            p = f'{self.args.output}/{datetime.today().strftime("%Y-%m-%d")}.json' if self.args.output else \
                f'{os.getcwd()}/{datetime.today().strftime("%Y-%m-%d")}.json'  # Making the correct path to the json
            if not os.path.isfile(p):  # If not exists, make a new one
                with open(p, 'w') as f:
                    f.write(json.dumps(op_json, indent=4))
            else:  # If exists, append the result to the end
                with open(p) as f:
                    data = json.load(f)
                data.update(op_json)
                with open(p, 'w') as f:
                    f.write(json.dumps(data, indent=4))

        if j["status"] == "success":
            if self.args.verbose or not self.args.json:  # Complete output with param "verbose" or not param "json"
                print(
                    f"""
                            \033[94m*-------------------*
        \033[94m[i] \033[93mResolving \033[96m\033[1m{ip}...
        \033[95mIP Address                    \033[94m:    \033[92m{j["query"]}
        \033[95mISP                           \033[94m:    \033[92m{j["isp"]}
        \033[95mASN                           \033[94m:    \033[92m{j["as"] if j["as"] else j["asname"] if j["asname"] else None}
        \033[95mReverse DNS                   \033[94m:    \033[92m{j["reverse"] if j["reverse"] else None}
        \033[95mCity                          \033[94m:    \033[92m{j["city"]}
        \033[95mRegion                        \033[94m:    \033[92m{j["region"]} ({j["regionName"]})
        \033[95mCountry                       \033[94m:    \033[92m{j["countryCode"]} ({j["country"]})
        \033[95mCountry Currency              \033[94m:    \033[92m{j["currency"]}
        \033[95mTimezone UTC DST (seconds)    \033[94m:    \033[92m{j["offset"]}
        \033[95mTime Zone                     \033[94m:    \033[92m{j["timezone"]}
        \033[95mPostal Code                   \033[94m:    \033[92m{j["zip"] if j["zip"] else None}
        \033[95mLatitude                      \033[94m:    \033[92m{j["lat"] if j["lat"] else None}
        \033[95mLongitude                     \033[94m:    \033[92m{j["lon"] if j["lon"] else None}
        \033[95mMobile Connection             \033[94m:    \033[92m{j["mobile"]}
        \033[95mProxy, VPN or Tor             \033[94m:    \033[92m{j["proxy"]}
        \033[95mHosting/Data Center           \033[94m:    \033[92m{j["hosting"]}
        \033[95mGoogle Maps                   \033[94m:    \033[92mhttps://maps.google.com/?q={j["lat"]},{j["lon"]}
                            \033[94m*-------------------*\033[0m
                """)
            else:
                print(f'        \033[94m[i] \033[93mResolved \033[96m\033[1m{ip}!\033[0m')
        else:
            print(f'        \033[91m[!!!] Failed to resolve: \033[96m\033[1m{ip}! \033[91m- {j["message"]}\033[0m')

    def main(self):
        self.banner()
        if self.args.ipfile:  # Oppening file and creating the list of IPs
            with open(self.args.ipfile) as f:
                ips = f.readlines()
            ips = [x.strip() for x in ips]
        elif self.args.ip:  # Using the list passed
            ips = self.args.ip
        else:  # Throwing error
            raise NoIPProvided('\033[91mYou need to provide at least one IP to lookup.\033[0m')

        start = datetime.now()
        print(f"""
        \033[94m[i] \033[93mBeginning to look up \033[92m{len(ips)} \033[93mIPs...
        \033[94m[i] \033[93mStarting time: \033[92m{start.strftime("%H:%M")}\033[0m
              """)

        for ip in ips:  # Looping through the list of IPs
            self.formatter(ip)

        finish = datetime.now()
        print(f"""
        \033[94m[i] \033[92mFinished looking up \033[93m{len(ips)} \033[92mIPs.
        \033[94m[i] \033[92mEnd time: \033[93m{finish.strftime("%H:%M")} \033[92m| Elapsed time: \033[93m{int(divmod((finish - start).total_seconds(), 60)[0])} minutes ({int((finish - start).total_seconds())} seconds)\033[92m.\033[0m
              """)


if __name__ == '__main__':
    a = Nipher()
    a.main()
