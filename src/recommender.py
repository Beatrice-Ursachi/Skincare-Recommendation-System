import pandas as pd
from src.ingredient_processor import scoring_func

# scores all products in the dataframe by applying scoring_func to each product's ingredients_list
# filters products matching the user's product type with a positive score
# returns the top N recommendations and all matching products
def recommender(products_df,skin_concern_score,skin_type,skin_concern,product_type_input,top_n):
    products_df[['score','scored_count','bad_ingredients','good_ingredients']] = products_df['ingredients_list'].apply(lambda x: scoring_func(x, skin_type, skin_concern,skin_concern_score)).apply(pd.Series)

    product_df1=products_df[(products_df['product_type'] == product_type_input) & (products_df['score']>0)]
    result=product_df1.sort_values(by='score', ascending=False).head(top_n)
    return result[['product_name','score','scored_count','bad_ingredients','good_ingredients']],product_df1