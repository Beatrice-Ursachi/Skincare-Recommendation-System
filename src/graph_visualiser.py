import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

# adjust plot spacing
plt.rcParams['figure.constrained_layout.use'] = True

# function that will create bar chart for ingredients that scored +2/+3
def plot_top_good_ingredients(result):
    good_ingred=[]
    for i in result['good_ingredients']:
        good_ingred+=i
    # check to prevent errors when no good ingredients are found
    if len(good_ingred) == 0:
        print("No good ingredients found. Graph has not been created.")
        return
    
    # count the frequency of each ingredient
    counts = pd.Series(good_ingred).value_counts()

    # use green gradient for bar chart
    n = len(counts)
    colors = cm.Greens_r(np.linspace(0.3, 0.9, n))

    plt.figure(figsize=(12, 6))
    counts.plot(kind='bar',color=colors, edgecolor='black')
    plt.title('Top Good Ingredients',fontsize=15, fontweight='bold')
    plt.xlabel('Ingredient',fontsize=12)
    plt.ylabel('Frequency',fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig('../graphs/plot_top_good_ingredients.png')
    plt.close()

# function that will create bar chart for ingredients that scored -2/-3
def plot_top_bad_ingredients(result):
    bad_ingred=[]
    for i in result['bad_ingredients']:
        bad_ingred+=i
    # check to prevent errors when no bad ingredients are found
    if len(bad_ingred) == 0:
        print("No bad ingredients found. Graph has not been created")
        return

    # count the frequency of each ingredient
    counts = pd.Series(bad_ingred).value_counts()

    # use red gradient for the bar chart
    n = len(counts)
    colors = cm.Reds_r(np.linspace(0.3, 0.9, n))

    plt.figure(figsize=(12, 6))
    counts.plot(kind='bar',color=colors, edgecolor='black')
    plt.title('Top Bad Ingredients',fontsize=15, fontweight='bold')
    plt.xlabel('Ingredient',fontsize=12)
    plt.ylabel('Frequency',fontsize=12)
    plt.xticks(rotation=45)
    plt.savefig('../graphs/plot_top_bad_ingredients.png')
    plt.close()

# function that plots distribution of product scores
def plot_score_distribution(product_df1):
    plt.figure(figsize=(12, 6))
    plt.hist(product_df1['score'], color='#06C2AC',bins=20)
    plt.title('Distribution of Product Scores',fontsize=15, fontweight='bold')
    plt.xlabel('Score',fontsize=12)
    plt.ylabel('No. Products',fontsize=12)
    plt.savefig('../graphs/plot_score_distribution.png')
    plt.close()

# function that creates scatterplot of product score, against the number of scored ingredients
def plot_score_vs_counts(product_df1):
    # check to prevent errors if product_df1 is empty
    if len(product_df1)==0:
        print("No data to plot")
        return
    plt.figure(figsize=(12, 6))
    plt.scatter(product_df1['scored_count'],product_df1['score'],color=	'#2C3E50')
    plt.title('Scatterplot: Score vs No. Scored Ingredients',fontsize=15, fontweight='bold')
    plt.xlabel('Number of Scored Ingredients',fontsize=12)
    plt.ylabel('Score',fontsize=12)
    plt.savefig('../graphs/plot_score_vs_counts.png')
    plt.close()