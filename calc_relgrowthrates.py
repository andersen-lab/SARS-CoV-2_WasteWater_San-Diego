import pandas as pd 
from freyja.utils import calc_rel_growth_rates

#growth rate calc based on PL data
agg_df = pd.read_csv('PointLoma_sewage_seqs.csv',header=0,skipinitialspace=True,index_col='Date') 
agg_df.index = pd.to_datetime(agg_df.index)
#drop VOC aggregations. 
agg_df = agg_df.drop(columns=['Alpha','Omicron','Delta'])

#restrict to more recent samples in case this gets big. 
daysIncluded = 90 # Use last 8 weeks of sample data

import datetime
h = pd.to_datetime(datetime.datetime.now()-datetime.timedelta(days=daysIncluded))
agg_df = agg_df.loc[agg_df.index>h]

nboots = 1000
serial_interval = 3.1 #estimated omicron serial interval
# daysIncluded = 56 # Use last 8 weeks of sample data

agg_df = agg_df.loc[:,agg_df.sum(axis=0)>0]
agg_df['Other'] = 100.-agg_df.sum(axis=1)


calc_rel_growth_rates(agg_df,nboots,serial_interval,'rel_growth_rates.csv',daysIncluded,thresh=0.01)

df = pd.read_csv('rel_growth_rates.csv',index_col='Lineage')
df = df.drop(index=['Other'])
df['EA'] = df['Estimated Advantage'].apply(lambda x:x[0:len(x)-1]).astype(float)
df = df.sort_values(by='EA',ascending=False)
df= df.drop(columns=['EA'])
df.to_csv('rel_growth_rates.csv')