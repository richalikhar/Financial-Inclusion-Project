#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from pathlib import Path

def extract_data(path="financial_inclusion_dataset.csv"):
    return pd.read_csv(path)

#df = pd.read_csv("financial_inclusion_dataset.csv")


# In[2]:


df.head()


# In[2]:


def clean_data(df):
    df = df.copy()
    # drop exact duplicates
    df = df.drop_duplicates()
    # Standardize date type
    num_cols = ['mobile_money_user','loan_access','age','monthly_income']
    for c in num_cols:
        if c in df.columns:
            df[c]=pd.to_numeric(df[c],errors='coerce')
    if 'age' in df.columns:     
        df['age'] = df['age'].fillna(df['age'].median().round(0))
    if 'monthly_income' in df.columns:
        df['monthly_income'] = df['monthly_income'].fillna(df['monthly_income'].median().round(0))
    if 'country' in df.columns:
        df['country'] = df['country'].fillna('None')
    if 'education_level' in df.columns:
        df['education_level'] = df['education_level'].fillna('None')
    if 'gender' in df.columns:
        df['gender'] = df['gender'].fillna('Unknown')
    for c in  ['monthly_income','age','mobile_money_user']:
        if c in df.columns:
             df.loc[df[c] < 0,c] = np.nan
        return df
        


# In[10]:


df


# In[3]:


def transform_data(df):
    df = df.copy()
    # Normalize has_bank_account field (yes, no, unknown → 1/0/NaN).
    df['has_bank_account'] = df['has_bank_account'].astype(str)
    df['has_bank_account'] = (df['has_bank_account'].str.lower().replace({'yes': 1,'no': 0,'unknown': np.nan}))  
    return df







# In[14]:


def validate_data(df):
    problems = []
    #nonegativeamounts
    df = df[df['monthly_income'] >= 0]
    if(df['monthly_income'] < 0).any():
        problems.append("Negative Amount found")
       
    return problems



# In[5]:


##df.to_csv("financial_inclusion_dataset.csv")

def save_data(df, filename="financial_inclusion_dataset_new.csv"):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filename, index=False)
    return filename




# In[15]:


if __name__ == "__main__":
    df = extract_data("financial_inclusion_dataset.csv")
    dfc = clean_data(df)
    dft = transform_data(dfc)
    problems = validate_data(dft)
    print("Validation problems:", problems)
    save_data(dfc, "financial_inclusion_dataset_new.csv")
    print("Saved financial_inclusion_dataset.csv")
    


# In[ ]:




