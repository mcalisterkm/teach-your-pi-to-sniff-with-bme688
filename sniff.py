#!/usr/bin/python3
# Sniff air / ethanol
# Keith McAlister 6th May 2023 based on the PI3G Meat and Cheese code.

from bme68x import BME68X
import bme68xConstants as cst
import bsecConstants as bsec
from time import sleep
from pathlib import Path
import json

# The export from AI Studio is for BSE C2.4.0.0 snf the first four bytes of the .config file in decimal are 1974
# The .h and .c that studio exports with the config file also has a reference to bsec_config_selectivity[1974] = ...
# So it looks like BSEC can use multiple AI configs and reference them by this index.
# In the PI3G Python Wrapper we use only one config and this function chops off the 1974 header - strictly speaking is chops off the first 4 bytes in the slicer [4:].


# This is the config file output by AI_Studio
config_file = '2023_05_06_15_00_Air-Ethanol_HP-354_RDC-5-10.config'
config_path = str(Path(__file__).resolve().parent.joinpath(config_file))
def read_conf(path: str):
    with open(path, 'rb') as ai_conf:
    	conf = [int.from_bytes(bytes([b]), 'little') for b in ai_conf.read()]
    	conf = conf[4:]
    return conf

def main():
    # Open the I2C communications and set the operating mode
    bme = BME68X(cst.BME68X_I2C_ADDR_LOW, 0)
    bme.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)
    # report on the BME688 and BSEC version
    print(f'SENSOR: {bme.get_variant()} BSEC: {bme.get_bsec_version()}')

    air_ethanol = read_conf(config_path)
    print(f'SET BSEC CONF {bme.set_bsec_conf(air_ethanol)}')

    # Air and Ethanol - two subscriptions (0,1)
    print(f'SUBSCRIBE GAS ESTIMATES {bme.subscribe_gas_estimates(2)}')

    # initialise the sensor
    print(f'INIT BME68X {bme.init_bme68x()}')

    print('\n\nSTARTING MEASUREMENT\n')

    while(True):
        # print(bme.get_bsec_data())
        try:
            data = bme.get_digital_nose_data()
        except Exception as e:
            print(e)
            main()
        if data:
            # for entry in bme.get_digital_nose_data():
            entry = data[-1]
            # print(f'{entry}')
            print(f'NORMAL AIR {entry["gas_estimate_1"]:.1%}\nETHANOL {entry["gas_estimate_2"]:.1%}')
            print()

            NormalAir = "{:.1%}".format(entry["gas_estimate_1"])
            Ethanol = "{:.1%}".format(entry["gas_estimate_2"])

            # This bit is from the Meat and Cheese PI3G demo - ist writes out the data to file as JASON
            d = {
                'NormalAir': NormalAir,
                'Ethanol': Ethanol,
            }

            with open('/home/kpi/sniff-data.json', 'w') as file:
                json.dump(d, file)



if __name__ == '__main__':
    main()
