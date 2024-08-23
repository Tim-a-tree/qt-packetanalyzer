import scapy.all as scapy
import re
from lxml import etree
from typing import Callable

from src.functions import find_function, xml_to_list
from src.models import Result, ListResult
from src.shared_variable import list_result




def get_result(function_name, pcap_file):
    # gets the data from the xml file
    xml_file = "src/data.xml"

    with open(xml_file) as f:
        xml_data = f.read()

    root = etree.fromstring(xml_data)
    xml_list = xml_to_list(root)

    # gets the values from the data for the function
    values = get_values(function_name, xml_list)
    print_in_format(values, 0, pcap_file)


'''
EXPLANATION NEEDS TO BE MODIFIED
Function: Checks the pcap, for designated KEYWORDS, whether it exists in pcap file

Input:
    keywords : List, keywords that identifies the packet sent/received in a correct format
    _pkt : Integer, starting packet number

Output:
    Print: PASS/POSSIBLE/FAIL status, for PASS/POSSIBLE case it shows the packet number for users' further examination
    Returns :
        PASS/POSSIBLE/FAIL : the packet number
'''
def _check_procedure(keywords: Callable[[str], bool], _pkt : int, pcap_file : str, pkt_req : bool) -> Result:
    # Reading the pcap file
    try:
        scapy_cap = scapy.rdpcap(pcap_file)
    except Exception as e:
        list_result.append("Unsupported File Format")
        return

    # print(f"{_pkt}") # DEBUG

    flag = False
    for pkt_num, packet in enumerate(scapy_cap, start=1):
        # if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP):
        if pkt_num <= _pkt:
            continue
        if flag == False:
            exists = [False for _ in range(len(keywords))]


        if scapy.Raw in packet:
            raw_data = packet[scapy.Raw].load

            # CHECKING KEYWORDS
            for i in range(len(keywords)):
                if re.search(keywords[i], str(raw_data)) and pkt_num > _pkt:
                    exists[i] = True

            if all(exists):
                print(f"PASS\t\t{pkt_num}")
                result = Result("PASS", pkt_num, False, str(raw_data))
                if pkt_req == True:
                    result.req_type = True
                list_result.append(result) # GLOBAL VARIABLE
                return result
            elif any(exists):
                if flag:
                    if set_pkt_size != len(packet):
                        flag = False
                        if any(exists) and starting_pkt > _pkt and pkt_req == False:
                            print(f"POSSIBLE\t\t{starting_pkt}")

                            result = Result("POSSIBLE", starting_pkt, False, str(raw_data))

                            list_result.append(result)  # GLOBAL VARIABLE
                            return result
                else:
                    flag = True
                    set_pkt_size = len(packet)
                    starting_pkt = pkt_num

    print(f"FAIL")
    result = Result("FAIL", _pkt, pkt_req, "")
    if pkt_req == True:
        result.req_type = True
    list_result.append(result)  # GLOBAL VARIABLE
    return result








'''
check_all()
Function : checking pcap file, checks all the cases those consist in 'src/data.xml' file.

Input : None:   

Output : Overall pass/fail of each cases,
    It shows in a format of
        Passed Cases: {cases}
        Failed Cases: {cases}

'''
def check_all(pcap_file):
    xml_file = "src/data.xml"
    
    with open(xml_file) as f:
        xml_data = f.read()

    root = etree.fromstring(xml_data)
    xml_list = xml_to_list(root)

    function_list = find_function(root, 'is_button')

    function_list = list(map(lambda function: function[0], function_list))

    for function in function_list:
        print(function)
        list_result.append(function)
        data = xml_list

        values = get_values(function, data)

        print_in_format(values, 0, pcap_file)


'''
check_designated()
Function : examine specific cases

Input :
    values : List - the steps and keywords needs for analzying the pcap
Output :
    Please check print_in_format() function


'''
def check_designated(values):
    print_in_format(values, 0)









'''
get_values()
Function : gets the steps/keywords for entered case

Input :
    input_str - name of the function(case) : string
    data(from the 'src/data.xml') : List

Output :
    value - Each step with keywords : Multi dimensional List
'''

def get_values(input_str, keywords):
    keys = input_str.split('.')
    # print(keys)
    value = keywords
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list):
            value = next((item[key] for item in value if key in item), None)
        else:
            return None
    return value






'''
print_in_format()
Function : Prints the PASS/POSSIBLE/FAIL status of each step

Input:
    data : Keywords that indicates that it followed steps - List
    _pkt : starting packet number - int
    pkt_req : identifies Request/Reponse procedure - boolean

Output:
    Prints : {PASS/POSSIBLE/FAIL}/{packet number if PASS/POSSIBLE}
    Returns: if PASS/POSSIBLE - packet number that program decided to give PASS/POSSIBLE
                FAIL - _pkt since it could not find any
'''
def print_in_format(data, _pkt, pcap_file, pkt_req : bool = False) -> int:
    if isinstance(data, dict):
        for key, value in data.items():
            print(key)
            if not (key == 'Request' or key == 'Response'):
                list_result.append(key)

            
            if key == 'Request':
                _pkt = print_in_format(value, _pkt, pcap_file, True)
            else:
                _pkt = print_in_format(value, _pkt, pcap_file, pkt_req)
    elif isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            for item in data:
                if item is not None:
                    _pkt = print_in_format(item, _pkt, pcap_file, pkt_req)
        else: # PASSES the keywords from here
            '''
            This is the place where you need to send the keywords to parsing function
            '''
            if data is not None or len(data) > 0:
                result = _check_procedure(data, _pkt, pcap_file, pkt_req)
                _pkt = result.packet_number
                # _pkt = _check_procedure(data, _pkt, pcap_file, pkt_req)
    else:
        print(f"at else{data}")

    return _pkt


'''
get_details()

Function: gets the detail of PASS/POSSIBLE/FAIL case 

Input :
    data : List - the keywords used for deciding PASS/POSSIBLE/FAIL
    pkt_num : int - the packet number, that program judged as an occurred point 

Output:
    Printing the full data of the packet with highlighted text for the matching keywords
    Summarization of missing keywords if there are any

'''
def get_details(self, data, pkt_num : int):
    pass


