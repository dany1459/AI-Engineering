#Imports
from selenium import webdriver
import pandas as pd
import re
import time
from helpers import *

def scraper(my_driver,csv_name,page_url_csv,page_number_store,save_freq,no_items_needed,wait_time):
    """This function scraps best-books from the website of the best-books

    Args:
        my_driver (str): the location and file name of the chrome driver
        csv_name (str): the location and file name to save the scrapped items
        page_url_csv (str): the url of the page to scrap from
        page_number_store (str): the location and file name to store intermedate page numbers
        save_freq (int): how often you want to write to the output file
        no_items_needed (int): the number of items you want to scrap
        wait_time (int): the delay time in secs
    """

    #open chrome
    op = webdriver.ChromeOptions()
    op.add_argument('headless')

    #collect in dictionary
    content_dict = {'url':[],'title':[],'author':[],'num_reviews':[],'num_ratings':[],'avg_rating':[],'num_pages':[],\
        'original_publish_year':[],'series':[],'genres':[],'awards':[],'places':[],'description':[],'book_index':[]}

    #if csv doesn't exist, create new one
    try:
        df = pd.read_csv(csv_name)
        next_row = df.shape[0]
        with open(page_url_csv,'r') as file:
            main_url = file.readlines()[0]
        with open(page_number_store,'r') as file:
            page_number = int(file.readlines()[0])
    except:
        next_row = 0
        with open(csv_name,'w') as file:
            file.write(','.join(content_dict.keys()))
            file.write('\n')
        with open(page_number_store,'w') as file:
            file.write(str(1))
            file.write('\n')
    k=0

    #move through the pages
    while True:
        print("="*20+"page("+str(page_number)+")"+"="*20)
        main_driver = webdriver.Chrome(my_driver,options=op)
        main_driver.implicitly_wait(wait_time)
        main_driver.get(main_url)
        time.sleep(wait_time)

        books = main_driver.find_elements_by_xpath('.//a[@class="bookTitle"]')
        author = main_driver.find_elements_by_xpath('.//a[@class="authorName"]')
        ratings = main_driver.find_elements_by_xpath('.//span[@class="minirating"]')

        den_divisor = len(books)
        it = next_row%den_divisor
        # print(it,next_row,len(books))


        while it+1 != len(books):
            #back to base url
            main_driver = webdriver.Chrome(my_driver,options=op)
            main_driver.implicitly_wait(wait_time)
            main_driver.get(main_url)
            time.sleep(wait_time)

            #get title, url, book index, series, author
            try: content_dict['title'].append(books[it].text)
            except: content_dict['title'].append(None)
            
            try: content_dict['url'].append(books[it].get_attribute("href"))
            except: content_dict['url'].append(None)

            try: content_dict['book_index'].append( get_book_index(books[it].get_attribute("href")) )
            except: content_dict['book_index'].append(None)

            try: content_dict['series'].append(check_Series(books[it].text))
            except: content_dict['series'].append(None)

            try: content_dict['author'].append(author[it].text)
            except: content_dict['author'].append(None)
            

            #get average rating, number of rating
            try:
                avg_rating, num_ratings = getRatings(ratings[it].text)
                content_dict['avg_rating'].append(avg_rating)
                content_dict['num_ratings'].append(num_ratings)
            except:
                content_dict['avg_rating'].append(None)
                content_dict['num_ratings'].append(None)

            #Follow the link of book i (redirection to book i page)

            #update movie_i_driver url
            book_i_driver_url = books[it].get_attribute("href")
            main_driver = webdriver.Chrome(my_driver,options=op)
            main_driver.implicitly_wait(wait_time)
            main_driver.get(book_i_driver_url)


            rightContainer = main_driver.find_element_by_xpath("//div[@class='rightContainer']")

            #get description
            try:
                description = main_driver.find_element_by_xpath("//div[@id='description']")
                description_href = description.find_elements_by_xpath('./a[contains(@href, "#")]')
                if len(description_href) != 0:
                    description_href[0].click()
                description = description.find_elements_by_tag_name("span")[-1]
                content_dict['description'].append(description.text)
            except:
                content_dict['description'].append(None)
            
            
            #get genres
            try:
                genres = rightContainer.find_elements_by_xpath('.//div[@class="elementList "]')
                genres = [g.find_element_by_xpath('.//div[@class="left"]').text for g in genres]
                content_dict['genres'].append(genres)
            except:
                content_dict['genres'].append(None)

            #get number of reviews
            try:
                bookMeta = main_driver.find_element_by_xpath('.//div[@id="bookMeta"]')
                hyperlink = bookMeta.find_elements_by_xpath('.//a[@class="gr-hyperlink"]')
                content_dict['num_reviews'].append( get_no_review_pages(hyperlink[-1].text) )
            except:
                content_dict['num_reviews'].append( None )

            #get number of pages
            try:
                numberOfPages = main_driver.find_element_by_xpath('.//span[@itemprop="numberOfPages"]')
                content_dict['num_pages'].append( get_no_review_pages(numberOfPages.text) )
            except:
                content_dict['num_pages'].append( None)

            #get original published year
            try:
                details = main_driver.find_element_by_xpath('.//div[@id="details"]')
                original_publish_year = details.find_elements_by_xpath('.//div[@class="row"]')[1]
                content_dict['original_publish_year'].append( get_original_publish_year(original_publish_year.text) )
            except:
                content_dict['original_publish_year'].append( None )
            
            #for places and awards
            main_driver.find_element_by_xpath('.//a[@id="bookDataBoxShow"]').click()
            bookDataBox = main_driver.find_element_by_xpath('.//div[@id="bookDataBox"]')
            
            #get places
            try:
                setting_div = bookDataBox.find_element_by_xpath("//div[text()='Setting']")
                settings = setting_div.find_element_by_xpath("./following-sibling::div")
                children = settings.find_elements_by_xpath('./span[contains(@class, "toggleLink")]')
                if len(children) != 0:
                    children[0].click()
                places = settings.find_elements_by_tag_name("a")
                places = [ a.text for a in places if a.get_attribute("href")[-1] != '#' ]
                content_dict['places'].append(places)
            except:
                content_dict['places'].append(None)

            
            #get awards
            try:
                literary_awards_div = bookDataBox.find_element_by_xpath("//div[text()='Literary Awards']")
                literary_awards = literary_awards_div.find_element_by_xpath("./following-sibling::div")
                children = literary_awards.find_elements_by_xpath('./span[contains(@class, "toggleLink")]')
                if len(children) != 0:
                    children[0].click()
                awards = literary_awards.find_elements_by_xpath('.//a[@class="award"]')
                awards = [ a.text for a in awards ]
                content_dict['awards'].append(awards)
            except:
                content_dict['awards'].append(None)
            
            #save data to csv after save_freq iterations
            if k%save_freq == 0 and k != 0:
                
                df = pd.DataFrame(content_dict)
                df.to_csv(csv_name, mode='a', header=False, index=False)
                print("Within page writing: "+str(save_freq)+", tottal written:"+str(next_row))
                content_dict = {'url':[],'title':[],'author':[],'num_reviews':[],'num_ratings':[],'avg_rating':[],'num_pages':[],\
                    'original_publish_year':[],'series':[],'genres':[],'awards':[],'places':[],'description':[],'book_index':[]}
            k += 1
            next_row += 1
            it = next_row%den_divisor
            
        next_row += 1


        #save data to csv after
        df = pd.DataFrame(content_dict)
        df.to_csv(csv_name, mode='a', header=False, index=False)
        print("After page writing: "+str(k%save_freq)+", tottal written:"+str(next_row))
        content_dict = {'url':[],'title':[],'author':[],'num_reviews':[],'num_ratings':[],'avg_rating':[],'num_pages':[],\
            'original_publish_year':[],'series':[],'genres':[],'awards':[],'places':[],'description':[],'book_index':[]}  
            
        #move to next page
        try:
            if k != 0:
                #back to base url
                main_driver = webdriver.Chrome(my_driver,options=op)
                main_driver.implicitly_wait(wait_time)
                main_driver.get(main_url)
                
                next_page = main_driver.find_element_by_xpath('//a[@class="next_page"]')

                #update main_url for next movie page
                main_url = next_page.get_attribute("href")
                
                
                with open(page_url_csv,'w') as file:
                    file.write(main_url)
                    file.write('\n')

                #store current page number
                page_number += 1
                with open(page_number_store,'w') as file:
                    file.write(str(page_number))
                    file.write('\n')

            #Stop after no_items_needed
            if k >= no_items_needed:
                break
            
            
        except:
            #stop loop when there is no next page
            break

        page_number += 1

        
    #write remaining items to csv
    if k%save_freq != 0:
        df = pd.DataFrame(content_dict)
        df.to_csv(csv_name, mode='a', header=False, index=False)
        print("final writing now: "+str(k%save_freq)+", total written:"+str(next_row))

    print("Done")
