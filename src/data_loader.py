import pandas as pd
import re
from pathlib import Path

# define a function to load and clean skincare products
def load_products():
    # create path for product csv file
    base=Path(__file__).parent.parent
    filepath=base/'data'/'skincare_products.csv'

    products_df=pd.read_csv(filepath)

    # drop irrelevant columns
    products_df=products_df.drop(columns=['product_url','price'])

    # drop products with missing ingredients lists (handling NA values)
    products_df=products_df.dropna()

    # convert relevant columns to lowercase for ease and consistency
    products_df['product_name']=products_df['product_name'].str.lower()
    products_df['ingredients']=products_df['ingredients'].str.lower()
    products_df['product_type']=products_df['product_type'].str.lower()

    # removing duplicates of the same product but different sizes in ml/oz/g
    products_df['product_name'] = products_df['product_name'].str.replace(r'\d+\s*ml', '', regex=True)
    products_df['product_name'] = products_df['product_name'].str.replace(r'\d+\s*oz', '', regex=True)
    products_df['product_name'] = products_df['product_name'].str.replace(r'\d+\s*g', '', regex=True)

    products_df= products_df.drop_duplicates(subset=["product_name"])

    # remove products that are not facial skincare
    products_df=products_df[(products_df['product_type']!='Bath Salts') & (products_df['product_type']!='Body Wash') & (products_df['product_type']!='Bath Oil')]

    products_df=products_df[~products_df['product_name'].str.contains('lip|hand|foot|feet', na=False)]

    # remove products that only contain 'body' but not 'face'
    products_df=products_df[~((products_df['product_name'].str.contains('body', na=False)) & ~(products_df['product_name'].str.contains('face', na=False)))]

    # convert ingredients from strings to lists
    products_df['ingredients_list']=products_df['ingredients'].str.split(',')

    return products_df


def load_ingredients():
    # create path for ingredients csv file
    base=Path(__file__).parent.parent
    filepath=base/'data'/'ingredientsList.csv'

    # import only the relevant columns
    ingredients_df=pd.read_csv(filepath)
    ingredients_df=ingredients_df[['name','who_is_it_good_for']]

    # clean up the column
    ingredients_df['who_is_it_good_for']=ingredients_df['who_is_it_good_for'].str.lower()
    ingredients_df["who_is_it_good_for"]=ingredients_df["who_is_it_good_for"].str.replace("' ',", "").str.replace("[", "").str.replace("]", "").str.replace("  '", "").str.replace("'", "")

    return ingredients_df
