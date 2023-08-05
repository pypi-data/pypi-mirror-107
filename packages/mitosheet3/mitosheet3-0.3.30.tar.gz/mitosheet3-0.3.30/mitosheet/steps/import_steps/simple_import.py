#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A simple import, which allows you to import dataframes with the given file_names

NOTE: special care needs to be taken when upgrading this step, as it is used (e.g in the 
api in special ways). Not sure exactly how, but be careful + test it thoroughly.
"""
import os
import pandas as pd
import json
import csv

from mitosheet.mito_analytics import log
from mitosheet.errors import make_is_directory_error
from os.path import basename, normpath
from mitosheet.utils import add_df_to_step, create_new_step, get_header_renames, make_valid_header

SIMPLE_IMPORT_DISPLAY_NAME = 'Imported CSV Files'

SIMPLE_IMPORT_EVENT = 'simple_import_edit'
SIMPLE_IMPORT_STEP_TYPE = 'simple_import'

SIMPLE_IMPORT_PARAMS = [
    'file_names', # list of strings
]

def guess_delimeter(file_name: str):
    """
    Given a path to a file that is assumed to exist and be a CSV, this
    function guesses the delimeter that is used by that file
    """
    s = csv.Sniffer()
    with open(file_name, 'r') as f:
        return s.sniff(f.readline()).delimiter

def file_name_to_df_name(file_name: str):
    # First, we strip off any path beyond the final filename
    file_name = basename(normpath(file_name))

    # We abuse the fact that all valid mito headers are almost valid variable names
    # If they start w/ numbers, we add letters
    possible_var_name = make_valid_header(file_name)
    if len(possible_var_name) == 0 or possible_var_name[0].isnumeric():
        return 'df_' + possible_var_name
    return possible_var_name

def get_dataframe_names(file_names, existing_df_names):
    """
    Helper function for taking a list of file names and turning them into valid
    names for dataframes.

    NOTE:
    1. If there are duplicates, appends onto the end of them to deduplicate.
    2. Avoids overwriting existing df names.
    """
    new_names_inital = [file_name_to_df_name(file_name) for file_name in file_names]

    final_names = []

    # Keep appending names till we get one that doesn't overlap
    for name in new_names_inital:
        curr_name = name
        count = 0
        while curr_name in final_names or curr_name in existing_df_names:
            curr_name = f'{name}_{count}'
            count += 1
        
        final_names.append(curr_name)
    
    return final_names


def execute_simple_import(
        curr_step,
        file_names
    ):
    """
    Imports the files with the given file names into the sheet
    """
    # If any of the files are directories, we throw an error to let
    # the user know
    for file_name in file_names:
        if os.path.isdir(file_name):
            raise make_is_directory_error(file_name)

    # Create a new step
    new_step = create_new_step(curr_step, SIMPLE_IMPORT_STEP_TYPE, deep=False)

    column_header_renames = dict()
    file_delimeters = dict()
    for file_name, df_name in zip(file_names, get_dataframe_names(file_names, new_step['df_names'])):

        delimeter = guess_delimeter(file_name)
        file_delimeters[df_name] = delimeter

        if delimeter != ',':
            log('used_non_standard_delimeter', {'delimeter': delimeter})

        df = pd.read_csv(file_name, sep=delimeter)
        renames = get_header_renames(df.keys())
        if len(renames) > 0:
            # Save that we did these renames
            column_header_renames[df_name] = renames
            # Actually perform any renames we need to
            df.rename(columns=renames, inplace=True)

        add_df_to_step(new_step, df, df_name=df_name)        

    # Save the renames that have occured in the step, for transpilation reasons
    # and also save the seperator that we used for each file
    new_step['column_header_renames'] = column_header_renames
    new_step['file_delimeters'] = file_delimeters

    return new_step


def transpile_simple_import(
        step,
        file_names
    ):
    """
    Transpiles a sort step to Python code. 
    """

    code = ['import pandas as pd']
    for file_name, df_name in zip(file_names, step['df_names'][len(step['df_names']) - len(file_names):]):

        delimeter = step['file_delimeters'][df_name]

        if delimeter == ',':
            # We don't add the delimeter if it's the default comma
            code.append(
                f'{df_name} = pd.read_csv(\'{file_name}\')'
            )
        else:
            # If there is a delimeter for this file, we use it
            code.append(
                f'{df_name} = pd.read_csv(\'{file_name}\', sep=\'{delimeter}\')'
            )
        # If we had to rename columns, mark that as well
        if df_name in step['column_header_renames']:
            renames = step['column_header_renames'][df_name]
            code.append(
                f'{df_name}.rename(columns={json.dumps(renames)}, inplace=True)'
            )

    return code


def describe_simple_import(
        file_names,
        df_names=None
    ):
    return f'Imported {", ".join(file_names)}'


SIMPLE_IMPORT_STEP = {
    'step_version': 1,
    'step_display_name': SIMPLE_IMPORT_DISPLAY_NAME,
    'event_type': SIMPLE_IMPORT_EVENT,
    'step_type': SIMPLE_IMPORT_STEP_TYPE,
    'params': SIMPLE_IMPORT_PARAMS,
    'saturate': None,
    'execute': execute_simple_import,
    'transpile': transpile_simple_import,
    'describe': describe_simple_import
}