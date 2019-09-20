#!/usr/bin/python3
from functools import reduce
from itertools import chain
import pandas as pd
import datetime
import logging

now = datetime.datetime.now()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        # logging.FileHandler("{0}/{1}.log".format('logs',now.strftime(r"%y-%m-%d-%H%M"))),
        logging.StreamHandler()
    ])

logger = logging.getLogger(__name__)


def get_list_obj(series):
    """ returns a dataseries of given series object. expands by the rows  """
    ds = series.copy()
    df = ds.reset_index()
    data = df.apply(
        lambda x: [{'index': x['index'], ds.name: ins} for ins in x[ds.name]], 
        axis=1
    )
    df = pd.DataFrame(list(chain(*data)))
    
    return set_index(df).iloc[:,0]


def get_column_obj(series):
    """ returns dataframe with index and the series.name """
    df_obj = series.reset_index()
    return df_obj


def get_column_dict(series, create_index=True):
    """ returns dataframe of normalized dictionary object """
    ds = series.copy()
    df = pd.io.json.json_normalize(ds)
    if create_index:
        df.index = ds.index
    return df


def set_index(df_or_ds, index_values=None):
    """ utility function to re set indexes in series and dataframes """
    temp = df_or_ds.copy()
    if index_values is None:
        temp.index = temp['index'].values
        temp.drop('index', inplace=True, axis=1)
    else:
        temp.index = index_values
    return temp


def get_obj(series):
    ds = series
    while True:
        ds = get_list_obj(ds)
        inside = ds.apply(lambda x: type(x)).iloc[0]
        logger.info(f'<Trial #  type: {inside} , len: {len(ds)}>')
        if inside != list:
            break
    
    return ds


def normalize(dataframe):
    result = []

    # get all series
    series_list = list(dataframe.iteritems())
    logger.info(f'series_list length:: current: {len(series_list)}')

    # iterate through each column/ series
    for _name, seri in series_list:
        # type of the object of series' values
        inside = seri.apply(lambda x: type(x)).iloc[0]

        # case if it is list -- expand rowwise
        if inside == list:
            temp = get_obj(seri)
            logger.info(f'expanding:: , {_name}, {inside} ==> seri: {seri.shape} temp: {temp.shape}')
            assert type(temp) == pd.Series
            series_list.append((_name, temp))

        # case if it is dict -- expand columnwise
        elif inside == dict:
            temp = get_column_dict(seri)
            logger.info(f'normalizing:: , {_name}, {inside} ==> seri: {seri.shape} temp: {temp.shape}')
            if len(temp) > 1:
                assert type(temp) == pd.DataFrame
                series_list.extend(list(temp.iteritems()))
            else:
                assert type(temp) == pd.Series
                series_list.append((_name, temp))

        # case of all others
        else:
            temp = get_column_obj(seri)
            assert type(temp) == pd.DataFrame
            result.append(temp)
            logger.info(f'columns added: , {_name}, {inside}, len: {temp.shape}')

    logger.info(f'exports :: , {len(result)}')
    logger.info([len(i) for i in result])

    return result