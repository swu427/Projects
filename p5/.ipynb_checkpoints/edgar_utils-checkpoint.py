import re
import netaddr
from bisect import bisect
import pandas as pd 


ips = pd.read_csv("ip2location.csv")
def lookup_region(ipaddr):
    ip_reformatted = re.sub(r"[A-Za-z+]", r"0", ipaddr)
    ip_number = int(netaddr.IPAddress(ip_reformatted))
    idx = bisect(ips["low"], ip_number) 
    return ips.iloc[idx-1]["region"]



class Filing:
    def __init__(self, html):
        dates = re.findall(r"((19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]))", html)
        self.dates = []
        for date in dates:
            self.dates.append(date[0])
        self.sic = None
        sic_digits = re.findall(r"SIC=(\d+)", html)

        for digits in sic_digits:
            if sic_digits:
                self.sic = int(sic_digits[0])
            else:
                self.sic = None  
        self.addresses = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html):
                lines.append(line.strip())
            empty_string =  "\n".join(lines)
            if empty_string != '':
                self.addresses.append("\n".join(lines))
            

    def state(self):
        for addr in self.addresses:
            match = re.search(r'\b[A-Z]{2}\s\d{5}\b', addr)
            if match:
                state_abbr = match.group().split()[0]
                return state_abbr