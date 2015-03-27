
# coding: utf-8

# In[2]:

import whois


# In[4]:

# Using whois module can let us extract data for all the popular TLDs(com, org, net...)
w = whois.whois('pythonforbeginners.com')
print w


# In[5]:

w.expiration_date


# In[6]:

w.text


# In[7]:

# To make the program a bit more interactive, enable raw_input
data = raw_input("Enter a domain: ")
w = whois.whois(data)

print w


# In[ ]:



