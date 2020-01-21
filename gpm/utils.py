ADRESS_COL_NAME = "full_address"


def add_adress(df, l_cols):
    """
    create new adress column concatenating all cols from l_cols
    :param df: input csv
    :param l_cols: cols to concatenate
    :return: df with additional adress col
    """
    sep = " "
    df_res = df[l_cols[0]].astype(str) + sep
    for col in l_cols[1:]:
        df_res += df[col].astype(str)
        df_res += sep
    df[ADRESS_COL_NAME] = df_res
    return df