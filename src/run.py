import sys
from pathlib import Path

# allow import from src folder
sys.path.insert(0,str(Path(__file__).parent.parent))

from src.data_loader import load_products, load_ingredients
from src.ingredient_processor import concern_score
from src.recommender import recommender
from src.graph_visualiser import plot_top_good_ingredients, plot_top_bad_ingredients,plot_score_distribution,plot_score_vs_counts

top_n=3

# function to receive and validate user inputs
def user_input():
    # receive and validate user inputs
    print("--SKINCARE RECOMMENDATION SYSTEM--")

    # user inputs skin concern, skin type and product type
    # check ensures that each input is correct, returns error if input is incorrect
    print("Please input:")
    skin_type=input("skin type (dry/oily/sensitive/normal):  ").lower().strip()
    valid_skin_type=["dry","oily","sensitive","normal"]
    if skin_type not in  valid_skin_type:
        print("Error: invalid skin type")
        return

    skin_concern=input("skin concern (acne/aging/redness/dehydration/dullness):  ").lower().strip()
    valid_skin_concern=["acne","aging","redness","dehydration","dullness"]
    if skin_concern not in  valid_skin_concern:
        print("Error: invalid skin concern")
        return

    product_type_input=input("product type (moisturiser/serum/oil/mist/balm/mask/peel/eye care/cleanser/toner/exfoliator):  ").lower().strip()
    valid_product_type=["moisturiser","serum","oil","mist","balm","mask","peel","eye care","cleanser","toner","exfoliator"]
    if product_type_input not in  valid_product_type:
        print("Error: invalid product type input")
        return

    return skin_type,skin_concern,product_type_input

# function to display and format recommendations
def result_output(result,top_n=3):

    if len(result)==0:
        print("Sorry, no products found matching your criteria")
        return

    print("--TOP RECOMMENDATIONS--")

    for i in range(min(top_n,len(result))):
        print(i+1,".", result.iloc[i]['product_name'],"  Score:",round(result.iloc[i]['score'],3))
        print("This product is recommended because it contains: ", set(result.iloc[i]['good_ingredients']))


# function to run the full pipeline: get user input, load data, get recommendations, and generate visualisations
def run():
    # set number of products to recommend
    top_n=3

    # get user input
    get_user_input=user_input()

    if get_user_input is None:
        print("Invalid input")
        return
    
    skin_type, skin_concern, product_type_input = get_user_input

    # load data and functions
    print("Data currently loading...")
    product_df=load_products()
    ingredients_df=load_ingredients()
    skin_concern_score=concern_score(ingredients_df)
    print("Data loaded")

    # get recommendations (result=top_n, product_df1=all matching products)
    output = recommender(product_df, skin_concern_score, skin_type, skin_concern, product_type_input, top_n)
    result, product_df1 = output

    # display recommendations in terminal
    result_output(result,top_n)

    # generate visualisations
    plot_top_good_ingredients(result)
    plot_top_bad_ingredients(result)
    plot_score_distribution(product_df)
    plot_score_vs_counts(product_df1)


if __name__=="__main__":
    run()
