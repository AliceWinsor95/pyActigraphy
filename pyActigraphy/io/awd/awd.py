import pandas as pd
import numpy as np
import os
import re

from ..base import BaseRaw


class RawAWD(BaseRaw):
    """Raw object from .AWD file (recorded by ActiWatches)

    Parameters
    ----------
    input_fname: str
        Path to the AWD file.
    header_size: int
        Header size (i.e. number of lines) of the raw data file. Default is 7.
    frequency: str
        Data acquisition frequency.
        Cf. #timeseries-offset-aliases in
        <https://pandas.pydata.org/pandas-docs/stable/timeseries.html>.
        Default is '1T'.
    dtype: dtype
        The dtype of the raw data. Default is np.int.
    """

    def __init__(
        self,
        input_fname,
        header_size=7,
        frequency='1min',
        start_time=None,
        period=None,
        dtype=np.int
    ):

        # get absolute file path
        input_fname = os.path.abspath(input_fname)
        # [TO-DO] check if file exists
        # [TO-DO] check it is has the right file extension .awd

        # read data file
        raw_data = pd.read_csv(
            filepath_or_buffer=input_fname,
            encoding='utf-8',
            engine='python',
            header=None,
            delim_whitespace=True,
            names=['Activity', 'Marker'],
            usecols=['Activity'],
            squeeze=True
        )

        # extract header and data
        header = raw_data[:header_size]
        data = raw_data[header_size:]

        # extract informations from the header
        name = self.__extract_awd_name(header)
        uuid = self.__extract_awd_uuid(header)
        start = self.__extract_awd_start_time(header)

        # index data
        index_data = pd.Series(
            data=data.values,
            index=pd.date_range(
                start=start,
                periods=len(data),
                freq=frequency
            ),
            dtype=dtype
        )

        if start_time is not None and period is not None:
            start_time = pd.to_datetime(start_time)
            period = pd.Timedelta(period)
            index_data = index_data[start_time:start_time+period]
        else:
            start_time = start

        # call __init__ function of the base class
        super().__init__(
            name=name,
            uuid=uuid,
            format='AWD',
            axial_mode='mono-axial',
            start_time=start_time,
            frequency=pd.Timedelta(frequency),
            data=index_data,
            light=None
        )

    def __extract_awd_name(self, header):
        return re.sub(r'[^\w\s:]\r\n', '', header[0])

    def __extract_awd_uuid(self, header):
        return header[5]

    def __extract_awd_start_time(self, header):
        return pd.to_datetime(header[1] + ' ' + header[2])


def read_raw_awd(
    input_fname,
    header_size=7,
    frequency='1min',
    start_time=None,
    period=None,
    dtype=np.int
):
    """Reader function for raw AWD file.

    Parameters
    ----------
    input_fname: str
        Path to the AWD file.
    header_size: int
        Header size (i.e. number of lines) of the raw data file. Default is 7.
    frequency: str
        Data acquisition frequency.
        Cf. #timeseries-offset-aliases in
        <https://pandas.pydata.org/pandas-docs/stable/timeseries.html>.
        Default is '1T'.
    start_time: str
        Default is None.
    period: str
        Default is None.
    dtype: dtype
        The dtype of the raw data. Default is np.int.

    Returns
    -------
    raw : Instance of RawAWD
        An object containing raw AWD data
    """

    return RawAWD(
        input_fname=input_fname,
        header_size=header_size,
        frequency=frequency,
        start_time=start_time,
        period=period,
        dtype=dtype
    )
