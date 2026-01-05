import pandas as pd
import numpy as np
from pathlib import Path

def extract_data(path="financial_inclusion_dataset.csv"):
    return pd.read_csv(path)

#df = pd.read_csv("financial_inclusion_dataset.csv")

# In[2]:
def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    
    # 1. Fix Types First
    num_cols = ['mobile_money_user', 'loan_access', 'age', 'monthly_income']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # 2. Handle Negatives & Outliers BEFORE filling NaNs
    # (If we do this later, we create new NaNs that don't get filled)
    if 'monthly_income' in df.columns:
        df.loc[df['monthly_income'] < 0, 'monthly_income'] = np.nan
        
    if 'age' in df.columns:
        # Set realistic bounds for financial data (e.g., 18 to 100)
        df.loc[(df['age'] < 18) | (df['age'] > 100), 'age'] = np.nan

    # 3. Now Impute (Fill) the Missing Values
    if 'age' in df.columns:     
        df['age'] = df['age'].fillna(df['age'].median()).round(0)
    
    if 'monthly_income' in df.columns:
        df['monthly_income'] = df['monthly_income'].fillna(df['monthly_income'].median()).round(2)
        
    if 'country' in df.columns:
        df['country'] = df['country'].fillna('Unknown')
        
    if 'education_level' in df.columns:
        df['education_level'] = df['education_level'].fillna('Unknown')
        
    if 'gender' in df.columns:
        df['gender'] = df['gender'].fillna('Unknown')

    return df
   


# In[3]:
def transform_data(df):
    df = df.copy()
    # Normalize has_bank_account field (yes, no, unknown → 1/0/NaN).
    mapper = {'yes': 1, 'no': 0, '1': 1, '0': 0, '1.0': 1, '0.0': 0}
    df['has_bank_account'] = df['has_bank_account'].astype(str).str.lower().map(mapper)
    return df

# In[14]:
def validate_data(df):
    problems = []
    #nonegativeamounts
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
    




