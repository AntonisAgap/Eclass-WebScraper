import requests
from bs4 import BeautifulSoup
from termcolor import colored

url = ""
path = r""
username = ""
password = "" 


data = {"uname": username,"pass": password,"submit":""}
with requests.Session() as s:
    # getting cookies
    s.get(url)
    # sending a post request using data
    response = s.post(url,data=data)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find(id="portfolio_lessons")
    # fetching course's documents url and course's title
    courses = results.find_all('b')
    for course in courses:
        course_title = (course.find('a').contents[0])
        course_url = course.find('a')['href']
        course_id = course_url.split("/")[4]
        course_documents_download_url = url+"modules/document/index.php?course="+course_id+"&download=/"
        # path to download files to 
        target_path = path+str(course_title)+ ".zip"
        print(colored("Downloading "+str(course_title),"green"))
        course_documents = s.get(course_documents_download_url,stream = True)
        handle = open(target_path,"wb")
        for chunk in course_documents.iter_content(chunk_size=512):
            if chunk:
                handle.write(chunk)
        handle.close()
