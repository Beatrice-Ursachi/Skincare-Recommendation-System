import pandas as pd
# INGREDIENT STANDARDISATION
# create dicitonary to standarise ingredients, as multiple names can be used to refer to the same ingredient
standard_ingred={
    "sodium lauryl sulfate":"sls", "lauryl sodium sulfate":"sls", "sodium lauryl sulphate":"sls", "lauryl sodium sulphate":"sls",
    "sodium laureth sulfate":"sles", "sodium lauryl ether sulfate":"sles", "sodium lauryl ether sulphate":"sles", 
    "sodium laureth sulphate":"sles",
    "parfum":"fragrance",
    "ceramide np": "ceramide","ceramide ap": "ceramide","ceramide eop": "ceramide","ceramide ns": "ceramide","ceramide ng": "ceramide","ceramide 1": "ceramide",
    "ceramide 2": "ceramide","ceramide 3": "ceramide","ceramide 6 ii": "ceramide","phytosphingosine": "ceramide","sphingosine": "ceramide","ceramide complex": "ceramide",
    "retinol":"retinoid", "retinal":"retinoid", "retinoic acid":"retinoid", "retinaldehyde":"retinoid",
    "l-ascorbic acid":"vitamin c", "ascorbic acid":"vitamin c","magnesium ascorbyl phosphate":"vitamin c","sodium ascorbyl phosphate":"vitamin c",
    "ascorbyl glucoside":"vitamin c","ascorbyl palmitate":"vitamin c","ethyl ascorbic acid":"vitamin c","tetrahexyldecyl ascorbate":"vitamin c",
    "hydrolyzed hyaluronic acid":"hyaluronic acid","sodium hyaluronate":"hyaluronic acid","sodium hyaluronate crosspolyme":"hyaluronic acid","sodium acetylated hyaluronate":"hyaluronic acid",
    "beta hydroxy acid":"salicylic acid",
    "sulphur":"sulfur",
    "provitamin b5":"panthenol",
    "butylene glycol":"butylene",
    "epidermal growth factor": "growth_factor","fibroblast growth factor": "growth_factor","transforming growth factor": "growth_factor","insulin-like growth factor": "growth_factor",
    "vascular endothelial growth factor": "growth_factor", "human epidermal growth factor": "growth_factor","sh-oligopeptide-1": "growth_factor","sh-oligopeptide-2": "growth_factor",
    "sh-polypeptide-1": "growth_factor","sh-polypeptide-9": "growth_factor","rh-oligopeptide-1": "growth_factor",
    "palmitoyl pentapeptide-4": "peptide","palmitoyl tripeptide-1": "peptide","palmitoyl tetrapeptide-7": "peptide","acetyl hexapeptide-8": "peptide",
    "copper tripeptide-1": "peptide","tripeptide-1": "peptide","tetrapeptide-1": "peptide","oligopeptide-1": "peptide","matrixyl": "peptide","argireline": "peptide",
    "tocopherol":"vitamin e","tocopheryl linoleate":"vitamin e","tocopherol acetate":"vitamin e",
    "sd alcohol":"alcohol denat", "sd alcohol 39-b":"alcohol denat", "sd alcohol 40-b":"alcohol denat" , "denatured alcohol":"alcohol denat",
    "ethyl alcohol":"ethanol", "theobroma oil":"cocoa butter", 
    "triticum vulgare germ oil":"wheat germ oil", "wheat germ extract oil":"wheat germ oil",
    "acetylated lanolin alcohol":"acetylated lanolin",  "peg-75 lanolin":"ethoxylated lanolin", "peg-16 lanolin":"ethoxylated lanolin",
    "peg-40 lanolin":"ethoxylated lanolin", "peg-55 lanolin":"ethoxylated lanolin",
    "tetradecyl myristate":"myristyl myristate", "octyl palmitate":"ethylhexyl palmitate", "octyl stearate":"ethylhexyl stearate",
    "butyrospermum parkii butter":"shea butter", "dodecanoic acid":"lauric acid",
    "butyl octadecanoate":"butyl stearate", "octadecanoic acid":"butyl stearate", "retinaldehyde":"retinal",
    "lemon peel oil":"lemon oil", "citrus limon peel oil":"lemon oil", "citrus aurantium dulcis oil":"orange oil",
    "bergamot essential oil":"bergamot oil", "citrus aurantium bergamia peel oil":"bergamot oil",
    "ho wood oil":"cinnamon bark oil", "cinnamomum camphora bark oil":"cinnamon bark oil", "lemon grass oil":"lemongrass oil",
    "cymbopogon schoenanthus oil":"lemongrass oil", "lavender essential oil":"lavender oil", "lavandula angustifolia oil":"lavender oil",
    "mentha piperita oil":"peppermint oil", "melaleuca alternifolia leaf oil":"tea tree oil", "tto":"tea tree oil"
}

