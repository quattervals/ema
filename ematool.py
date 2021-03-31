
import numpy as np
import pandas as pd
import requests
import yaml
import matplotlib.pyplot as plt
import datetime
import re
import copy
import pickle

code_location = {
    'VSST76' : "Payerne",
    'VSST77' : "München",
    'VSST78' : "Stuttgart",
    'VSST80' : "Milano"
}

def fetch_raw_data(url_config: dict) -> list:
    '''
    sample URL of milano
    https://www.meteoschweiz.admin.ch/product/input/radio-soundings/VSST80.LSSW_20210302_0000.txt

    https://www.meteoschweiz.admin.ch/home/mess-und-prognosesysteme/atmosphaere/radiosondierung.html?query=emagramm&pageIndex=0&tab=search_tab
    '''

    point_in_time = ('current', 'previous')
    file_list = []
    now = datetime.datetime.now(datetime.timezone.utc)

    for pit in point_in_time:

        if pit == 'previous':
            now = now - datetime.timedelta(hours=12)

        date = ".LSSW_{}{:02d}{:02d}".format(now.year, now.month, now.day)
        time = "_{:02d}00.txt".format(12 if now.hour > 12 else 0)

        for station in url_config["stations"]:
            req_str = str(url_config["base_url"]) + str(station["code"]) + date + time
            res = requests.get(req_str)

            file_name = "rawfiles/" + str(station["name"]) + "_" + str(station["code"]) + date + time
            with open(file_name, 'w') as f:
                f.write(res.text)
                file_list.append(file_name)

    return file_list


def read_raw_data(raw_file: str) -> dict:
    """
    Reads from emagramm file at location raw_file

    Cleans NAN-like values
    Removes dupes

    Returns dict with a data frame of the measurements plus meta data
    """
    ema = {}
    ema["rawfile"] = raw_file

    with open(raw_file, 'r') as f:
        for position, line in enumerate(f):
            if position == 0:
                pass  # this is not really used # ema["Location"] = re.sub('[\s\/]', '_', line.strip()) #remove space and /
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

    # Alternative ################################################
    # using pandas dataframe is maybe a bit overkill
    # simply generate numpy arrays
    # ema["data"] = np.genfromtxt(raw_file, skip_header=7)
    # get height, temp as vectors
    # simplified with just using numpy and no pandas
    #h = ema["data"][:,0]

    # Clean nan-like values from df
    df = ema["df"]  # df is a reference to ema["df"] and used here as shorthand
    nan_vals = (9999.9, 999)
    for header in ema["headers"]:
        df.drop(df[df[header].isin(nan_vals)].index, inplace=True)

    # remove duplicate rows
    df.drop_duplicates(keep='first', inplace=True)

    # date time object to keep track of the time easily
    ema["datetime"] = datetime.datetime(*map(int, (ema["date"].split('-')[::-1])), hour=int(ema["time"][0:2]),
                                        tzinfo=datetime.timezone.utc)  # need to reverse the date from file to match Y,M,D order

    # if ema["datetime"] is less than 12 hours in the past from now, it is the current one
    # if ema["datetime"] is more than 12 hours in the past from now, it is the previous one
    now = datetime.datetime.now(datetime.timezone.utc)
    if now - ema["datetime"] < datetime.timedelta(hours=12):
        ema["cp"] = "current"
    else:
        ema["cp"] = "previous"

    ema["loc_code"] = re.search('VSST[0-9]{2}', ema["rawfile"])[0]

    return ema


def grad_calc(ema: dict) -> None:
    """
    Calculates temperature gradient
    Adds gradient data to ema
    """

    h = ema["df"].loc[:, 'Height'].values
    h_delta = np.diff(h.astype(float))

    h_mid = (h[:-1] + h[1:]) / 2

    T = ema["df"].loc[:, 'Temp'].values
    T_delta = np.diff(T)
    T_mid = (T[:-1] + T[1:]) / 2

    #avoid division by zero
    h_delta[h_delta == 0] = 0.1

    T_grad = T_delta / h_delta * 100

    ema["grad"] = pd.DataFrame(data=np.array([h_mid, h_delta, T_mid, T_grad]).T, columns=["h", "dH", "T", "dT"])


def grad_plot(ema: dict) -> None:
    """
    Makes saves plots

    Resources:

    https://matplotlib.org/3.1.1/gallery/subplots_axes_and_figures/axhspan_demo.html#sphx-glr-gallery-subplots-axes-and-figures-axhspan-demo-py
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/span_regions.html#sphx-glr-gallery-lines-bars-and-markers-span-regions-py
    http://pyhogs.github.io/colormap-examples.html
    """
    grad = ema["grad"]

    h_mid = grad["h"].values
    h_delta = grad["dH"].values
    T_mid = grad["T"].values
    T_grad = grad["dT"].to_numpy()

    plt.close('all')

    # pick colors from https://www.w3schools.com/colors/colors_picker.asp
    for ix, hstripe in enumerate(h_mid):
        if T_grad[ix] > 0:
            plt.axhspan(hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='#ff8000', alpha=0.5)
        elif 0   >= T_grad[ix] > -0.5:
            plt.axhspan(hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='#f2f2f2', alpha=0.5)
        elif -0.5 >= T_grad[ix] > -0.6:
            plt.axhspan(hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='#66ff99', alpha=0.5)
        elif -0.6 >= T_grad[ix] > -0.8:
            plt.axhspan(hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='#33cc33', alpha=0.5)
        elif -0.8 >= T_grad[ix] > -100:
            plt.axhspan(hstripe - 0.5 * h_delta[ix], hstripe + 0.5 * h_delta[ix], facecolor='#0099ff', alpha=0.5)

    plt.plot(T_grad, h_mid)
    plt.plot(T_mid, h_mid, color='#3F3F3F')
    plt.grid(True, which="both")
    plt.ylabel('Altitude AMSL [m]')
    plt.xlabel('Temperature [°C]')
    plt.ylim(0, 5000)
    plt.xlim(-30, 10)

    # plt.legend(M.T)
    plt_title = "Gradient in " + code_location[ema["loc_code"]] + " on " + ema["date"] + ", at " + ema["time"]
    plt.title(plt_title)
    # plt.ion()
    # plt.show()

    # file name depending on time of the ema
    figure_name = 'static/images/' + re.sub(r'[\s\/]', '_', ema["loc_code"]) + '_' + ema["cp"] + '.svg'

    plt.savefig(figure_name)

def ema():
    """
    Wraps all the Emagrammstuff in function
    """
    with open('url_config.yaml') as f:
        station_config = yaml.safe_load(f)

    stations = copy.deepcopy(station_config["stations"])

    file_list = fetch_raw_data(station_config)
    for raw_file in file_list:
        ema = read_raw_data(raw_file)
        grad_calc(ema)
        grad_plot(ema)

        for station in stations:
            if station["code"] == ema["loc_code"]:
                if ema["cp"] == 'current':
                    station["c_ema"] = ema
                elif ema["cp"] == 'previous':
                    station["p_ema"] = ema
                else:
                    print("neither current nor previous ema")
                    print(ema)

    with open(station_config["storage_file"], 'wb') as f:
        pickle.dump(stations, f)

if __name__ == "__main__":

    ema()
    print("done")
