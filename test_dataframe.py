"""
This module implements a test_create_dataframe function that check certain dataframe properties.
This function is also tested in this module using Python's unittest library.
"""

import unittest
import pandas as pd
import numpy as np


def test_create_dataframe(test_df, list_column_names):
    """
    Check the following properties of a DataFrame:
        1. The DataFrame contains only the columns that are specified as the second argument
        2. all columns have values of the correct type
        3. Check for nan values
        4. Verify that the DataFrame has at least one row
    :param test_df: DataFrame whose properties to be checked
    :param list_column_names: a list of column names that the DataFrame should contains
    :return: True if all the above conditions hold; False otherwise
    """
    result = True
    test_df_col = test_df.columns.values
    # The DataFrame contains only the columns that you specified as the second argument
    if not set(list_column_names) == set(test_df_col):
        result = False
    # There is no NAN in test_df
    if any([any(pd.isnull(test_df[col_name])) for col_name in list(test_df)]):
        raise ValueError('There is NaN in the dataframe.')
    # The values in each column have the same python type
    sets_of_type_in_column = [set(map(type, test_df[c])) for c in test_df_col]
    lengths_of_type_set_in_column = [len(t) for t in sets_of_type_in_column]
    if any(l > 1 for l in lengths_of_type_set_in_column):
        result = False
    # There are at least 10 rows in the DataFrame
    if test_df.shape[0] < 1:
        result = False
    return result


DEFAULT_DATAFRAME = pd.DataFrame({'float_col': [1.0, 2.0, 2.6, 4.7],
                                  'int_col': [1, 1, 2, 6],
                                  'string_col': ['foo', 'st', 'acb', 'fov']})


class TestDataFrameMethods(unittest.TestCase):
    """
    This class tests the above test_create_dataframe method
    """
    def test_all_columns_same_type(self):
        """
        Test for the functionality of checking all columns having values of the correct type
        :return: test passes if functionality works; test fails otherwise
        """
        # a dataframe that values in each column have the same type
        df1 = DEFAULT_DATAFRAME
        # a dataframe that some values in each column have different type
        df2 = DEFAULT_DATAFRAME.copy(deep=True)
        df2.loc[3, 'string_col'] = 98
        col_names = ['float_col', 'int_col', 'string_col']
        self.assertTrue(test_create_dataframe(df1, col_names))
        self.assertFalse(test_create_dataframe(df2, col_names))

    def test_check_nan(self):
        """
        Test for the functionality of checking for nan values
        :return: test passes if functionality works; test fails otherwise
        """
        col_names = ['float_col', 'int_col', 'string_col']
        df1 = df2 = DEFAULT_DATAFRAME.copy(deep=True)
        # change some values to nan
        df1.loc[2, 'int_col'] = np.nan
        df2.loc[3, 'string_col'] = np.nan
        # should raise error
        with self.assertRaises(ValueError):
            test_create_dataframe(df1, col_names)
            test_create_dataframe(df2, col_names)

    def test_at_least_one_row(self):
        """
        Test for the functionality of verifying that the dataframe has at least one row
        :return: test passes if functionality works; test fails otherwise
        """
        # a dataframe with at least 1 row
        df1 = pd.DataFrame(DEFAULT_DATAFRAME.head(1))
        # a dataframe with fewer than 1 row
        df2 = pd.DataFrame(DEFAULT_DATAFRAME.head(0))
        col_names = ['float_col', 'int_col', 'string_col']
        self.assertTrue(test_create_dataframe(df1, col_names))
        self.assertFalse(test_create_dataframe(df2, col_names))


if __name__ == '__main__':
    unittest.main()