# INGREDIENT GROUPING
# group ingredients if they affect the skin in a similar manner
grouped_ingred={
    "ethanol":"drying_alcohol", "alcohol denat":"drying_alcohol", "isopropyl alcohol":"drying_alcohol","lemon oil":"irritant_fragrance",
     "fragrance":"irritant_fragrance", "orange oil":"irritant_fragrance", "bergamot oil":"irritant_fragrance",
    "cinnamon bark oil":"irritant_fragrance", "clove oil":"irritant_fragrance", "lemongrass oil":"irritant_fragrance",
    "lavender oil":"irritant_fragrance", "peppermint oil":"irritant_fragrance", "tea tree oil":"irritant_fragrance",
    "benzyl alcohol":"irritant_fragrance", "salicylic acid":"bha", "glycolic acid":"aha", "lactic acid":"aha", "mandelic acid":"aha",
    "sles":"mild_surfactant", "sls":"harsh_surfactant", "coconut oil":"highly_comedogenic", "cocoa butter":"highly_comedogenic",
    "isopropyl myristate":"highly_comedogenic", "lauric acid":"highly_comedogenic", "wheat germ oil":"highly_comedogenic",
    "lanolin":"mildly_comedogenic", "acetylated lanolin":"mildly_comedogenic", "ethoxylated lanolin":"mildly_comedogenic",
    "myristyl myristate":"highly_comedogenic", "ethylhexyl palmitate":"moderately_comedogenic", "ethylhexyl stearate":"moderately_comedogenic",
    "shea butter":"mildly_comedogenic", "lauric acid":"highly_comedogenic", "butyl stearate":"moderately_comedogenic",
    "benzoyl peroxide":"drying_active", "retinal":"irritating_active", "isopropyl palmitate":"moderately_comedogenic", 
}


# SKIN TYPE PENALTY SCORE
# negative scores are used to penalise ingredients which would harm/not benefit the skin, this is dependent on skin type
skin_type_score={
    "mildly_comedogenic":{"dry":0,"oily":-1,"sensitive":0,"normal":0},
    "moderately_comedogenic":{"dry":0,"oily":-2,"sensitive":-1,"normal":0},
    "highly_comedogenic":{"dry":0,"oily":-3,"sensitive":-2,"normal":-1},
    "aha":{"dry":0,"oily":0,"sensitive":-2,"normal":0},
    "irritating_active":{"dry":-1,"oily":0,"sensitive":-2,"normal":0},
    "irritant_fragrance":{"dry":-2,"oily":-1,"sensitive":-3,"normal":0},
    "drying_alcohol":{"dry":-3,"oily":-1,"sensitive":-2,"normal":0},
    "bha":{"dry":-1,"oily":0,"sensitive":-2,"normal":0},
    "mild_surfactant":{"dry":-1,"oily":0,"sensitive":-1,"normal":0},
    "harsh_surfactant":{"dry":-3,"oily":-1,"sensitive":-3,"normal":0},
    "drying_active":{"dry":-3,"oily":0,"sensitive":-2,"normal":0},
}


