# -*- coding: utf-8 -*-
"""ua_wrokbook.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ld_CZ8yp6WdOR8UVi0P3t9cCyqInIeHD

# 0. data loading

"DataSet_1" is set as "df1";
"DataSet_2_SKAN" is set as "df2"
"""

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

# Load the datasets
file_path1 = 'Dataset1.csv'
file_path2 = 'Dataset2.csv'

df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

"""# Part 1: Data Preparation

## 1.1: Explore the raw dataset
"""

# inspect the first few rows and get a general understanding of the data structure
df1.head()

df2.head()

"""# 1.2 Check Data Type"""

# data info of df1
df1.info()

# corret data type of df1
df1['Spend'] = pd.to_numeric(df1['Spend'], errors='coerce')
df1['Impressions'] = pd.to_numeric(df1['Impressions'], errors='coerce')
df1['Clicks'] = pd.to_numeric(df1['Clicks'], errors='coerce')
df1['Installs'] = pd.to_numeric(df1['Installs'], errors='coerce')
df1['ROAS D1'] = pd.to_numeric(df1['ROAS D1'], errors='coerce')
df1['ROAS D3'] = pd.to_numeric(df1['ROAS D3'], errors='coerce')
df1['ROAS D7'] = pd.to_numeric(df1['ROAS D7'], errors='coerce')
df1['Revenue D365 (predicted)'] = pd.to_numeric(df1['Revenue D365 (predicted)'], errors='coerce')
df1['Retention D1'] = pd.to_numeric(df1['Retention D1'], errors='coerce')
df1['Retention D7'] = pd.to_numeric(df1['Retention D7'], errors='coerce')
df1['IAP NET Revenue'] = pd.to_numeric(df1['IAP NET Revenue'], errors='coerce')
df1['Ad NET Revenue'] = pd.to_numeric(df1['Ad NET Revenue'], errors='coerce')
df1['CR%_payer_d1'] = pd.to_numeric(df1['CR%_payer_d1'], errors='coerce')
df1['Date'] = pd.to_datetime(df1['Date'], errors='coerce')

# check missing values of df1
missing_values1 = df1.isnull().sum()
print(missing_values1)

# replace missing value with 0
df1.fillna(0, inplace=True)

print(df1.isnull().sum())

# check if the replace is successful
df1.head(10)

# data info of df2
df2.info()

# corret data type of df2
df2['Spend'] = pd.to_numeric(df2['Spend'], errors='coerce')
df2['Impressions'] = pd.to_numeric(df2['Impressions'], errors='coerce')
df2['Clicks'] = pd.to_numeric(df2['Clicks'], errors='coerce')
df2['SKAN CPI'] = pd.to_numeric(df2['SKAN CPI'], errors='coerce')
df2['m_ROAS D1'] = pd.to_numeric(df2['m_ROAS D1'], errors='coerce')
df2['m_ROAS D7'] = pd.to_numeric(df2['m_ROAS D7'], errors='coerce')
df2['SKAN Postbacks D2 (retention)'] = pd.to_numeric(df2['SKAN Postbacks D2 (retention)'], errors='coerce')
df2['Date'] = pd.to_datetime(df2['Date'], errors='coerce')

# check missing values of df2
missing_values2 = df2.isnull().sum()
print(missing_values2)

# replace missing value with 0
df2.fillna(0, inplace=True)

print(df2.isnull().sum())

# check if the replace is successful
df2.head(10)

"""# 1.3: Categorize campaign based on Campaign_Name

## 1.3.1 Dataset1
First split dataset1 into 3 subset
*   Organic search
*   US_brand
*   Normal (media source): Facebook, TikTok, Googke, APS
"""

# split dataset
df1_organic = df1[df1['Campaign_Name'].str.contains('Organic')]
df1_brand = df1[df1['Campaign_Name'].str.contains('US - Brand')]
df1_normal = df1[~df1.index.isin(df1_organic.index) & ~df1.index.isin(df1_brand.index)]

# used to check the splited dataset

#df1_organic.head()
#df1_brand.head()
#df1_normal.head()

"""Identify media source and OS for each campaign"""

