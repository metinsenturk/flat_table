#!/usr/bin/python3
from functools import reduce
from itertools import chain
import pandas as pd
import datetime
import logging

now = datetime.datetime.now()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    handlers=[
        logging.FileHandler("{0}/{1}.log".format('logs',now.strftime(r"%y-%m-%d-%H%M"))),
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

    return set_index(df).iloc[:, 0]


def to_index(series):
    """ returns dataframe with index and the series.name """
    df_obj = series.reset_index()
    return df_obj


def set_index(df_or_ds, index_values=None):
    """ utility function to re set indexes in series and dataframes """
    temp = df_or_ds.copy()
    if index_values is None:
        temp.index = temp['index'].values
        temp.drop('index', inplace=True, axis=1)
    else:
        temp.index = index_values
    return temp


def to_columns(series, create_index=True):
    """ returns dataframe of normalized dictionary object """
    ds = series.copy()
    df = pd.io.json.json_normalize(ds)
    if create_index:
        df.index = ds.index
    return df


def to_rows(series):
    """ gets the object from a list in a series """
    ds = series
    while True:
        ds = get_list_obj(ds)
        inside = ds.apply(lambda x: type(x)).iloc[0]
        logger.info(f'<Trial #  type: {inside} , len: {len(ds)}>')
        if inside != list:
            break

    return ds


def print_parent_child_node(parent: str, child: pd.Series):
    """ shows parent child relation btw columns and their values """
    logger.info('{:20} {:20} {:15} {:10}'.format(
        parent, child.name, get_type(child), str(child.shape)))


def get_type(child):
    """ get type of the values of the dataseries object """
    return child.apply(lambda x: type(x)).iloc[0].__name__


def mapper(df):
    """ maps the relationship rowwise and columnwise expansion. """
    headers = ['parent', 'child', 'type', 'obj']
    series_list = [('.', n, get_type(s), s) for n, s in df.iteritems()]

    for ind, (parent, name, typ, child) in enumerate(series_list):
        inside = child.apply(lambda x: type(x)).iloc[0]

        # parent child nodes '.' level
        print_parent_child_node(parent, child)

        # expand rowwise, add new series for processing
        if inside == list:
            _child = to_rows(child)
            series_list.insert(
                ind + 1, (name, _child.name, get_type(_child), _child))
            print_parent_child_node(name, _child)

        # expand columnwise, add new columns for processing
        if inside == dict:
            temp = to_columns(child)
            if temp.shape[1] > 1:
                for _name, _child in temp.iteritems():
                    series_list.insert(
                        ind + 1, (name, _name, get_type(_child), _child))
                    print_parent_child_node(name, _child)
            else:
                _child = temp.iloc[:, 0]
                series_list.insert(
                    ind + 1, (name, _child.name, get_type(_child), _child))
                print_parent_child_node(name, _child)

    return pd.DataFrame(data=series_list, columns=headers)
