"""Transformations applied to data exported from a REDCap project"""

import pandas as pd

def transform_data(form, data, status=False):
    """Apply transforms to data in place"""
    
    strip_whitespace(data)
    translate_dates(form, data)
    
    if not status:
        data.drop(columns=f'{form.form_name}_complete', inplace=True)

def strip_whitespace(df):
    """Strip leading/trailing whitespace and embedded newlines"""
    
    # Trim leading and trailing whitespace
    df.replace({r'^\s+':'', r'\s+$':''}, regex=True, inplace=True)
    
    # Remove embedded newlines
    df.replace(r'\r?\n', '  ', regex=True, inplace=True)

def translate_dates(form, df):
    """Translate date vars to datetime objects"""
    
    for item in form.items:
        
        if item.text_validation_type=='date_mdy':
            df[item.name] = pd.to_datetime(df[item.name],
                                           infer_datetime_format=True,
                                           errors='coerce')
        
        # TODO Need to figure out how to handle partial dates; for example,
        # currently '2016' gets coerced to '2016-01' which may not always be
        # the desired behavior
        elif item.text_validation_type=='date_my':
            df[item.name] = pd.to_datetime(df[item.name],
                                           infer_datetime_format=True,
                                           errors='coerce').dt.to_period('M')
