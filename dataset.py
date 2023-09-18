import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset as NetCDFDataset


class Dataset:
    def __init__(self):
        self.data = None

    def load_from_directory(self, directory):
        if not os.path.isdir(directory):
            raise ValueError('Directory not found')

        netcdf_files = [file for file in os.listdir(directory) if file.endswith(('.nc', '.nc4'))]

        if not netcdf_files:
            raise ValueError('No NetCDF files found in the directory')

        data_frames = []

        for netcdf_file in netcdf_files:
            file_path = os.path.join(directory, netcdf_file)
            with NetCDFDataset(file_path, 'r') as nc:
                latitudes = nc.variables['lat'][:]
                longitudes = nc.variables['lon'][:]
                levels = nc.variables['lev'][:]
                times = nc.variables['time'][:]
                temperature = nc.variables['T'][:]

                multi_index = pd.MultiIndex.from_product([latitudes, longitudes, levels, times],
                                                         names=['lat', 'lon', 'lev', 'time'])
                data_df = pd.DataFrame({'T': temperature.flatten()}, index=multi_index)

            data_frames.append(data_df)

        self.data = pd.concat(data_frames)

        return self.data