# feature engineering for df1_organic
df1_organic.loc[:, 'media_source'] = df1_organic['Campaign_Name'].apply(lambda x: x.split(': ')[0])
df1_organic.loc[:, 'OS'] = df1_organic['Campaign_Name'].apply(lambda x: x.split(': ')[1])

"""Format consistency"""

# clean dataset - ensure OS format consistency between df1_organic and df1_normal
df1_organic['OS'] = df1_organic['OS'].replace('ios', 'iOS')
df1_organic['OS'] = df1_organic['OS'].replace('android', 'Android')

df1_organic.head()

# feature engineering for df_normal
df1_normal['media_source'] = df1_normal['Campaign_Name'].apply(lambda x: x.split('_')[0])
df1_normal['OS'] = df1_normal['Campaign_Name'].apply(lambda x: x.split('_')[1])

# clean dataset - ensure media_source format consistency
df1_normal['media_source'] = df1_normal['media_source'].replace('Tiktok', 'TikTok')

df1_normal.head()

# @title media_source

from matplotlib import pyplot as plt
import seaborn as sns
df1_normal.groupby('media_source').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

"""## 1.3.2 Dataset2"""

# clean dataset - Filter out rows where Campaign_Name starts with "ios" or "iOS"
## The rows with Campaign_Name starting with "ios" or "iOS" were removed
## because they do not specify which platform the campaign is targeting
## Additionally, these rows contained significant missing data, reducing their usefulness for analysis.
## By removing these rows, the dataset becomes more focused and accurate for platform-specific campaign analysis

df2_filtered = df2[~df2['Campaign_Name'].str.lower().str.startswith('ios')]

# Identify media source
df2_filtered['media_source'] = df2_filtered['Campaign_Name'].apply(lambda x: x.split('_')[0])

# clean dataset - ensure media_source format consistency
df2_filtered['media_source'] = df2_filtered['media_source'].replace('Tiktok', 'TikTok')

df2_filtered.head(10)

# df2_filtered.to_csv('df2_filtered.csv', index=False)

# @title media_source

from matplotlib import pyplot as plt
import seaborn as sns
df2_filtered.groupby('media_source').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

"""# Part 2: User Acquisition Analysis

# 2.1: Describe and Summarize Available Data
Provide an overview of the data in "DataSet_1" and "DataSet_2_SKAN." What insights can you gather about Highrise user acquisition from this data?
"""

df1.describe()

columns_of_interest = ['Date', 'Spend', 'Impressions', 'Clicks', 'Installs', 'ROAS D1', 'ROAS D3', 'ROAS D7','Revenue D365 (predicted)', 'Retention D1', 'Retention D7']
df1[columns_of_interest].describe()

unique_values_count1 = df1.nunique()
unique_values_count1

unique_values_count1_normal = df1_normal.nunique()
unique_values_count1_normal

# To see the unique media sources in the dataset
unique_media_sources1 = df1_normal['media_source'].unique()

# Display the unique media sources
print(unique_media_sources1)

df2.describe()

# Get the result of df2.describe()
# description_df2 = df2.describe()

# Export descriptive statistics to a CSV file
# description_df2.to_csv('df2_description.csv')

unique_values_count2 = df2.nunique()
unique_values_count2

unique_values_count2_filtered = df2_filtered.nunique()
unique_values_count2_filtered

# To see the unique media sources in the dataset
unique_media_sources2 = df2_filtered['media_source'].unique()

# Display the unique media sources
print(unique_media_sources2)

# Visualization: Correlation Heatmap of Numerical Features
plt.figure(figsize=(10, 8))
correlation_matrix = df1.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap of Numerical Features')
plt.show()

