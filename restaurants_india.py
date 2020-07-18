import streamlit as st
import pandas as pd

@st.cache(persist=True)
def load_data():
	restaurants1 = pd.read_csv('restaurants1.csv', encoding = 'latin-1')
	restaurants2 = pd.read_csv('restaurants2.csv', encoding = 'latin-1')
	df = pd.concat([restaurants1,restaurants2])
	df.drop(['url','currency','zipcode','city_id','country_id','locality_verbose','takeaway','opentable_support','highlights','timings'], axis=1, inplace=True)
	df = df[df['longitude'] != 0]
	df = df[df['latitude'] != 0]
	df.replace({"['CafÃ©']": "['Cafe']"}, inplace=True)
	df.drop_duplicates(subset= ['latitude','longitude'] ,inplace=True)
	return df

df = load_data()

establishment = []
for item in df['establishment'].unique().tolist():
    try:
        establishment.append(item.split("'")[1])
    except:
        pass

st.image('https://wallpapercave.com/wp/wp1874155.jpg', use_column_width = True)
st.title('Indian Restaurants Explorer')
st.markdown('')

city = st.sidebar.selectbox('Select your City', ['All'] + df['city'].unique().tolist())

g = df.groupby('city')
if city == 'All':
	city_df = df
else:
	city_df = g.get_group(city)

minimum_rating = st.sidebar.slider('Minimum Rating', 0.0,4.9)

type_of_food = st.sidebar.selectbox('Type of establishment', ['All']+establishment)


if type_of_food == 'All':
	city_df = city_df[city_df['aggregate_rating'] > minimum_rating]
else:
	type_of_establishment = "['{}']".format(type_of_food)
	city_df = city_df[(city_df['establishment'] == type_of_establishment) & (city_df['aggregate_rating'] > minimum_rating)]

if st.sidebar.checkbox('Home Delivery', False):
	city_df = city_df[city_df['delivery'] == 1]	
	
price = st.sidebar.selectbox('Price Range', ['0-200', '200-500', '500-1000', '1000-2000', '2000+','None'])
if price == "0-200":
	city_df = city_df[city_df['average_cost_for_two'] <= 200]
if price == "200-500":
	city_df = city_df[city_df['average_cost_for_two'] <= 500]
	city_df = city_df[city_df['average_cost_for_two'] > 200]
if price == "500-1000":
	city_df = city_df[city_df['average_cost_for_two'] <= 1000]
	city_df = city_df[city_df['average_cost_for_two'] > 500]
if price == "1000-2000":
	city_df = city_df[city_df['average_cost_for_two'] <= 2000]
	city_df = city_df[city_df['average_cost_for_two'] > 1000]
if price == "2000+":
	city_df = city_df[city_df['average_cost_for_two'] > 2000]

if len(city_df) == 0:
	st.error('No such restaurants available')
else:
	st.map(city_df[['latitude','longitude']])
	st.subheader('Top restaurants:')
	st.markdown('')
	for i in range(min(5,len(city_df))):
		st.markdown('**_{} -_**'.format(city_df.sort_values('aggregate_rating',ascending=False)['name'].iloc[i]))
		st.markdown('_{}_'.format(city_df.sort_values('aggregate_rating',ascending=False)['address'].iloc[i]))
