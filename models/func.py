from sklearn.preprocessing import OrdinalEncoder, RobustScaler
from sklearn.model_selection import StratifiedKFold


def miss_values(data):
    col_null = []
    column = list(data.columns)
    for col in column:
        if data[col].isna().sum() > 0:
            col_null.append(col)
    mode = []
    for miss in col_null:
        mode.append(data[miss].mode())
    real_mode = []
    for modes in mode:
        real_mode.append(modes[0])
    val = {}
    for miss in col_null:
        for m in real_mode:
            val[miss] = m
            real_mode.remove(m)
            break
    for i, k in val.items():
        data[i].fillna(k, inplace=True)
    return data


# creating a function for ordinal encoding
def ordinal_encoding(data):
    """Performs ordinate encoding on columns with object datatypes.
    When calling the function, it takes in the data as a variable. """
    s = data.dtypes == "object"
    obj_col = list(s[s].index)
    ordinate = OrdinalEncoder()
    data[obj_col] = ordinate.fit_transform(data[obj_col])
    return data.head()


def stratified_splits(n_split, x, y):
    skf = StratifiedKFold(n_splits=n_split)

    for train_index, test_index in skf.split(x, y):
        x_train, x_test = x.loc[train_index], x.loc[test_index]
        y_train, y_test = y.loc[train_index], y.loc[test_index]
    return x_train, x_test, y_train, y_test


def rob_scaling(x, y):
    rob = RobustScaler()
    x = rob.fit_transform(x, y)
    return x
