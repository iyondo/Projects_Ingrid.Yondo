#!/usr/bin/env python
# coding: utf-8
Python program to generate a random strong password:

- Minimum length 6 characters.

- Maximum length 16 characters.

- At least 1 letter between [a-z] and 1 letter between [A-Z].

- At least 1 number between [0-9].

- At least 1 character from [$#@].


# In[23]:


import random
import string

length = random.randrange(2,12)

lower = string.ascii_lowercase 

upper = string.ascii_uppercase 

number = string.digits 

special_char = "@#$" 

all = lower + upper + number + special_char 

sample = "".join(random.sample(all,length)) 

char_list = [random.choice(special_char),
            random.choice(lower),
            random.choice(upper),
            random.choice(number),
            sample]

random.shuffle(char_list) 

password = ''.join(char_list) 

print(password)


# In[ ]:





# In[ ]:




