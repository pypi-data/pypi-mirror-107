#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A add_column step, which allows you to add a column to 
a dataframe. 
"""

from mitosheet.utils import create_new_step, does_sheet_index_exist_within_step
from mitosheet.errors import (
    make_column_exists_error,
    make_no_sheet_error
)

ADD_COLUMN_DISPLAY_NAME = 'Added a Column'

ADD_COLUMN_EVENT = 'add_column_edit'
ADD_COLUMN_STEP_TYPE = 'add_column'

ADD_COLUMN_PARAMS = [
    'sheet_index', # int
    'column_header', # the new column to create
    'column_header_index' # the index of the new column
]

def execute_add_column_step(
        curr_step,
        sheet_index,
        column_header,
        column_header_index
    ):
    """
    The function responsible for updating the widget state container
    with a new add_column step.
    """
    # if the sheet doesn't exist, throw an error
    if not does_sheet_index_exist_within_step(curr_step, sheet_index):
        raise make_no_sheet_error(sheet_index)

    if column_header in curr_step['column_metatype'][sheet_index]:
        raise make_column_exists_error(column_header)

    # We add a new step with the added column
    new_step = create_new_step(curr_step, ADD_COLUMN_STEP_TYPE)

    # If the column_header_index is out of range, then make the new column the last column
    if column_header_index < 0 or len(curr_step['dfs'][sheet_index].columns) <= column_header_index:
        column_header_index = len(curr_step['dfs'][sheet_index].columns)

    # Update the state variables
    new_step['column_metatype'][sheet_index][column_header] = 'formula'
    new_step['column_type'][sheet_index][column_header] = 'number'
    new_step['column_spreadsheet_code'][sheet_index][column_header] = '=0'
    new_step['column_python_code'][sheet_index][column_header] = f'df[\'{column_header}\'] = 0'
    new_step['column_evaluation_graph'][sheet_index][column_header] = set()
    new_step['column_filters'][sheet_index][column_header] = {'operator': 'And', 'filters': []}
        
    # Update the dataframe
    new_step["dfs"][sheet_index].insert(column_header_index, column_header, 0)
    
    return new_step


def transpile_add_column_step(
        step,
        sheet_index,
        column_header, 
        column_header_index
    ):
    """
    Transpiles an add column step to python code!
    """
    # If the column_header_index is out of range, then make the new column the last column
    # Note: here we subtract 1 from the len of the columns arrray because the array generated from 
    # the step dfs object already inclused the column header that the transpiled code is adding.
    if column_header_index < 0 or len(step['dfs'][sheet_index].columns) <= column_header_index:
        column_header_index = len(step['dfs'][sheet_index].columns) - 1

    return [
        f'{step["df_names"][sheet_index]}.insert({column_header_index}, \'{column_header}\', 0)'
    ]


def describe_add_column_step(
        sheet_index,
        column_header,
        column_header_index,
        df_names=None
    ):    
    if df_names is not None:
        df_name = df_names[sheet_index]
        return f'Added column {column_header} to {df_name}'
    return f'Added column {column_header}'


ADD_COLUMN_STEP = {
    'step_version': 2,
    'step_display_name': ADD_COLUMN_DISPLAY_NAME,
    'event_type': ADD_COLUMN_EVENT,
    'step_type': ADD_COLUMN_STEP_TYPE,
    'params': ADD_COLUMN_PARAMS,
    'saturate': None,
    'execute': execute_add_column_step,
    'transpile': transpile_add_column_step,
    'describe': describe_add_column_step
}