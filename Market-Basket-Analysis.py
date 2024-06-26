# -*- coding: utf-8 -*-
"""SEM6_PROJECT(IU2141050174).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yji04m43mofnsP1L7XBkARQkbsszwu0O

Market Basket Analysis is a data-driven technique used to uncover patterns and relationships within large transactional datasets, particularly in retail and e-commerce. It helps businesses understand which products or items are often purchased together, providing insights for optimizing product placement, marketing strategies, and promotions.
"""

import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_white"

data = pd.read_csv("market_basket_dataset.csv")
print(data.head())

print(data.isnull().sum())

#summary statistics of this dataset:
print(data.describe())

"""1.   Gather transactional data, including purchase history, shopping carts, or invoices.
Analyze product sales and trends.
2.Use algorithms like Apriori or FP-growth to discover frequent item sets and generate association rules.
3.Interpret the discovered association rules to gain actionable insights.
4.Develop strategies based on the insights gained from the analysis.

**the sales distribution of items:**
"""

fig = px.histogram(data, x='Itemname',
                   title='Item Distribution')
fig.show()

"""The top 10 most popular items sold by the store:
Key Concepts<br>
1.Grouping Data: The code uses the groupby function to group the data by the item name and then calculates the sum of quantities sold for each item.<br>
2.Sorting: The sort_values function is used to sort the items based on the total quantity sold in descending order.<br>
3.Plotting: The code utilizes the plotly library to create an interactive bar chart that displays the top N most popular items based on sales quantity.
"""

x=item_popularity.index[:top_n]item_popularity = data.groupby('Itemname')['Quantity'].sum().sort_values(ascending=False)# Calculate item popularity
item_popularity = data.groupby('Itemname')['Quantity'].sum().sort_values(ascending=False)

top_n = 10
fig = go.Figure()
fig.add_trace(go.Bar(x=item_popularity.index[:top_n], y=item_popularity.values[:top_n],
                     text=item_popularity.values[:top_n], textposition='auto',
                     marker=dict(color='skyblue')))
fig.update_layout(title=f'Top {top_n} Most Popular Items',
                  xaxis_title='Item Name', yaxis_title='Total Quantity Sold')
fig.show()

"""let’s have a look at the customer behaviour:


1.   The agg() method allows you to apply a function or a list of function names to be executed along one of the axis of the DataFrame,


"""

# Calculate average quantity and spending per customer
customer_behavior = data.groupby('CustomerID').agg({'Quantity': 'mean', 'Price': 'sum'}).reset_index()

# Create a DataFrame to display the values
table_data = pd.DataFrame({
    'CustomerID': customer_behavior['CustomerID'],
    'Average Quantity': customer_behavior['Quantity'],
    'Total Spending': customer_behavior['Price']
})

# Create a subplot with a scatter plot and a table
fig = go.Figure()

# Add a scatter plot
fig.add_trace(go.Scatter(x=customer_behavior['Quantity'], y=customer_behavior['Price'],
                         mode='markers', text=customer_behavior['CustomerID'],
                         marker=dict(size=10, color='coral')))

# Add a table
fig.add_trace(go.Table(
    header=dict(values=['CustomerID', 'Average Quantity', 'Total Spending']),
    cells=dict(values=[table_data['CustomerID'], table_data['Average Quantity'], table_data['Total Spending']]),
))

# Update layout
fig.update_layout(title='Customer Behavior',
                  xaxis_title='Average Quantity', yaxis_title='Total Spending')

# Show the plot
fig.show()

""" Apriori algorithm to create association rules. The Apriori algorithm is used to discover frequent item sets in large transactional datasets. It aims to identify items that are frequently purchased together in transactional data.
  

*  It helps uncover patterns in custome behaviour, allowing businesses to make informed decisions about product placement, promotions, and marketing. Here’s how to implement Apriori to generate association rules:
"""

from mlxtend.frequent_patterns import apriori, association_rules

# Group items by BillNo and create a list of items for each bill
basket = data.groupby('BillNo')['Itemname'].apply(list).reset_index()

# Encode items as binary variables using one-hot encoding
# Next, one-hot encoding is used to convert the list of items into binary variables.
basket_encoded = basket['Itemname'].str.join('|').str.get_dummies('|')

# Find frequent itemsets using Apriori algorithm with lower support
frequent_itemsets = apriori(basket_encoded, min_support=0.01, use_colnames=True)

# Generate association rules with lower lift threshold
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=0.5)

# Display association rules
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

"""The above output shows association rules between different items (antecedents) and the items that tend to be purchased together with them (consequents). Let’s interpret the output step by step:

Antecedents: These are the items that are considered as the starting point or “if” part of the association rule. For example, Bread, Butter, Cereal, Cheese, and Chicken are the antecedents in this analysis.
Consequents: These are the items that tend to be purchased along with the antecedents or the “then” part of the association rule.
Support: Support measures how frequently a particular combination of items (both antecedents and consequents) appears in the dataset. It is essentially the proportion of transactions in which the items are bought together. For example, the first rule indicates that Bread and Apples are bought together in approximately 4.58% of all transactions.
Confidence: Confidence quantifies the likelihood of the consequent item being purchased when the antecedent item is already in the basket. In other words, it shows the probability of buying the consequent item when the antecedent item is bought. For example, the first rule tells us that there is a 30.43% chance of buying Apples when Bread is already in the basket.
Lift: Lift measures the degree of association between the antecedent and consequent items, while considering the baseline purchase probability of the consequent item. A lift value greater than 1 indicates a positive association, meaning that the items are more likely to be bought together than independently. A value less than 1 indicates a negative association. For example, the first rule has a lift of approximately 1.86, suggesting a positive association between Bread and Apples.
"""