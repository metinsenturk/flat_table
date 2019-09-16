from functools import reduce
from itertools import chain
import pandas as pd


def get_list_obj(df_list):
    column_name = df_list.name
    df_list = df_list.reset_index()
    
    df_list = df_list.apply(lambda x: [{'index': x['index'], column_name: ins} for ins in x[column_name]], axis=1)
    return pd.DataFrame(list(chain(*df_list))) 


def get_list_dict(df_list):
    column_name = df_list.name
    df_list = df_list.reset_index()
    
    df_list.apply(lambda x: [ins.update({'index': x['index']}) for ins in x[column_name]], axis=1)
    # pd.DataFrame(list(chain(*df_list.family)))
    return pd.io.json.json_normalize(list(chain(*df_list[column_name])))


def get_list_list(df_list):
    temp = get_list_obj(df_list)
    temp.index = temp['index'].values
    temp.drop('index', inplace=True, axis=1)
    return temp.iloc[:,0]


def get_column_list(series):
    inside = series.apply(lambda x: [type(i) for i in x][0]).iloc[0]
    print(series.name, inside)
    if inside == list:
        temp = get_list_list(series)
        return get_column_list(temp)
    elif inside == dict:
        return get_list_dict(series)
    else:
        return get_list_obj(series)


def get_column_obj(series):
    df_obj = series.reset_index()
    return df_obj


def get_column_dict(series):
    df_dict = pd.io.json.json_normalize(series)
    df_dict['index'] = series.index
    return df_dict


def reset_index(dataframe):
    temp = dataframe
    temp.index = temp['index'].values
    temp.drop('index', inplace=True, axis=1)
    return temp


def normalize(dataframe):
    result = []
    for name, seri in dataframe.iteritems():
        inside = seri.apply(lambda x: type(x)).iloc[0]
        if inside == list:
            print('normalizing:: ', name, inside)
            temp = get_column_list(seri)
            temp = reset_index(temp)
            op = normalize(temp)
            result.extend(op)
        elif inside == dict:
            print('normalizing:: ', name, inside)
            temp = get_column_dict(seri)
            temp = reset_index(temp)
            op = normalize(temp)
            result.extend(op)
        else:
            temp = get_column_obj(seri)
            #print(temp.columns.values)
            result.append(temp)
            # print(len(result))
    return reduce(lambda x, y: pd.merge(x, y, on="index", copy=False), result)