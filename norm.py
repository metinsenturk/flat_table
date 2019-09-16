from functools import reduce
import pandas as pd


def normalize_object(series):
    result = [{"index": ind, series.name: item} for ind, item in series.iteritems()]
    return pd.DataFrame(result)


def normalize_dict(series):
    [item.update({"index": ind}) for ind, item in series.iteritems()]
    return pd.io.json.json_normalize(series)


def normalize_list_old(series):
    result = []
    for in_ind, seri_item in series.iteritems():
        [item.update({"index": in_ind}) for item in seri_item]
        result.extend(seri_item)
    return pd.DataFrame(result)


def normalize_list(list_object, name="None", index="None"):
    result = []
    for item in list_object:
        if type(item) == list:
            normalize_list(item, name, index)
        elif type(item) == dict:
            item.update({"index": index})
            result.append(item)
        else:
            result.append({"index": index, name: item})
    print(result)
    return reduce(lambda x, y: pd.merge(x, y, on="index"), pd.DataFrame(result))


def normalize(dataframe):
    result = []
    for name, seri in dataframe.iteritems():
        if any(seri.apply(lambda x: type(x) == dict)):
            result.append(normalize_dict(seri))
        elif any(seri.apply(lambda x: type(x) == list)):
            result.append(normalize_list(seri))
        else:
            result.append(normalize_object(seri))
    return reduce(lambda x, y: pd.merge(x, y, on="index"), result)

