#!/usr/bin/python3
from functools import reduce
from itertools import chain
import pandas as pd
import datetime
import logging
import os

now = datetime.datetime.now()
dirname = os.path.dirname(os.path.realpath('__file__'))
logfile = "{0}/{1}/{2}.log".format(dirname, 'logs', now.strftime(r"%y-%m-%d-%H%M"))

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(filename=logfile, mode='a+'),
        logging.StreamHandler()
    ])

logger = logging.getLogger(__name__)


def get_list_obj(series):
    """ returns a dataseries of given series object. expands by the rows  """
    ds = series.copy()
    df = ds.reset_index()
    data = df.apply(
        lambda x: [
            {'index': x['index'], ds.name: ins} 
            for ins in x[ds.name]
        ] 
        if type(x[ds.name]) == list 
        else [{'index': x['index'], ds.name: x[ds.name]}],
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


def to_columns(series):
    """ returns dataframe of normalized dictionary object """
    ds = series.copy()
    # rows with values
    ds_withvalues = ds[pd.notna(ds)]
    df_withvalues = pd.io.json.json_normalize(ds_withvalues)
    df_withvalues.index = ds_withvalues.index

    # rows with nans
    ds_withnans = ds[pd.isna(ds)]
    df_withnans = pd.DataFrame(columns=df_withvalues.columns, index=ds_withnans.index)

    # concat both
    df = pd.concat([df_withvalues, df_withnans]).sort_index()
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
    logger.info('{:40} {:20} {:15} {:10}'.format(
        parent, child.name, get_type(child), str(child.shape)))


def get_type(child):
    """ get type of the values of the dataseries object """
    df = child[pd.notna(child)]
    typ = ''
    if len(df) > 0:
        typ = df.apply(lambda x: type(x)).iloc[0].__name__
    else:
        typ = type(pd.np.nan).__name__
    
    return typ


def mapper(df):
    """ maps the relationship rowwise and columnwise expansion. """
    headers = ['parent', 'child', 'type', 'obj']
    series_list = [('.', n, get_type(s), s) for n, s in df.iteritems()]

    for ind, (parent, name, typ, child) in enumerate(series_list):
        inside = get_type(child)
        name = ''.join([parent, name]) if parent == '.' else '.'.join([parent, name])

        # parent child nodes '.' level
        print_parent_child_node(parent, child)

        # expand rowwise, add new series for processing
        if inside == 'list':
            _child = to_rows(child)
            series_list.insert(
                ind + 1, (name, _child.name, get_type(_child), _child))
            print_parent_child_node(name, _child)

        # expand columnwise, add new columns for processing
        if inside == 'dict':
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


def normalize(df):
    """ normalize rows and columns of a given dataframe """
    dfs = []
    rts = []
    dataframe = df[(df.type != 'dict') & (df.type != 'list')]
    # final packing for list type childs  (concat)
    for parent in dataframe.parent.unique():
        group = dataframe[dataframe.parent.isin([parent])]
        df_group = pd.concat([i for i in group.obj], axis=1)
        dfs.append(df_group)
        logger.info('{:40} before: {:7} after: {:7} obj.shape: {:7} columns: {}'.format(
            parent, 
            str(group.shape),
            str(df_group.shape),
            str(group.obj.iloc[0].shape),
            str(', '.join(df_group.columns.tolist())[:50] + '..')
        ))

    # final packing for all childs        (merge)
    for _df in dfs:
        rts.append(to_index(_df))

    return reduce(lambda x,y: pd.merge(x, y, on='index'), rts)