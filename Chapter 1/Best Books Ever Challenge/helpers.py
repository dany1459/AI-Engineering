import re

def check_Series(title):
    """checks if a book is a series or not using the title name

    Args:
        title (str):the tile of a book

    Returns:
        bolean: true is book is series, false otherwise
    """
    if len(title.split('(')) > 1:
        return True
    return False

def getRatings(ratings):
    """extracts the average rating and number of rating

    Args:
        ratings (str): a string containing the average and number of ratings

    Returns:
        (int, int): the average rating and the number of rating
    """
    ratings = ratings.replace(',','')
    ratings = re.findall(r'\d+', ratings)
    avg_rating = float(ratings[0]+'.'+ratings[1])
    num_ratings = int(ratings[2])
    
    return avg_rating, num_ratings

def get_original_publish_year(original_publish_year):
    """extraacts the origiantion published date

    Args:
        original_publish_year (str): a string conatining the original published date

    Returns:
        int: the year of publication
    """
    return  [int(s) for s in original_publish_year.replace(')','').split() if s.isdigit()][-1]
    
def get_no_review_pages(review_pages):
    """extracts the books number of pages from review section

    Args:
        review_pages (str): a string containing the number of pages from review section

    Returns:
        int: the books number of pages
    """
    return int(review_pages.replace(',','').split()[0])

def get_book_index(link):
    """extracts unique identifier for book from the url

    Args:
        link (str): the link to the book

    Returns:
        int: a unique identifier for the book
    """
    return int(''.join([i for i in link.split('/')[-1] if i.isdigit()]))