plt.figure(figsize=(10, 8))
correlation_matrix2 = df2_filtered.corr(numeric_only=True)
sns.heatmap(correlation_matrix2, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap of Numerical Features')
plt.show()

# Media source compposition
# Define colors for each media source, ensuring consistency
media_source_colors = {
    'TikTok': '#66b3ff',  # Blue for TikTok
    'Google': '#ff9999',  # Red for Google
    'Facebook': '#8c564b',  # Brown for Facebook
    'ASA': '#ffcc99',  # Light orange for ASA
    'Unity': '#99ff99',  # Green for Unity
    'Highrise': '#c2c2f0'  # Light purple for Highrise
}

# Plot for df1_normal
df1_normal['media_source'].value_counts().plot(kind='pie',
                                               autopct='%1.1f%%',
                                               colors=[media_source_colors[label] for label in df1_normal['media_source'].value_counts().index],
                                               startangle=140,
                                               figsize=(8, 8))

plt.title('Media Source Composition')
plt.ylabel('')  # Removes the y-label
plt.show()

# Plot for df2_filtered
df2_filtered['media_source'].value_counts().plot(kind='pie',
                                                 autopct='%1.1f%%',
                                                 colors=[media_source_colors[label] for label in df2_filtered['media_source'].value_counts().index],
                                                 startangle=140,
                                                 figsize=(8, 8))

plt.title('Media Source Composition')
plt.ylabel('')  # Removes the y-label
plt.show()

import matplotlib.pyplot as plt

# Define consistent colors for each media source
media_source_colors = {
    'TikTok': '#66b3ff',  # Blue for TikTok
    'Google': '#ff9999',  # Red for Google
    'Facebook': '#8c564b',  # Brown for Facebook
    'ASA': '#ffcc99',  # Light orange for ASA
    'Unity': '#99ff99',  # Green for Unity
    'Highrise': '#c2c2f0'  # Light purple for Highrise
}

# Aggregate Ad NET Revenue by media_source for df1_normal
revenue_by_source = df1_normal.groupby('media_source')['Ad NET Revenue'].sum()

# Create a pie chart for df1_normal using the color dictionary
plt.figure(figsize=(8, 8))
plt.pie(revenue_by_source,
        labels=revenue_by_source.index,
        colors=[media_source_colors[label] for label in revenue_by_source.index],
        autopct='%1.1f%%', startangle=90)
plt.axis('equal')

# Display the first chart
plt.show()

# Aggregate predicted total net revenue by media_source for df2_filtered
revenue_by_source_df2 = df2_filtered.groupby('media_source')['pred_total_net_revenue_d365'].sum()

# Create a pie chart for df2_filtered using the color dictionary
plt.figure(figsize=(8, 8))
plt.pie(revenue_by_source_df2,
        labels=revenue_by_source_df2.index,
        colors=[media_source_colors[label] for label in revenue_by_source_df2.index],
        autopct='%1.1f%%', startangle=90)
plt.title(' Revenue Share by Media Source (df2_filtered)')
plt.axis('equal')

# Display the second chart
plt.show()

# Visualization: Distribution of Installs across Campaigns
plt.figure(figsize=(12, 6))
sns.boxplot(x='media_source', y='Installs', data=df1_normal)
plt.xticks(rotation=90)
plt.title('Distribution of Installs across Media Source')
plt.xlabel('Media Source')
plt.ylabel('Installs')
plt.grid(True)
plt.show()

"""# 2.2 Analyze Media Source Performance
Summarize the performance of various media sources. Identify any trends or patterns you observe. Include your comments and conclusions based on this analysis.

# 2.2.1 Dataset 1
"""

# df1_normal.to_csv('df1_normal.csv', index=False)

# Creating a dataframe with the required calculations by media source
media_source_metrics1 = df1_normal.groupby('media_source').agg({
    'Spend': 'sum',
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Installs': 'sum',
    'ROAS D1': 'mean',
    'ROAS D3': 'mean',
    'ROAS D7': 'mean',
    'Retention D1': 'mean',
    'Retention D7': 'mean'
}).reset_index()

# Calculating additional metrics
media_source_metrics1['Cost per Mile (CPM)'] = media_source_metrics1['Spend'] / (media_source_metrics1['Impressions'] / 1000)
media_source_metrics1['Cost per Click (CPC)'] = media_source_metrics1['Spend'] / media_source_metrics1['Clicks']
media_source_metrics1['Cost per Install (CPI)'] = media_source_metrics1['Spend'] / media_source_metrics1['Installs']

# Renaming columns for clarity
media_source_metrics1.rename(columns={
    'ROAS D1': 'Average ROAS D1',
    'ROAS D3': 'Average ROAS D3',
    'ROAS D7': 'Average ROAS D7',
    'Retention D1': 'Average Retention D1',
    'Retention D7': 'Average Retention D7'
}, inplace=True)

# Display the resulting dataframe
media_source_metrics1.head()

# download media_source_metrics1
# media_source_metrics1.to_csv('media_source_metrics1.csv', index=False)

# Preparing data for plotting
media_sources1 = media_source_metrics1['media_source']
roas_d1 = media_source_metrics1['Average ROAS D1']
roas_d3 = media_source_metrics1['Average ROAS D3']
roas_d7 = media_source_metrics1['Average ROAS D7']

# Adjusting the colors and modifying the y-axis label and values
colors = ['orange', 'red', 'green', 'blue']

# Creating the overlay line chart with specified colors and percentage conversion
plt.figure(figsize=(10, 6))

for index, media_source_metrics1 in enumerate(media_sources1):
    plt.plot(['ROAS D1', 'ROAS D3', 'ROAS D7'],
             [roas_d1.iloc[index] * 100, roas_d3.iloc[index] * 100, roas_d7.iloc[index] * 100],
             marker='o', label=media_sources1, color=colors[index])

plt.title('Overlay Chart of ROAS by Media Source')
plt.xlabel('ROAS Time Period')
plt.ylabel('Percentage (%)')
plt.legend(title='Media Source')
plt.grid(True)
plt.show()

# Creating a dataframe with the required calculations by media source
media_source_metrics1 = df1_normal.groupby('media_source').agg({
    'Spend': 'sum',
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Installs': 'sum',
    'ROAS D1': 'mean',
    'ROAS D3': 'mean',
    'ROAS D7': 'mean',
    'Retention D1': 'mean',
    'Retention D7': 'mean'
}).reset_index()

# Calculating additional metrics
media_source_metrics1['Cost per Mile (CPM)'] = media_source_metrics1['Spend'] / (media_source_metrics1['Impressions'] / 1000)
media_source_metrics1['Cost per Click (CPC)'] = media_source_metrics1['Spend'] / media_source_metrics1['Clicks']
media_source_metrics1['Cost per Install (CPI)'] = media_source_metrics1['Spend'] / media_source_metrics1['Installs']

# Renaming columns for clarity
media_source_metrics1.rename(columns={
    'ROAS D1': 'Average ROAS D1',
    'ROAS D3': 'Average ROAS D3',
    'ROAS D7': 'Average ROAS D7',
    'Retention D1': 'Average Retention D1',
    'Retention D7': 'Average Retention D7'
}, inplace=True)

# Preparing data for plotting the Average Retention overlay chart
average_retention_d1 = media_source_metrics1['Average Retention D1']
average_retention_d7 = media_source_metrics1['Average Retention D7']

# Creating the overlay line chart for Average Retention with specified colors and percentage conversion
plt.figure(figsize=(10, 6))

for index, media_source in enumerate(media_sources1):
    plt.plot(['Retention D1', 'Retention D7'],
             [average_retention_d1.iloc[index] * 100, average_retention_d7.iloc[index] * 100],
             marker='o', label=media_source, color=colors[index])

plt.title('Overlay Chart of Average Retention by Media Source')
plt.xlabel('Retention Time Period')
plt.ylabel('Percentage (%)')
plt.legend(title='Media Source')
plt.grid(True)
plt.show()

"""# 2.2.2 Dataset2

Observations and Trends:
TikTok has the largest reach in terms of impressions and clicks, with a lower average cost per install (CPI) compared to Facebook. However, its return on ad spend (ROAS) and retention are significantly lower, indicating that despite the volume, TikTok may not be driving as much revenue or user retention.
Facebook demonstrates a better retention rate and higher predicted net revenue over 365 days, despite a higher cost per install. This suggests that Facebook is driving more quality installs than TikTok.
Highrise and Unity are almost non-contributing, suggesting these platforms are either underutilized or ineffective for the campaigns analyzed.
Conclusion:
TikTok is successful in reaching a large audience at a relatively low cost but may need improvement in driving higher user engagement and returns. Facebook, on the other hand, while more expensive, generates more valuable users in terms of revenue and retention.
"""

# Creating a dataframe with the required calculations by media source
media_source_metrics2 = df2_filtered.groupby('media_source').agg({
    'Spend': 'sum',
    'Impressions': 'sum',
    'Clicks': 'sum',
    'SKAN Installs': 'sum',
    'SKAN CPI': 'mean',
    'm_ROAS D1': 'mean',
    'm_ROAS D7': 'mean',
    'pred_total_net_revenue_d365': 'sum',
    'SKAN Postbacks D2 (retention)': 'mean'
}).reset_index()

# Calculating additional metrics
media_source_metrics2['Cost per Mile (CPM)'] = media_source_metrics1['Spend'] / (media_source_metrics1['Impressions'] / 1000)
media_source_metrics2['Cost per Click (CPC)'] = media_source_metrics1['Spend'] / media_source_metrics1['Clicks']
media_source_metrics2['Cost per Install (CPI)'] = media_source_metrics1['Spend'] / media_source_metrics1['Installs']

# Renaming columns for clarity
media_source_metrics1.rename(columns={
    'ROAS D1': 'Average ROAS D1',
    'ROAS D3': 'Average ROAS D3',
    'ROAS D7': 'Average ROAS D7',
    'SKAN Postbacks D2 (retention)': 'Average Retention',
    'Retention D7': 'Average Retention D7'
}, inplace=True)

# Display the resulting dataframe
media_source_metrics2.head()

"""# 2.3: Evaluate the Largest Paid Media Source by App Installs
Focus on the media source with the highest number of app installs. Summarize the performance of individual campaigns within this source. Share your conclusions and insights.

## Dataset1

Google is the paid media source generating highest installs
"""

# Filter the dataset to include only rows where media_source is 'Google'
df1_google = df1_normal[df1_normal['media_source'] == 'Google']

# Display the first few rows of the filtered dataframe to confirm the selection
df1_google.head()

# Aggregate the data by 'Campaign_Name' within the 'Google' media source
df1_google_aggregated = df1_google.groupby('Campaign_Name').agg({
    'Spend': 'sum',
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Installs': 'sum',
    'ROAS D1': 'mean',
    'ROAS D3': 'mean',
    'ROAS D7': 'mean',
    'Revenue D365 (predicted)': 'sum',
    'Retention D1': 'mean',
    'Retention D7': 'mean',
    'IAP NET Revenue': 'sum',
    'Ad NET Revenue': 'sum',
    'CR%_payer_d1': 'mean'
}).reset_index()

# Adding calculated fields (if needed)
df1_google_aggregated['Cost per Mile (CPM)'] = df1_google_aggregated['Spend'] / (df1_google_aggregated['Impressions'] / 1000)
df1_google_aggregated['Cost per Click (CPC)'] = df1_google_aggregated['Spend'] / df1_google_aggregated['Clicks']
df1_google_aggregated['Cost per Install (CPI)'] = df1_google_aggregated['Spend'] / df1_google_aggregated['Installs']

df1_google_aggregated
# df1_google_aggregated.to_csv('df1_google_aggregated.csv', index=False)

import seaborn as sns
import numpy as np

# Select the columns to include in the heatmap
heatmap_data = df1_google_aggregated[['Campaign_Name', 'Cost per Mile (CPM)', 'Cost per Click (CPC)', 'Cost per Install (CPI)']]

# Set the Campaign_Name as the index
heatmap_data.set_index('Campaign_Name', inplace=True)

# Normalize the data for better visualization in the heatmap
# heatmap_data_normalized = heatmap_data.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', linewidths=.5)
plt.title('Heatmap of CPM, CPC, CPI by Campaign')
plt.show()

# Adding additional metrics for campaign efficiency
# ROI (Return on Investment) = Revenue D365 / Spend
df1_google_aggregated['ROI'] = df1_google_aggregated['Revenue D365 (predicted)'] / df1_google_aggregated['Spend']

# Efficiency Score: considering installs, ROAS D7, Retention D7, and ROI
df1_google_aggregated['Efficiency_Score'] = (
    (df1_google_aggregated['Installs'] / df1_google_aggregated['Installs'].max()) +
    (df1_google_aggregated['ROAS D7'] / df1_google_aggregated['ROAS D7'].max()) +
    (df1_google_aggregated['Retention D7'] / df1_google_aggregated['Retention D7'].max()) +
    (df1_google_aggregated['ROI'] / df1_google_aggregated['ROI'].max())
) / 4

# Sorting campaigns by the highest efficiency score
df1_google_aggregated_sorted = df1_google_aggregated.sort_values(by='Efficiency_Score', ascending=False)

df1_google_aggregated_sorted

df1_google_aggregated_sorted.to_csv('df1_google_aggregated_sorted.csv', index=False)

# Plotting the top 5 campaigns based on Efficiency Score
top_5_campaigns = df1_google_aggregated_sorted.head(5)

# Define colors for each campaign
colors = ['orange', 'green', 'blue', 'red', 'purple']

# Redrawing the plots without campaign names on the x-axis

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Installs
axs[0, 0].bar(top_5_campaigns['Campaign_Name'], top_5_campaigns['Installs'], color=colors)
axs[0, 0].set_title('Installs')
axs[0, 0].set_ylabel('Installs')
axs[0, 0].tick_params(axis='x', labelbottom=False)  # Remove x-axis labels



# ROAS D7
axs[0, 1].bar(top_5_campaigns['Campaign_Name'], top_5_campaigns['ROAS D7'], color=colors)
axs[0, 1].set_title('ROAS D7')
axs[0, 1].set_ylabel('ROAS D7')
axs[0, 1].tick_params(axis='x', labelbottom=False)  # Remove x-axis labels

# Retention D7
axs[1, 0].bar(top_5_campaigns['Campaign_Name'], top_5_campaigns['Retention D7'], color=colors)
axs[1, 0].set_title('Retention D7')
axs[1, 0].set_ylabel('Retention D7')
axs[1, 0].tick_params(axis='x', labelbottom=False)  # Remove x-axis labels

# ROI
axs[1, 1].bar(top_5_campaigns['Campaign_Name'], top_5_campaigns['ROI'], color=colors)
axs[1, 1].set_title('ROI')
axs[1, 1].set_ylabel('ROI')
axs[1, 1].tick_params(axis='x', labelbottom=False)  # Remove x-axis labels

# Creating a unified legend outside the subplots
fig.legend(top_5_campaigns, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.1), frameon=False)

