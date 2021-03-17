
import numpy as np
import pandas as pd
import requests
import yaml
import matplotlib.pyplot as plt
from datetime import datetime
import re


def fetch_raw_data():
    '''
    sample URL of milano
    https://www.meteoschweiz.admin.ch/product/input/radio-soundings/VSST80.LSSW_20210302_0000.txt

    https://www.meteoschweiz.admin.ch/home/mess-und-prognosesysteme/atmosphaere/radiosondierung.html?query=emagramm&pageIndex=0&tab=search_tab
    '''

    with open('url_config.yaml') as f:
        url_config = yaml.safe_load(f)

    now = datetime.now()

    date = ".LSSW_{}{:02d}{:02d}".format(now.year, now.month, now.day)
    time = "_{:02d}00.txt".format(12 if now.hour > 12 else 0)

    file_list = []
    for station, stat_code in url_config["stations"].items():
        print(station, stat_code)
        req_str = url_config["base_url"] + stat_code + date + time
        res = requests.get(req_str)

        file_name = "rawfiles/" + station + "_" + stat_code + date + time
        with open(file_name, 'w') as f:
            f.write(res.text)
            file_list.append(file_name)

    return file_list


if __name__ == "__main__":

    file_list = fetch_raw_data()



    raw_file = file_list[3]

    for raw_file in file_list:
        ema = {}
        with open(raw_file, 'r') as f:
            for position, line in enumerate(f):
                if position == 0:
                    ema["Location"] = re.sub('[\s\/]', '_', line.strip()) #remove space and /
                elif position == 2:
                    lst = line.split()
                    ema["date"] = lst[0].strip()
                    ema["time"] = lst[1].strip()
                elif position == 4:
                    ema["headers"] = line.split()
                elif position == 5:
                    ema["units"] = line.split()

        ema["df"] = pd.read_csv(raw_file, delim_whitespace=True,
                                skiprows=7, names=ema["headers"])

        print(ema["df"])

        # using pandas dataframe is maybe a bit overkill
        # simply generate numpy arrays
        ema["data"] = np.genfromtxt(raw_file, skip_header=7)

        # number crunching

        # get height, temp as vectors
        # simplified with just using numpy and no pandas
        #h = ema["data"][:,0]

        h = ema["df"].loc[:, 'Height'].values
        h_delta = np.diff(h)

        h_mid = (h[:-1] + h[1:]) / 2

        T = ema["df"].loc[:, 'Temp'].values
        T_delta = np.diff(T)
        T_mid = (T[:-1] + T[1:]) / 2

        T_grad = T_delta / h_delta * 100

        plt.close('all')

        fig, ax = plt.subplots()

        for ix, hstripe in enumerate(h_mid):
            if T_grad[ix] < 100 and T_grad[ix] >= -0.5:
                plt.axhspan(
                    hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='red', alpha=0.5)
            elif T_grad[ix] < -0.5 and T_grad[ix] >= -0.8:
                plt.axhspan(
                    hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='green', alpha=0.5)
            elif T_grad[ix] < 0.8 and T_grad[ix] >= -100:
                plt.axhspan(
                    hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='blue', alpha=0.5)

        plt.plot(T_grad, h_mid)
        plt.plot(T_mid, h_mid)
        plt.grid(True, which="both")
        plt.ylabel('h')
        plt.xlabel('grad')
        # plt.legend(M.T)
        plt_title = "Temp Grad in " + ema["Location"] + " on " + ema["date"] + " , at " + ema["time"]
        plt.title(plt_title)
        # plt.ion()
        # plt.show()


        figure_name = 'static/images/' + re.sub('[\s\/]', '_', ema["Location"])


        plt.savefig(figure_name)


    '''
    https://matplotlib.org/3.1.1/gallery/subplots_axes_and_figures/axhspan_demo.html#sphx-glr-gallery-subplots-axes-and-figures-axhspan-demo-py
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/span_regions.html#sphx-glr-gallery-lines-bars-and-markers-span-regions-py
    http://pyhogs.github.io/colormap-examples.html
    '''

    print("done")
