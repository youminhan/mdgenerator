
import os,sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from Naked.toolshed.shell import execute_js
from datetime import datetime
import os

today = datetime.today().strftime('%Y-%m-%d')
print(today)
quesList = sys.argv[1:]
print(quesList)

companyList = []
topicList = []

#Add Cookie
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=/Users/youminhan/Library/Application Support/Google/Chrome/Default")
dir,file = os.path.split(os.path.abspath(sys.argv[0]))
browser = webdriver.Chrome(dir + '/chromedriver', chrome_options=options)

for ques_num in quesList: 
    ques_num = int(ques_num)
    # Search question
    browser.get('https://leetcode.com/problemset/all/?search=' + str(ques_num))

    # Find question URL and open question
    table_path = "//*[@id='question-app']/div/div[2]/div[2]/div[2]/table/tbody[1]/tr[1]/td[3]/div/a"
    element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, table_path)))
    ques_url = element.get_attribute("href")
    print(ques_url)
    element.click()

    company_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[5]/div[2]/div/a[1]/button/div/span[1]"
    topic_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[6]/div[2]"
    topic_click_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[6]/div[1]"
    click_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[5]/div[1]/div/div"
    list_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[5]/div[2]"
    question_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]"
    title_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[1]/div[1]"
    diff_path = "//*[@id='app']/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[1]/div[2]/div"
    time.sleep(3)

    # Get title
    title_element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, title_path)))
    title_arr = title_element.get_attribute('innerHTML').split(". ", 1)
    ques_title = title_arr[1]
    print(title_arr)
    print(ques_title)

    # Get difficulty
    diff_element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, diff_path)))
    ques_diff = diff_element.get_attribute('innerHTML')
    print(ques_diff)


    # Get question contnet
    question_element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, question_path)))

    # Click to show company list
    click_element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, click_path)))
    click_element.click()

    # Get a list of company
    company_element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, list_path)))
    html_page = company_element.get_attribute('innerHTML')
    question_soup = BeautifulSoup(html_page, "html.parser")
    for link in question_soup.findAll('span', attrs={'class': re.compile("btn-content__lOBM")}):
        companyList.append(link.text)
    companyList.sort()
    print(companyList)

    # Click to show topic
    topic_click_element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, topic_click_path)))
    topic_click_element.click()

    # Get a list of topic
    topic_element = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, topic_path)))
    topic_html_page = topic_element.get_attribute('innerHTML')
    topic_soup = BeautifulSoup(topic_html_page, "html.parser")
    for link in topic_soup.findAll('span', attrs={'class': re.compile("tag__2PqS")}):
        topicList.append(link.text)
    topicList.sort()
    print(topicList)

    ques_file_name = str(ques_num) + '-' + ques_url.split("/problems/",1)[1]
    print(ques_file_name)

    # Convert to md
    if not os.path.exists('temp/'):
        os.makedirs('temp/')
    if not os.path.exists('md/'):
        os.makedirs('md/')
    with open('temp/' + ques_file_name + '.html', 'w') as f:
        f.write(question_element.get_attribute('innerHTML'))
        f.close()
    success = execute_js('html2markdown.js ' + ques_file_name)


    with open('md/' + ques_file_name + '.md', 'r+') as f:
        lines = f.readlines()
        f.seek(0, 0)
        f.write('---')
        f.write('layout: default')
        f.write('\n')
        f.write('title: ' + ques_title + '\n')
        f.write('topic: ')
        f.write('%s ' % topicList)
        f.write('\n')
        f.write('level: ' + ques_diff + '\n')
        f.write('ques_num: ' + str(ques_num) + '\n')
        f.write('parent: Question\n')
        f.write('date: ' + today + '\n')
        f.write('company: ')
        f.write('%s ' % companyList)
        f.write('\n')
        f.write('---\n\n')  
        f.write('{% if page.level == "Easy" %}\n')
        f.write('  [{{ page.level}}]({{site.baseurl}}/docs/levelsort){: .btn .btn-green }\n')
        f.write('  [{{ page.topic}}]({{site.baseurl}}/docs/topicsort){: .btn .btn-purple }\n')
        f.write('{% if page.level == "Medium" %}\n')
        f.write('  [{{ page.level}}]({{site.baseurl}}/docs/levelsort){: .btn .btn-orange }\n')
        f.write('  [{{ page.topic}}]({{site.baseurl}}/docs/topicsort){: .btn .btn-purple }\n')
        f.write('{% if page.level == "Medium" %}\n')
        f.write('  [{{ page.level}}]({{site.baseurl}}/docs/levelsort){: .btn .btn-red }\n')
        f.write('  [{{ page.topic}}]({{site.baseurl}}/docs/topicsort){: .btn .btn-purple }\n')
        f.write('{% if page.company %}\n')
        f.write('{% endif %}\n\n')
        f.write('{% assign sorted = page.company | sort %}\n')
        f.write('{% for page in sorted %}\n')
        f.write('<p class="label label-blue">{{page}}</p>\n')
        f.write('{% endfor %}\n')
        f.write('<div style="height: 7px"></div>\n')
        f.write('{% endif %}\n\n')

        f.write('{{ page.date}}\n')
        f.write('{: .label .label-red }\n\n')
        f.write('## {{page.ques_num}}. {{ page.title}} \n\n')
        f.write('<!-- ### Similar Question: [LeetCode Question xxx]({{site.baseurl}}/docs/question/xxx) -->\n\n')
        f.write('<!-- ![]({{site.baseurl}}/images/interval1.png) -->\n\n')
        f.write('### [Question](' + ques_url + '){:target="_blank"}:  \n')
        
        for line in lines: # write old content after new
            f.write(line)

        f.write('\n\n---\n\n### Solution:  \n\n\n```java\n\n```\n')
        f.close()
        # os.remove('temp/' + ques_file_name + '.html')

# Close browser
browser.close()
