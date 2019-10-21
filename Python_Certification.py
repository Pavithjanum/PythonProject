import pandas as pd
import os

os.chdir(r'C:\Users\PAVI\Desktop\Edureka\Python Certification\Project')

US_911_data = pd.read_csv('539_cert_project_v1.csv',delimiter=',')

US_911_data.describe()
US_911_data.shape
US_911_data.size
US_911_data.head()
US_911_data.info()

# Compute -- What are the top 10 Zipcodes for 911 & Question 1: Are Zipcodes 19446
# and 19090 present ?

grp_data_by_zipcode =  US_911_data.groupby('zip')
top_10_zip = grp_data_by_zipcode['lat'].count().nlargest(10)
dic_top_10_zip_911 = dict(top_10_zip)

(19446 in dic_top_10_zip_911.keys()) & (19090 in dic_top_10_zip_911.keys())

# Compute -- What are the top 4 townships (twp) for 911 calls & Question 2: Which of
# the following township are not present? -- LOWER POTTSGROVE, NORRISTOWN,
# HORSHAM, ABINGTON

grp_data_by_twp =  US_911_data.groupby('twp')
top_4_twp = grp_data_by_twp['lat'].count().nlargest(4)
dic_top_4_twp_911 = dict(top_4_twp)

not_in_twp=[]

for item in ['LOWER POTTSGROVE', 'NORRISTOWN','HORSHAM', 'ABINGTON']:
    if item not in dic_top_4_twp_911.keys():
        not_in_twp.append(item)
        
print('The follwing township are not present in the top 4 townships: ')
for entry in not_in_twp:
    print(entry)

# Compute -- Create new features & Question 3: What is the most common Reason for a
# 911 call based on Reason Column? Which comes second

updated_911_data = pd.DataFrame(US_911_data)
updated_911_data['reason'] = updated_911_data['title'].apply(lambda x: x.split(':') [0] )
grp_data_by_reason = updated_911_data.groupby('reason')
top_2_reason = grp_data_by_reason['reason'].count().nlargest(2)
dic_top_2_reason_911 = dict(top_2_reason)

for key,value in dic_top_2_reason_911.items():
    print(key+'--'+str(value))
    
reason_ = list(dic_top_2_reason_911.keys())
print('Second most common Reason for a 911 call based on Reason Column is ',reason_[1])

# Compute -- Plot barchart using matplot for 911 calls by Reason & Question 4: How
# can you plot the bars horizontally ?

import matplotlib.pyplot as plt
reason_map = grp_data_by_reason['reason'].count()
reason_dic = dict(reason_map)
plt.barh(list(reason_dic.keys()),width=list(reason_dic.values()))
plt.show()

# Do data manipulation & Question 5: Which day got maximum calls for EMS and how
# many?

from datetime import datetime
updated_911_data['day'] = updated_911_data['timeStamp'].apply(lambda x:(datetime.strftime((datetime.strptime(x,'%Y-%m-%d %H:%M:%S')),'%A'))) 
updated_911_data_EMS = updated_911_data[updated_911_data.reason == 'EMS']

grp_data_by_day = updated_911_data_EMS.groupby('day')
day_with_max = grp_data_by_day['day'].count().nlargest(1)
dic_day_with_max = dict(day_with_max)

print( list(dic_day_with_max.keys())[0], 'got maximum calls for EMS and the count is',list(dic_day_with_max.values())[0])

# Compute -- Create a countplot of the Day of Week column with the hue based of the
# Reason column & Question 6: On which day traffic calls were lowest ?

grp_data_by_day = updated_911_data.groupby('day')
day_of_911 = grp_data_by_day['day'].count()
dic_day_of_911 = dict(day_of_911)

plt.plot(list(dic_day_of_911.keys()),list(dic_day_of_911.values()))
plt.xlabel('Day of Week')
plt.ylabel('Number of columns')
plt.show()

day_with_min = grp_data_by_day['day'].count().nsmallest(1)
dic_day_with_min = dict(day_with_min)
print('Day traffic calls were lowest on ',list(dic_day_with_min.keys())[0],'with count',list(dic_day_with_min.values())[0])

# Compute -- Create a countplot month wise -- Question 7: Which month saw highest
# calls for fire?

updated_911_data['month'] = updated_911_data['timeStamp'].apply(lambda x:(datetime.strftime((datetime.strptime(x,'%Y-%m-%d %H:%M:%S')),'%m')))
updated_911_data_fire = updated_911_data[updated_911_data.reason == 'Fire']
grp_data_by_month = updated_911_data_fire.groupby('month')
grp_data_by_month = grp_data_by_month['month'].count()
dic_grp_data_by_month = dict(grp_data_by_month)

plt.plot(list(dic_grp_data_by_month.keys()),list(dic_grp_data_by_month.values()))
plt.xlabel('Month')
plt.ylabel('Number of counts w.r.t Fire')
plt.show()

grp_data_by_month_max = grp_data_by_month.nlargest(1)
dic_grp_data_by_month_max = dict(grp_data_by_month_max)
print('Month that saw highest calls for fire is',datetime.strftime(datetime.strptime(list(dic_grp_data_by_month_max.keys())[0],'%m'),'%B'),'with count',list(dic_grp_data_by_month_max.values())[0])

# Compute -- Create Web Map for Traffic Calls & Question 8: Why some areas seem to
# have lower or almost zero traffic calls? Hint: Zoom the map

import folium
map = folium.Map(location=[40,-75],zoom_start=6,tiles='Stamen Terrain')
fg_fire = folium.FeatureGroup(name='Fire calls')
fg_EMS = folium.FeatureGroup(name='EMS calls')
fg_traffic = folium.FeatureGroup(name='Traffic calls')

updated_911_data_fire = updated_911_data[updated_911_data.reason == 'Fire']
updated_911_data_EMS = updated_911_data[updated_911_data.reason == 'EMS']
updated_911_data_traffic = updated_911_data[updated_911_data.reason == 'Traffic']

lt_fire =  updated_911_data_fire['lat']
ln_fire = updated_911_data_fire['lng']
addr_fire = updated_911_data_fire['addr']
reason_fire = updated_911_data_fire['reason']

for lat,lon,add,rea in zip(lt_fire,ln_fire,addr_fire,reason_fire):
    fg_fire.add_child(folium.Marker(location=[lat,lon],radius=6,popup=add,fill_color='green',fill=True,color='Grey',fill_opacity=0.7))


lt_EMS =  updated_911_data_EMS['lat']
ln_EMS = updated_911_data_EMS['lng']
addr_EMS = updated_911_data_EMS['addr']
reason_EMS = updated_911_data_EMS['reason']

for lat,lon,add,rea in zip(lt_EMS,ln_EMS,addr_EMS,reason_EMS):
    fg_EMS.add_child(folium.Marker(location=[lat,lon],radius=6,popup=add,fill_color='green',fill=True,color='red',fill_opacity=0.7))


lt_traffic =  updated_911_data_traffic['lat']
ln_traffic = updated_911_data_traffic['lng']
addr_traffic = updated_911_data_traffic['addr']
reason_traffic = updated_911_data_traffic['reason']

for lat,lon,add,rea in zip(lt_traffic,ln_traffic,addr_traffic,reason_traffic):
    fg_traffic.add_child(folium.Marker(location=[lat,lon],radius=6,popup=add,fill_color='green',fill=True,color='Grey',fill_opacity=0.7))


map.add_child(fg_fire)
map.add_child(fg_EMS)
map.add_child(fg_traffic)

map.add_child(folium.LayerControl())
map.save('911_Calls_v1.html')
    