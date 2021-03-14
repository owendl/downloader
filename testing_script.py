# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bs4 import BeautifulSoup
import requests
import keyring
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import os
import shutil
#%% user supplied
download_folder = "/Users/drewowen/Documents/roleplaying/downloads"
move_to ="/Users/drewowen/Documents/roleplaying/solo_rpgs"
user_field = "username"
pw_field = "password"

login_page = "https://itch.io/login"
downloads_page = "https://itch.io/bundle/download/BDbUvWXI1oh6ovQoKoNJ2jP2qnWEhcUI_AOGtoR3"
#%%

def prep_folder(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

def download_links(links, browser):
#Either method works here
    l=browser.find_elements_by_partial_link_text("Download")
    # lb=browser.find_elements_by_class_name("game_download_btn")
    for lis in l:
        result=lis.get_attribute('href')
        if result:
            links.append(result)
    return links

def try_downloads(browser, link):
    '''
    function that calls itself to try and download items that might be nested in a page

    Parameters
    ----------
    browser : TYPE
        DESCRIPTION.
    link : string
        one of the links found by download_links

    Returns
    -------
    None.

    '''

ef download_name(broswer):
    '''
    tries to get the name of the downloads

    Returns
    -------
    a string to call the download title

    '''
    download_title=browser.find_element_by_class_name("object_title-1").get_attribute('innerHTML').replace("/","")
    return download_title

prep_folder(download_folder)
    
prep_folder(move_to)

#%%

'''
This section of code defines some configurations for the firefox browser.
'''
profile = webdriver.FirefoxProfile()
#These two lines tell firefox to use a non-standard download folder.
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.dir", download_folder)

#Disabling possible firefox download pop-ups
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png, image/jpg, application/pdf, application/zip, text/html, text/rtf, text/plain")
profile.set_preference("plugin.scan.plid.all",False)
profile.set_preference("plugin.scan.Acrobat" ,"99.0")
profile.set_preference("pdfjs.disabled", True)


#%%
'''
s=BeautifulSoup(r.content, features="html")


payload = {user_field: keyring.get_password("system", "username"),
          pw_field: keyring.get_password("system","password")}

with requests.Session() as sess:
    res = sess.get(login_page)
    signin = BeautifulSoup(res._content, 'html.parser')
    #if we need a csrf token
    payload['csrf_token'] = signin.find(attrs= {"name":'csrf_token'})['value']
    
    res = sess.post(login_page, data=payload)
    print(res.content)
    res = sess.get(purchases)
    print(res.content)
    '''

browser = webdriver.Firefox(firefox_profile=profile)
browser.implicitly_wait(10)
browser.get(login_page)
time.sleep(1)
browser.find_element_by_name(user_field).send_keys(keyring.get_password("system", "username"))
browser.find_element_by_name(pw_field).send_keys(keyring.get_password("system", "password"))
browser.find_element_by_name(pw_field).send_keys(Keys.ENTER)

#%%
time.sleep(1)
browser.get(downloads_page)
time.sleep(1)


#%%

links=download_links([], browser)
#%%

next_flag=False
try:
    next_btn = browser.find_element_by_partial_link_text("Next")
    next_flag = True
except:
    next_flag = False

while next_flag:
    next_btn.click()
    time.sleep(2)
    links =  download_links(links, browser)
    
    try:
        next_btn = browser.find_element_by_partial_link_text("Next")
    except:
        next_flag = False

#%%
for game_link in links:    
    browser.get(game_link)
    time.sleep(1)
    
    game_title=browser.find_element_by_class_name("object_title-1").get_attribute('innerHTML').replace("/","")
    print(game_title)
    d=browser.find_elements_by_link_text("Download")
    d_len=len(d)
    for i in range(d_len):
        print("in download loop")
        download=d[i]    
        # print(download.get_attribute('innerHTML'))
        print(download.get_attribute('data-upload_id'))
    
        # download.click()
        time.sleep(1)
    
    rpg_files = os.listdir(download_folder)
    if len(rpg_files)==1:
        game_folder = move_to
    else:
        game_folder =os.path.join(move_to, game_title)
        prep_folder(game_folder)
        
    for file_name in rpg_files:
        full_file_name = os.path.join(download_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, game_folder)
            os.remove(full_file_name)

browser.quit()

