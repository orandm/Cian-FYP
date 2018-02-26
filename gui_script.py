# Created:  23/02/2018
# Author:   Oran Dolphin-Murray
# Email:    oran.dolphin-murray@ul.ie
# Licence:  GNU
# ----------------------------------------------

import numpy as np
import tkinter as tk


class Application:

    currentLatLon = [52.673775, -8.572778]

    def __init__(self, master):

        self.master = master

        # Begin to build the GUI
        self.master.wm_title("Distance & Direction")

        tk.Label(self.master, text="Current Position", font=("Helvetica", 16, 'bold'), padx=5, pady=10,
                 justify="left").grid(row=0, column=0, sticky='W')
        tk.Label(self.master, text="\t LAT: {0}".format(self.currentLatLon[0]), font=("Helvetica", 16),
                 pady=10).grid(row=0, column=1, columnspan=2)
        tk.Label(self.master, text="\t LON: {0}".format(self.currentLatLon[1]), font=("Helvetica", 16),
                 pady=10, padx=5).grid(row=0, column=3, columnspan=2)

        tk.Label(self.master, text="Destination Position", font=("Helvetica", 16, 'bold'), pady=10,
                 justify='left', padx=5).grid(row=1, column=0)

        tk.Label(self.master, text="\tLAT:", font=("Helvetica", 16), pady=10).grid(row=1, column=1)
        self.master.dLat = tk.Entry(self.master)
        self.master.dLat.config(width=10)
        self.master.dLat.grid(row=1, column=2)
        tk.Label(self.master, text="\t LON:", font=("Helvetica", 16), pady=10).grid(row=1, column=3)
        self.master.dLon = tk.Entry(self.master)
        self.master.dLon.config(width=10)
        self.master.dLon.grid(row=1, column=4, padx=5)

        tk.Button(self.master, text="Calculate", font=("Helvetica", 16), pady=10, fg='black',
                  command=self.calculations, width=40).grid(row=2, column=0, columnspan=5)

        tk.Label(self.master, text="Distance:", font=("Helvetica", 16, 'bold'), pady=10, padx=5,
                 justify="left").grid(row=3, column=0, sticky='W')

        tk.Label(self.master, text="Direction:", font=("Helvetica", 16, 'bold'), pady=10, padx=5,
                 justify="left").grid(row=4, column=0, sticky='W')

        self.master.distance = tk.Label(self.master, text="", font=("Helvetica", 16, 'bold'), pady=10,
                                        justify="left")
        self.master.distance.grid(row=3, column=1, sticky='W')
        self.master.direction = tk.Label(self.master, text="", font=("Helvetica", 16, 'bold'), pady=10,
                                         justify='left')
        self.master.direction.grid(row=4, column=1, sticky='W')

    def calculations(self):
        lat1, lon1 = np.radians(self.currentLatLon)

        r = 6371  # Radius of Earth

        try:
            lat2, lon2 = np.radians((float(self.master.dLat.get()), float(self.master.dLon.get())))
        except ValueError:
            return
        # Distance
        # convert to radians
        lat_distance, lon_distance = [(lat2 - lat1), (lon2 - lon1)]

        # Haversine Formula
        a = np.sin(lat_distance / 2) * np.sin(lat_distance / 2) + np.cos(lat1) * np.cos(lat2) * \
            np.sin(lon_distance / 2) * np.sin(lon_distance / 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = r * c * 1000


        # Direction
        lonDelta = lon2 - lon1

        if lat1 == lat2 and lonDelta is 0:
            direction = 0

        # determine the absolute bearing between two given pairs of latitudes/longitudes
        y = np.sin(lonDelta) * np.cos(lat2)
        x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lonDelta)
        theta = np.degrees(np.arctan2(y, x))
        direction = (theta + 360) % 360

        # avoid errors if angles are negative
        if direction < 0:
            direction = 360 + direction

        self.draw_results(distance, direction)

    def draw_results(self, distance, direction):
        distance_bins = ['green', 'yellow', 'red']
        direction_bins = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

        if distance < 1000:
            font = distance_bins[0]
        elif distance > 10000:
            font = distance_bins[2]
        else:
            font = distance_bins[1]

        if 22.5 <= direction < 67.5:
            direction_label = direction_bins[1]
        elif 67.5 <= direction < 112.5:
            direction_label = direction_bins[2]
        elif 112.5 <= direction < 157.5:
            direction_label = direction_bins[3]
        elif 157.5 <= direction < 202.5:
            direction_label = direction_bins[4]
        elif 202.5 <= direction < 247.5:
            direction_label = direction_bins[5]
        elif 247.5 <= direction < 292.5:
            direction_label = direction_bins[6]
        elif 292.5 <= direction < 337.5:
            direction_label = direction_bins[7]
        else:
            direction_label = direction_bins[0]

        self.master.distance.config(text="{0} metres.".format(int(distance)), fg=font)
        self.master.direction.config(text=direction_label)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()