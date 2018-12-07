######################## import all required stuff #########################
import re
import pandas as pd
import numpy as np 

############## importing the dataset into program using pandas ##############

dataset = pd.read_csv("data.csv")
dataset = dataset.replace(np.nan, 'NA', regex=True)

############## extracting required columns from the dataset  ################

review_text=list(dataset["review_text"]);review_clean=[];cr=[];review = "";reviews_text = list()

for i in review_text:
	for j in i:
		j=str(j)
		if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j) or re.search(r'\!',j)):
			review+=j
	review_clean.append(review)
	review=""

for i in review_clean:
	res=re.findall(r'n\'t',i)
	i = i.replace("n\'t",' not')
	cr.append(i)

cr1 = cr

restaurant_name=list(dataset["name"]);restaurant_name_clean=[];review="";restaurant_names = list()

for i in restaurant_name:

	for j in i:

		j=str(j)

		if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j) or re.search(r'\!',j)):
			
			if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j)):

				j=j.lower()

			review+=j
	
	restaurant_name_clean.append(review)
	
	review=""

rn = restaurant_name_clean 


review_title=list(dataset["title"]);title_clean=[];rtc1=[];title = "";reviews_title = list()

for i in review_title:
	for j in i:
		j=str(j)
		if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j) or re.search(r'\!',j)):
			title+=j
	title_clean.append(title)
	title=""

rtc1 = title_clean

reviewer_list=list(dataset["author"]);reviewer_clean=[];rc1=[];reviewer = "";reviewers = list()

for i in reviewer_list:
	for j in i:
		j=str(j)
		if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j) or re.search(r'\!',j)):
			reviewer+=j
	reviewer_clean.append(reviewer)
	reviewer=""

rc1 = reviewer_clean

ids = list(dataset['uniq_id']) #done
restaurant_ids = list(dataset['restaurant_id']) #2 done
restaurant_names = rn #4 done
reviews_title = rtc1 #6 done
reviews_date = list(dataset['review_date']) #7 done
reviews_text = cr1 #8 done
reviewers = rc1 #9 done
star_ratings = list(dataset['rating']) #12 done
visit_dates = list(dataset['visited_on']) #16 done   

################# Grouping restaurants having same ids ################
unique_restaurant_ids = []
indexes_with_same_rest_id = {}
for id in restaurant_ids:
    if id not in unique_restaurant_ids: 
        index = [i for i,x in enumerate(restaurant_ids) if x == id]
        unique_restaurant_ids.append(id) 
        indexes_with_same_rest_id[id] = index
        
############### Grouping reastaurants having same names ###################
unique_restaurant_names = []
indexes_with_same_rest_name = {}
for name in restaurant_names:
    if name not in unique_restaurant_names:
        index = [i for i,x in enumerate(restaurant_names) if x == name]
        unique_restaurant_names.append(str(name).lower())
        indexes_with_same_rest_name[name] = index


######## Keywords indicating the nature of review ############

positive_words = ['perfect','great','good','tasty','friendly','spectacular','awesome','delicious','yummy','best','soothing','juicy']

negative_words = ['bad','tastless','sad','mild','foul']

positive_words_syns = [] 

negative_words_syns = []


##### Getting Synonums using nltk #####
from nltk.corpus import wordnet  
for word in positive_words:    
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            positive_words_syns.append(l.name())

positive_words_syns = list(set(positive_words_syns))
#print(positive_words_syns) 

for word in negative_words:    
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            negative_words_syns.append(l.name())

negative_words_syns = list(set(negative_words_syns))
#print(negative_words_syns) 


########### Assigning scores for each review ##############

indexes_with_rest_id_greater_than_one_elements = {}   
for id,sublist in indexes_with_same_rest_id.items():
    if(len(sublist)>1):
        indexes_with_rest_id_greater_than_one_elements[id] = sublist    


def classifyReviewsOf(indexes):
    indexWiseScore = {}
    positive_reviews = []
    negative_reviews = []
    insufficient_data_to_classify = []
    ###################################modified here########################
    for index in indexes:
        score = calcScore(reviews_text[index])
        indexWiseScore[index] = score;
        if(score>0):
            positive_reviews.append(reviews_text[index])
        elif(score<-0):
            negative_reviews.append(reviews_text[index])
        else:
            insufficient_data_to_classify.append(reviews_text[index])     
            #################and next line#################################
    return positive_reviews,negative_reviews,insufficient_data_to_classify,indexWiseScore     #a lot of things

def calcScore(review):
    score = 0
    for word in review.split():
        if(word in positive_words_syns):
            score+=1
        elif(word in negative_words_syns):
            score-=1
    return score

#############################below is a new function#########################
def recommendRestaurantForACuisine(indexWiseScore):
    popular_restaurants = sorted(indexWiseScore, key=lambda x: (-indexWiseScore[x], x))
    most_popular_rest = []
    for index in popular_restaurants:
        most_popular_rest.append(restaurant_name[index])
    return most_popular_rest

#### Type of Food found in restaurants ####
    
food_in_restaurants={} # dictionary with keys = food_type & value = indexes of restaurants

cuisines=["french", "indian", "italian", "spanish", "mexican", "english", "dutch", "european", "chinese", "pakistani"]

restaurant_index=[];

for cuisine in cuisines:
    for review in reviews_text:
        temp=str(review).lower()
        if(re.search(cuisine,temp)):
            restaurant_index.append(reviews_text.index(review))
            
    food_in_restaurants[cuisine]=restaurant_index
    
    restaurant_index=[] # resetting the list
    

####### Main Output of Program ##############

response='y'

while(response == 'y' or response == 'Y'):
    print("\n\n Select an option: \n\n\n")
    print(" 1. Search by Restaurant Name :\n")
    print(" 2. Search by Cuisine :\n")
    print(" 3. Search by Restaurant ID :\n")
    positive_reviews=[]
    negative_reviews=[]
    insufficient_data_to_classify=[]
    pos=0;neg=0;neu=0;total=0;
    choice=int(input())
        
    if(choice==1):
        #reqId=input("Enter Restuarant ID: ")
        reqName=input("Enter Restaurant Name: ").lower()
        #print(reqName)
        #reqIndexes=indexes_with_same_rest_name[reqName]
        if reqName in restaurant_names:
        	index = restaurant_names.index(reqName)
        reqId = restaurant_ids[index]
        reqIndexes=indexes_with_same_rest_id[reqId]
        positive_reviews, negative_reviews, insufficient_data_to_classify,indexWiseScore = classifyReviewsOf(reqIndexes)
        
    elif(choice==2):    
        reqId=input("Enter Food Type: ").lower()
        #reqIndexes=indexes_with_same_rest_id[reqId]        
        if reqId in food_in_restaurants.keys():
            positive_reviews, negative_reviews, insufficient_data_to_classify,indexWiseScore = classifyReviewsOf(food_in_restaurants[reqId])
            most_popular_restaurant = recommendRestaurantForACuisine(indexWiseScore)
            print("The most popular restaurant for " + reqId + " cuisine is: " + most_popular_restaurant[0] )
        showAll = input("Do you want to see all restaurants recommendations? \nY or N: ")
        if(showAll.lower()=="y"): 
            unique_most_popular_restaurant = []
            for restaurant in most_popular_restaurant:
                if(restaurant not in unique_most_popular_restaurant):
                    unique_most_popular_restaurant.append(restaurant)
            for restaurant in unique_most_popular_restaurant:
                print(restaurant)
    if(choice==3):
        reqId=input("Enter Restuarant ID: ")
        reqIndexes=indexes_with_same_rest_id[reqId]
        positive_reviews, negative_reviews, insufficient_data_to_classify,indexWiseScore = classifyReviewsOf(reqIndexes)
        #print(len(positive_reviews),"\n")
        #print(len(negative_reviews),"\n")
        #print(len(insufficient_data_to_classify),"\n")
    if(choice==1 or choice==3):
	    positive=len(positive_reviews)
	    negative=len(negative_reviews)
	    neutral=len(insufficient_data_to_classify)
	    total=positive+negative+neutral;
	    positive_percentage=(positive*100)//total
	    negative_percentage=(negative*100)//total
	    neutral_percentage=(neutral*100)//total
	    print("Positive Reviews : ",positive_percentage,"% \n")
	    print("Negative Reviews : ",negative_percentage,"% \n")
	    print("Neutral Reviews : ",neutral_percentage,"% \n") 
    response = input("Do you want to continue ? ")