# CONCERN SCORE FUNCTION
# this function creates a dictionary, mapping each ingredient to a score for each skin concern
def concern_score(ingredients_df):
    # extracting ingredients based on desciptions from 'who_is_it_good_for' column
    acne_text="acne|blackheads|texture|enlarged pores"
    dehydration_text="dry and dehydrated skin|impaired skin barrier"
    aging_text="fine lines|wrinkles|elasticity"
    redness_text="redness|impaired skin barrier"
    dullness_text="radiance|texture|pigmentation|post blemish marks|dark circles"

    # scoring beneficial ingredients for each skin concern
    ingredients_df.loc[ingredients_df["who_is_it_good_for"].str.contains(acne_text),"acne"]=1
    ingredients_df.loc[ingredients_df["who_is_it_good_for"].str.contains(dehydration_text),"dehydration"]=1
    ingredients_df.loc[ingredients_df["who_is_it_good_for"].str.contains(aging_text),"aging"]=1
    ingredients_df.loc[ingredients_df["who_is_it_good_for"].str.contains(redness_text),"redness"]=1
    ingredients_df.loc[ingredients_df["who_is_it_good_for"].str.contains(dullness_text),"dullness"]=1

    # Score key ingredients (extremely benificial for skin concern) 
    # ACNE:
    acne_data={"name":["retinoid","tretinoin","adapelene","benzoyl peroxide","salicylic acid","azelaic acid","glycolic acid","niacinimide","sulfur","kaolin clay","zinc","tea tree oil"],
                "acne":[3,3,3,3,2,2,2,2,2,2,2,2]
                }
    acne_df=pd.DataFrame(acne_data)

    # get ingredients that have already flagged by the CSV file (ie score=1)
    acne_rows=ingredients_df.loc[ingredients_df["acne"]==1]
    acne_rows=acne_rows[["name","acne"]]

    # Combine: manual scores (2/3) take priority, then CSV scores (1) fill out the rest
    acne_df2=acne_df.combine_first(acne_rows)

    # DEHYDRATION:
    dehydration_data={"name": ["hyaluronic acid","glycerin","peptide","ceramide","panthenol","squalane","shea butter","butylene","ectoin","lactic acid"],
                        "dehydration":[3,3,3,3,2,2,2,2,2,2]
                        }
    dehydration_df=pd.DataFrame(dehydration_data)
    dehydration_rows=ingredients_df.loc[ingredients_df["dehydration"]==1]
    dehydration_rows=dehydration_rows[["name","dehydration"]]
    dehydration_df2=dehydration_df.combine_first(dehydration_rows)

    # AGING:
    aging_data={"name": ["retinoid","vitamin c","peptide","growth factor","bakuchiol","lactic acid","niacinimide","glycolic acid","hyaluronic acid","ceramide"],
                "aging":[3,3,3,3,3,2,2,2,2,2]
                }
    aging_df=pd.DataFrame(aging_data)
    aging_rows=ingredients_df.loc[ingredients_df["aging"]==1]
    aging_rows=aging_rows[["name","aging"]]
    aging_df2=aging_df.combine_first(aging_rows)

    # REDNESS:
    redness_data={"name": ["azelaic acid","colloidal oatmeal","centella asiatica","niacinimide","alpha arbutin","ceramide","aloe vera","sulfur","panthenol","hyaluronic acid"],
                  "redness":[3,3,3,3,2,2,2,2,2,2]
                  }
    redness_df=pd.DataFrame(redness_data)
    redness_rows=ingredients_df.loc[ingredients_df["redness"]==1]
    redness_rows=redness_rows[["name","redness"]]
    redness_df2=redness_df.combine_first(redness_rows)

    # DULLNESS:
    dullness_data={"name": ["vitamin c","niacinimide","retinoid","bakuchiol","ferulic acid","lactic acid","glycolic acid","hyaluronic acid","resveratrol","vitamin e"],
                   "dullness":[3,3,3,3,3,2,2,2,2,2]}
    dullness_df=pd.DataFrame(dullness_data)
    dullness_rows=ingredients_df.loc[ingredients_df["dullness"]==1]
    dullness_rows=dullness_rows[["name","dullness"]]
    dullness_df2=dullness_df.combine_first(dullness_rows)

    #merge all dataframes with skin concern scoring into one dataframe
    merged_df=pd.merge(acne_df2,dehydration_df2,on='name',how='outer')
    merged_df=pd.merge(merged_df,aging_df2,on='name',how='outer')
    merged_df=pd.merge(merged_df,redness_df2,on='name',how='outer')
    merged_df=pd.merge(merged_df,dullness_df2,on='name',how='outer')

    # replace all nans in df with 0
    merged_df=merged_df.fillna(0)

    # keep only the highest score per ingredient, for each skin concern
    for col in ['acne', 'dehydration', 'aging', 'redness', 'dullness']:
        merged_df = merged_df.sort_values(col, ascending=False).drop_duplicates('name').sort_index()

    # convert dataframe with scores into nested dictionary
    # e.g. {'ingredient name':{'acne':2}, etc}
    skin_concern_score=merged_df.set_index('name').to_dict(orient='index')

    return skin_concern_score

# SCORING FUNCTION
# calculates a product's score based on ingredient penalties (skin type) and rewards (skin concern)
# the total is normalised by the number of scored ingredients (any ingredient with a non-zero score)
# this is applied to every row in the DataFrame
def scoring_func(ingredients_list,skin_type,skin_concern,skin_concern_score):
    total=0
    scored_count=0
    bad_ingredients=[]
    good_ingredients=[]
    for i in ingredients_list:
        i=i.strip()
        i=standard_ingred.get(i,i)
        group=grouped_ingred.get(i,i)
        penalty=skin_type_score.get(group,{}).get(skin_type,0)
        reward=skin_concern_score.get(i,{}).get(skin_concern,0)
        if penalty!=0 or reward!=0:
            scored_count+=1
        if penalty<=-2:
            bad_ingredients.append(i)
        if reward>=2:
            good_ingredients.append(i)
        total+=penalty+reward

    if scored_count>0:
        total=total/scored_count
    return total, scored_count, bad_ingredients, good_ingredients