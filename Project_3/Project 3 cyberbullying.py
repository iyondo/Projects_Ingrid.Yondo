#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import sqlalchemy as db
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base


# In[3]:


project3=pd.read_excel(r'C:\Users\Ingrid\Desktop\DAFT Nov 21\Projects\Project 3\1 - cyberbullying_in_social_media.xlsx')


# In[4]:


project3.head()


# In[5]:


#briefly see what there is in the data
stat=project3.describe()
stat
#IsRetweet has 0 everywhere so can be deleted since it has no added value (will check for outliers later on, first missing values in next step)


# In[6]:


project3.drop(['IsRetweet'],axis=1, inplace=True)


# In[7]:


project3.isnull().sum().sort_values(ascending=False) #(isnull and isna send same feedback)


# In[8]:


#start with SenderLocation missing values : column with the most missing values (364)
# Decided to drop column : location does not seem relevant for our analysis. Also if we needed to guess it seems like all data comes from Turkey
project3.drop(['SenderLocation'],axis=1, inplace=True)


# In[9]:


#investigating column IsSelfMentioned with value counts since all values are either 0 or 1 (or missing)
#from 5000 rows, 4990 = 0, 4 = 1 and 6 are missing.
# here again column will have no added value considering the few different values we have (4 out of 5000 or 0,08%)
#decision to drop this column 
project3['IsSelfMentioned'].value_counts()


# In[10]:


project3.drop(['IsSelfMentioned'],axis=1, inplace=True)


# In[11]:


#investigating column Retweets#
#varying values, may be interesting to keep for now . Maybe some outliers to filter later on .
# thanks to .describe() we know the first 3 quartiles are 0 so missing values will be replaced with 0 and should no impact our data too much 


# In[12]:


project3['Retweets#']=project3['Retweets#'].fillna(0)


# In[13]:


# Investigating AvgWordLength missing values 


# In[14]:


words = project3['Text'].str.split(' ')
words
int(sum(map(len,words[0])/len(words),0))


# In[15]:


# Defining a function in order to calculate the missing values of AvgWordLength 
# having troubles here to get the exact same number as the data when we double check with existing values 
# eg.: for row 1 getting 7 instead of 6

def avgwordlength(Series):
    words = Series.str.split(' ')
    return int(round(sum(map(len,words))/len(words),0))

avgwordlength(project3['Text'])


# In[16]:


project3['AvgWordLength']=project3['AvgWordLength'].fillna(avgwordlength(project3['Text']))


# In[17]:


#now the average word length has been calculated, we can drop the text column
project3.drop(['Text'],axis=1, inplace=True)


# In[18]:


project3.describe()
#this to see all columns since SenderFollowers# was not visible
pd.set_option('display.max_columns', None)


# In[19]:


#chosing to replace 5 missing values by mean value of 131. This should not impact our data
project3['SenderFollowers#']=project3['Retweets#'].fillna(131)


# In[20]:


# Investigating Emojis columns with 6 missing values
project3['Emojis#'].value_counts()
# approx 800 out of 5000 tweets have emojis, so 16% . Had tu juger weather or not this information will be usefull in future (is there a correlation between using an emoji and cyberbullying?)
cor=project3.corr()
cor
#thanks to the correlation view we can see that the IsCyberbullying/Emojis correlation is at 0.6 so there might be interesting data to analyze here.
#we are choosing to keep the Emojis column for further analysis. The missing values will be replaced by 0


# In[21]:


project3['Emojis#']=project3['Emojis#'].fillna(0.39)
#quick check to cinfirm we have no missing values anymore 
project3.isnull().sum() 


# In[22]:


#check if there are any duplicates - result is False so no duplicates in DataFrame
project3.duplicated().any()


# In[23]:


#searching for outliers using describe data
project3.describe()


# In[24]:


#looks like we have at least one tweet that is outlying on all features on the maximum scale. 
project3.sort_values('SenderFollowers#', ascending=False).head(10)


