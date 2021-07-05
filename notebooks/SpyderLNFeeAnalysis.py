# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pymongo import MongoClient
from random import randint
import pandas as pd
import seaborn as sns

# The MongoDB connection info.
connection = MongoClient('mongodb+srv://RickFontenot:Ska7punk%2A@cluster0.fmnuc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

# db name Puri_testdb_snapshotid7_0705
db = connection.Puri_testdb_snapshotid7_0705

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    satistics for router nodes with regard to base fee optimization.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Collection Name
col = db.opt_fees

x = col.find()

opt_fees = pd.DataFrame.from_records(x)
#to view datafram click on variable list

# list of columns and definitions 
# node	LN node           | public key
# total_income	          | routing income
# total_traffic	          | number of routed transactions
# failed_traffic_ratio	  | ratio of failed transactions out of total_traffic payments if node is removed from LN
# opt_delta	estimated     | optimal increase in base fee
# income_diff	estimated | increase in daily routing income after applying optimal base fee increment

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                  Distribution of payment path length
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Collection Name
col = db.lengths_distrib

x = col.find()

#Distribution of payment path length for the sampled transactions
len_dist = pd.DataFrame.from_records(x)


# list of columns and definitions 
# First	    | Payment path length
# Second	| Number of sampled transactions with given length

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                  nodes that forwarded payments 'routers'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Collection Name
col = db.router_incomes

x = col.find()

#statistics on nodes that forwarded payments. refered to these nodes as routers.
routers = pd.DataFrame.from_records(x)

# list of columns and definition
# node	    | LN node public key
# fee	    | routing income
#num_trans	| number of routed transactions

#check out the df
routers.head()

#summary stats of routers
routers.describe()

#looks like we have a big outlier
routers.loc[routers['fee'] == 60001.490000]

#update cell value to 601.49
routers.at[0, "fee"]=601.49

#see affect on summary stats
routers.describe()

#histogram of router fee
sns.set_style('whitegrid')
router_fee = sns.histplot(data=routers, x="fee")
router_fee.set(xlim=(0,100))
router_fee.set(ylim=(0,150))

#fee vs number of transactions
sns.relplot(x="fee", y='num_trans', kind = 'line', data=routers)
router_fee.set(xlim=(0,100))
router_fee.set(ylim=(0,200))

#joint plot showing similar thing
sns.jointplot(x="fee", y='num_trans', kind="kde",height=5, ratio=2, marginal_ticks=True, data=routers)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#         statistics on payment initiator nodes (senders).
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Collection Name
col = db.source_fees

x = col.find()

#statistics on nodes that forwarded payments. refered to these nodes as routers.
senders = pd.DataFrame.from_records(x)

#list of columns and definitions
#source	    | LN node that initiated the payment (sender node)
#num_trans	| the number of transactions initiated by this node in the simulation
#mean_fee	| the mean transaction cost per payment

senders.head()

senders.describe()

#looks like extreme outlier probably meant to be 601.55
senders.loc[senders['mean_fee'] == 60001.550000]

#update cell value to 601.55
senders.at[106, "mean_fee"]=601.55

#double check to ensure replacement
senders.loc[senders['mean_fee'] == 601.550000]

#see how that change affected summary stats
senders.describe()

#histogram of senders fees
sns.set_style('whitegrid')
sender_fee = sns.histplot(data=senders, x="mean_fee")

sender_fee.set(xlim=(0,100))
sender_fee.set(ylim=(0,150))