plt.tight_layout()
plt.show()

"""# 2.4 Compare OS Performance (iOS vs. Android):

Reflect on the performance differences between iOS and Android. What trends or patterns do you notice? Draw any relevant conclusions.
"""

# Grouping the data by 'Platform' to compare key metrics
OS_comparison = df1_normal.groupby('OS').agg({
    'Spend': 'sum',
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Installs': 'sum',
    'ROAS D1': 'mean',
    'ROAS D3': 'mean',
    'ROAS D7': 'mean',
    'Retention D1': 'mean',
    'Retention D7': 'mean',
    'Revenue D365 (predicted)': 'sum',
    'IAP NET Revenue': 'mean',
    'Ad NET Revenue': 'mean',
    'CR%_payer_d1': 'mean'
}).reset_index()
platform_comparison

# OS_comparison.to_csv('OS_comparison.csv', index=False)

# Grouping the data by OS and calculating the average for relevant KPIs
kpi_columns = ['Spend', 'Impressions', 'Clicks', 'Installs', 'ROAS D1', 'ROAS D3', 'ROAS D7',
               'Revenue D365 (predicted)', 'Retention D1', 'Retention D7', 'IAP NET Revenue',
               'Ad NET Revenue', 'CR%_payer_d1']

os_performance = df.groupby('OS')[kpi_columns].mean().reset_index()

# @title OS

from matplotlib import pyplot as plt
import seaborn as sns
df1_normal.groupby('OS').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)