# In[25]:


# deleting rows that have more than 18 followers.
# 18 followers = Q 3 + 1,5 * IQR(Q3-Q1) so 17,5 rounded up to 18
# this drops 942 rows that are saved in "followeroutliers" if needed to be anaylzed
followeroutliers = project3[project3['SenderFollowers#']>18]
project3.drop(project3.loc[project3['SenderFollowers#']>18].index, inplace=True)
project3


# In[26]:


project3.describe()


# In[27]:


# delete columns that we will not want to study or analyse later on
# the following information does not seem necessary to conserv fo further work:
# Puctuations, Letter, Symbols, Uppercaseletter


# In[28]:


project3.drop(['Punctuations#','Letter#', 'Symbols#','UpperCaseLetter#'], axis=1,inplace=True)


# In[29]:


project3.describe()


# In[30]:


# Outliers : replace year 2020 by 1 year
project3['SenderAccountYears'].replace(2020,1, inplace=True)


# In[31]:


# Outliers : drop columns that have a value 0 or 1 in first 3 quartiles : Hashtags, Medias, Emojis
project3.drop(['Hashtags#','Medias#', 'Emojis#',], axis=1,inplace=True)


# In[32]:


project3.describe()


# In[33]:


#doing the same for senderfollowings as we did for senderfollowers
followingoutliers = project3[project3['SenderFollowings#']>1910]
project3.drop(project3.loc[project3['SenderFollowings#']>1910].index, inplace=True)
project3.describe()


# In[34]:


# columns that still have big outliers : Favorites, Mentions, SenderFavorites, Sender Statues


# In[35]:


project3.sort_values('Favorites#', ascending=False).head(10)


# In[36]:


#trying to visualize the outliers for the last 3 columns to know what to clear.
plt.figure(figsize=(10, 6))
project3.boxplot(column=['Favorites#']) 
# here valures over 800 seem to be outliers that can be deleted


# In[37]:


plt.figure(figsize=(10, 6))
project3.boxplot(column=['Mentions#']) 
# same here, deleting value over 20


# In[38]:


project3.drop(project3.loc[project3['Mentions#']>20].index, inplace=True)


# In[39]:


project3.describe()


# In[40]:


plt.figure(figsize=(10, 6))
project3.boxplot(column=['SenderFavorites#']) 
# outliers above 400000


# In[41]:


project3.drop(project3.loc[project3['SenderFavorites#']>400000].index, inplace=True)


# In[42]:


project3.describe()


# In[43]:


plt.figure(figsize=(10, 6))
project3.boxplot(column=['SenderStatues#']) 
# outliers above 0.6


# In[44]:


project3.drop(project3.loc[project3['SenderStatues#']>600000].index, inplace=True)


# In[45]:


project3.describe()


# In[46]:


project3


# In[47]:


encoder = LabelEncoder()
project3['IsCyberbullying_encode']=encoder.fit_transform(project3['IsCyberbullying'])
project3


# In[48]:


project3=project3.drop(columns=['IsCyberbullying'])


# In[49]:


project3['IsCyberbullying_encode'].value_counts()

#DATA IS NOW CLEAN AND READY TO BE USED
# # EXPORTING DATA TO MYSQL

# In[50]:


# Export data
project3.to_csv(r'C:\Users\Ingrid\Desktop\DAFT Nov 21\Projects\Project 3\project3_cyberbullying.csv')


# In[51]:


#'mysql://username:password@localhost/dbname'
engine = db.create_engine('mysql://root:Bonjour1@localhost/Project3')


# In[52]:


pip install mysqlclient


# In[53]:


engine.connect()

print(engine)


# In[54]:


# Exporting our DataFrame to SQL 
table_name = 'project_dataframe'
project3.to_sql(
    table_name,
    engine,
    if_exists='replace')


# In[ ]:




