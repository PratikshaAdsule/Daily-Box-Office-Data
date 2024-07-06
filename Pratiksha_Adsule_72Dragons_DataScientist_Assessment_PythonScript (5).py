#!/usr/bin/env python
# coding: utf-8

# ## Project Title
# Web Data Scraping, Storage, and Visualization Using Python
# 
# ## Project Objective
# The objective of this project is to demonstrate the ability to scrape data from a selected website, save the data into a CSV file and a database, and generate visualizations using Plotly. The steps include:
# 1. Selecting a data site (e.g., box office data, population analytics, health analytics).
# 2. Writing a Python script to scrape data from the site.
# 3. Saving the scraped data into a CSV file.
# 4. Storing the scraped data in a database.
# 5. Creating at least three visualizations (HTML, PDF, or PNG) using Plotly.
# 
# This project aims to showcase proficiency in web scraping, data manipulation, database management, and data visualization.
# 

# ## Daily Box Office Data

# In[36]:


##Install required libraries


# In[37]:


pip install requests beautifulsoup4 pandas plotly


# In[39]:


#Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Step 1: Scrape Data
def scrape_data():
    url = 'https://www.boxofficemojo.com/daily/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    headers = [header.text.strip() for header in table.find_all('th')]
    data = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) == len(headers):  # Ensure row has the correct number of columns
            data.append([cell.text.strip() for cell in cells])

    df = pd.DataFrame(data, columns=headers)
    return df

# Step 2: Save Data into CSV
def save_to_csv(df):
    df.to_csv('C:/Users/Prashant/Pratiksha_Adsule_72Dragons_DataScientist_daily_boxoffice_data.csv', index=False)

# Step 3: Save Data into SQLite Database
def save_to_sqlite(df):
    conn = sqlite3.connect('C:/Users/Prashant/boxoffice_data.db')
    df.to_sql('boxoffice', conn, if_exists='replace', index=False)
    conn.close()

# Step 4: Generate Visualizations and Save as HTML
def generate_visualizations(df):
    # Selecting and renaming relevant columns for analysis
    df = df[['#1 Release', 'Gross', 'Top 10 Gross', 'Releases']].copy()
    df.columns = ['Title', 'Daily Gross', 'Total Gross to Date', 'Theaters']

    # Convert columns to appropriate data types
    df['Daily Gross'] = df['Daily Gross'].str.replace('[\$,]', '', regex=True).astype(float)
    df['Total Gross to Date'] = df['Total Gross to Date'].str.replace('[\$,]', '', regex=True).astype(float)
    df['Theaters'] = df['Theaters'].str.replace(',', '').astype(int)

    # Sort the dataframe by 'Total Gross to Date' in descending order
    df_sorted_total_gross = df.sort_values(by='Total Gross to Date', ascending=False)
    fig1 = px.bar(df_sorted_total_gross, x='Title', y='Total Gross to Date', title='Total Gross by Movie', color_discrete_sequence=['blue'])
    fig1.update_layout(xaxis={'categoryorder':'total descending'}, width=1200, height=800)

    # Sort the dataframe by 'Daily Gross' in descending order
    df_sorted_daily_gross = df.sort_values(by='Daily Gross', ascending=False)
    fig2 = px.bar(df_sorted_daily_gross, x='Title', y='Daily Gross', title='Daily Gross by Movie', color_discrete_sequence=['green'])
    fig2.update_layout(xaxis={'categoryorder':'total descending'}, width=1200, height=800)

    # Sort the dataframe by 'Theaters' in descending order
    df_sorted_theaters = df.sort_values(by='Theaters', ascending=False)
    fig3 = px.bar(df_sorted_theaters, x='Title', y='Theaters', title='Number of Theaters by Movie', color_discrete_sequence=['orange'])
    fig3.update_layout(xaxis={'categoryorder':'total descending'}, width=1200, height=800)

    # Save figures as HTML files
    fig1.write_html("C:/Users/Prashant/Pratiksha_Adsule_72Dragons_DataScientist_Total_Gross_by_Movie_Graph1.html")
    fig2.write_html("C:/Users/Prashant/Pratiksha_Adsule_72Dragons_DataScientist_Daily_Gross_by_Movie_Graph2.html")
    fig3.write_html("C:/Users/Prashant/Pratiksha_Adsule_72Dragons_DataScientist_Number_of_Theatres_by_Movie_Graph3.html")

    fig1.show()
    fig2.show()
    fig3.show()


def main():
    df = scrape_data()
    save_to_csv(df)
    save_to_sqlite(df)
    generate_visualizations(df)

if __name__ == "__main__":
    main()

# Convert SQLite database to SQL file
get_ipython().system('sqlite3 C:/Users/Prashant/boxoffice_data.db .dump > C:/Users/Prashant/Pratiksha_Adsule_72Dragons_DataScientist_boxoffice_data.sql')


# ## Insights from Data Visualizations
# 
# ### 1. Impact of Limited Distribution
# - Movies like **"The Chosen: S4 Episodes 1-3," "A Quiet Place: Day One," "Abigail," "Demon Slayer: Kimetsu No Yaiba-To the Hashira Training,"** and **"Night Swim"** were shown in the fewest theaters, leading to the lowest daily and total gross, indicating that limited distribution directly impacts overall box office performance.
# 
# ### 2. Benefits of Extensive Distribution
# - Conversely, movies like **"Inside Out 2," "Dune: Part Two,"** and **"Godzilla x Kong: The New Empire"** had the highest number of theaters and achieved the highest daily and total gross, demonstrating that extensive distribution significantly boosts box office performance.
# 
# ### 3. Importance of Audience Appeal
# - **"The Beekeeper"** and **"Challengers"** had a moderate number of theaters yet exhibited low daily and total gross, while **"Kung Fu Panda 4"** and **"Bad Boys: Ride or Die"** achieved higher gross despite fewer theaters. This highlights that audience appeal and engagement are crucial for box office success beyond just distribution reach.
# 
# ### 4. Balanced Distribution and Performance
# - Movies like **"Kingdom of the Planet of the Apes," "Wonka," "The Garfield Movie," "Ghostbusters: Frozen Empire,"** and **"IF"** have a moderate number of theaters and also moderate total and daily gross, indicating a balanced relationship between distribution reach and box office performance.
# 
# These insights underscore the importance of both wide distribution and strong audience engagement for achieving successful box office outcomes.
# 

# ## Summary
# 
# In this project, I successfully demonstrated the ability to:
# 
# 1. **Scrape Data from a Website**: Using the BeautifulSoup library, I extracted data from a chosen website.
#    - **Source data site link**: https://www.boxofficemojo.com/daily/
#    
# 2. **Save Data to CSV**: The scraped data was saved into a CSV file using the Pandas library, ensuring the data is structured and easily accessible.
#    - **CSV File**: Pratiksha_Adsule_72Dragons_DataScientist_daily_boxoffice_data.csv
#    
# 3. **Store Data in a Database**: The data was then stored in an SQLite database, showcasing my ability to manage and query data effectively.
#    - **SQL File**: Pratiksha_Adsule_72Dragons_DataScientist_boxoffice_data.sql
#    
# 4. **Generate Visualizations with Plotly**: Using Plotly, I created three insightful visualizations, which were saved as HTML files.
#    - **All created graphs**:
#      - Pratiksha_Adsule_72Dragons_DataScientist_Total_Gross_by_Movie_Graph1.html
#      - Pratiksha_Adsule_72Dragons_DataScientist_Daily_Gross_by_Movie_Graph2.html
#      - Pratiksha_Adsule_72Dragons_DataScientist_Number_of_Theatres_by_Movie_Graph3.html
# 
# Through this project, I demonstrated proficiency in web scraping, data manipulation, database management, and data visualization, highlighting my ability to handle end-to-end data processing tasks. This comprehensive approach ensures that the data is not only collected and stored efficiently but also analyzed and visualized in a meaningful way to derive insights.

# In[ ]:




