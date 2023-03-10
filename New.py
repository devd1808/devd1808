#!/usr/bin/env python
# coding: utf-8

# In[1]:



import pandas as pd
from pulp import *
import streamlit as st
import altair as alt

st.title('Raw Material Optimization')
st.markdown('The concept was to use LP to find an optimal mix of raw igt to produce the chepest meal bar while meeting some contraint nutrion requrement')
# In[2]:



# Import Nutrition Data
st.header('Nutrition and Ingredient Costs Data ')
nutrition = pd.read_excel('Nutrition Facts.xlsx', index_col = 0)




# In[3]:


# Import Costs
costs = pd.read_excel('Costs.xlsx')
dict_costs = dict(zip(costs['Ingredients'], costs['Costs']))


# Display the Data two tables side by side
col3, col4 = st.columns(2)

with col3:
    if st.sidebar.checkbox('Nutrition Data'):
        st.write(nutrition)

with col4:
    if st.sidebar.checkbox('Costs Data'):
        st.write(costs)
    
    

# In[25]:


# Variables
variables = ['Chicken', 'Beef', 'Mutton', 'Rice', 'Wheat bran', 'Corn', 'Peanuts']

# Initialize Class
model = LpProblem("Optimize your Protein Bar", LpMinimize)

# Create Decision Variables
x = LpVariable.dicts("Qty", [j for j in variables],
                     lowBound=0, upBound=None, cat='continuous')

# Define Objective Function
model += (lpSum([dict_costs[i] * x[i] for i in variables]))

 
# Add Constraints
with st.sidebar:
    st.sidebar.header("Meal Bar weight")
    model += (lpSum([x[i] for i in variables])) == st.sidebar.number_input('Total weight', 100, 120)# 120gm total weight not more or less 
    st.sidebar.header("Nutritional Fact")
    model += (lpSum([x[i] * nutrition.loc[i, 'Protein'] for i in variables])) >= st.sidebar.number_input('Prtotien range 0-20', 0, 20)    
    # int(input("Enter your Protien: "))    #protein 
    model += (lpSum([x[i] * nutrition.loc[i, 'Fat'] for i in variables])) <= st.sidebar.number_input('Fat range 0-22', 0, 22)   #int(input("Enter your Fat: "))        #fat max
    model += (lpSum([x[i] * nutrition.loc[i, 'Fibre'] for i in variables])) >= st.sidebar.number_input('Fiber range 0-6', 0, 6)   #int(input("Enter your Fibre: "))      # fiber min
    model += (lpSum([x[i] * nutrition.loc[i, 'Salt'] for i in variables])) <= st.sidebar.number_input('Salt range 0-3', 0, 3) #int(input("Enter your Salt: "))      # salt max
    model += (lpSum([x[i] * nutrition.loc[i, 'Sugar'] for i in variables])) <= st.sidebar.number_input('Sugar range 0-30', 0, 30)   #int(input("Enter your Sugar: "))      # sugar max
                                                   
              
        
# Solve Model
Mod_var=[]

model.solve()
st.title('Cost Per Bar')
print("Cost per Bar = {:,} $".format(round(value(model.objective), 2)))
st.markdown(value(model.objective))


print('\n' + "Status: {}".format(LpStatus[model.status]))
for v in model.variables():
    print(v.name, "=", round(v.varValue,2), 'g')
    Mod_var.append({'Status':v.name,'Optimal':round(v.varValue,2)})
    #Mod_var.append(a)
a=pd.DataFrame(Mod_var)

# Add a title to the plot
st.title('Table and Bar chart for Optimal Ingredient in gm')


# Display the table and the graph in two columns
col1, col2 = st.columns(2)

with col1:
    st.write(a)

with col2:
    st.bar_chart(a.set_index('Status'))
    


    
    
    
    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




