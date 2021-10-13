import re

def check_Series(title):
    if len(title.split('(')) > 1:
        return True
    return False

def getRatings(ratings):
    ratings = ratings.replace(',','')
    ratings = re.findall(r'\d+', ratings)
    avg_rating = float(ratings[0]+'.'+ratings[1])
    num_ratings = int(ratings[2])
    
    return avg_rating, num_ratings

def get_original_publish_year(original_publish_year):
    return  [int(s) for s in original_publish_year.replace(')','').split() if s.isdigit()][-1]
    
def get_no_review_pages(review_pages):
    return int(review_pages.replace(',','').split()[0])

def get_book_index(link):
    return int(''.join([i for i in link.split('/')[-1] if i.isdigit()]))