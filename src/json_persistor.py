import json
import csv
import datetime
from src.models.packet import Packet
from src.models.type import Type
from src.db_utils import db_interact
from datetime import datetime

csv_dir = '../data/mac-vendors.csv'


def get_oui(input_mac):
    input_mac = input_mac[:8]
    input_mac = input_mac.replace(':', '')
    return input_mac.upper()


def get_vendor(input_mac):
    reader = csv.reader(open(csv_dir), delimiter=',', quotechar='|')
    device_oui = get_oui(input_mac)
    for row in reader:
        if device_oui == row[0]:
            return row[1]


def parse_and_save(received_json):
    try:
        obj = json.loads(received_json)
    except ValueError as e:
        print(str(e))
        return

    macs = obj["MAC"]
    decibs = obj["RSSI"]
    milis = obj["MILIS"]
    ssids = obj["STATION/SSID"]
    types = obj["TYPE"]
    channels = obj["CH"]

    type_c = Type('C')
    type_b = Type('B')
    type_r = Type('R')

    for i in range(len(macs)):
        db_interact.open_session()
        if types[i] == 'C':
            db_interact.persist(Packet(datetime.fromtimestamp(milis[i]), decibs[i], macs[i], channels[i], ssids[i], type_c))
        elif types[i] == 'B':
            db_interact.persist(Packet(datetime.fromtimestamp(milis[i]), decibs[i], macs[i], channels[i], ssids[i], type_b))
        else:
            db_interact.persist(Packet(datetime.fromtimestamp(milis[i]), decibs[i], macs[i], channels[i], ssids[i], type_r))
        db_interact.close_session()
        print(milis[i], decibs[i], macs[i], channels[i], ssids[i], types[i])
        print(get_vendor(macs[i]))

