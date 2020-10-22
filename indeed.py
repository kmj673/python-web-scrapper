import requests
from bs4 import BeautifulSoup

LIMIT=50
URL=f"https://malaysia.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"

def get_last_pages():
  result = requests.get(URL)
  soup=BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class":"pagination"})
  links=pagination.find_all("a")
  pages=[]
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_jobs(html):
  title=html.find("h2",{"class":"title"}).find("a")["title"] 
  company=html.find("span",{"class":"company"})
  if company is not None:
    company_a=company.find("a")
    if company_a is not None:
      company=str(company_a.string)
    else:
      company=str(company.string)
    company=company.strip()  
  location=html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
  job_id=html["data-jk"]
  return {"title":title,"company": company, "location": location, "link":f"https://malaysia.indeed.com/viewjob?jk={job_id}" }

def get_extract_jobs(last_page):
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping Indeed : Page{page}")
    result=requests.get(f"{URL}&start={page*LIMIT}") 
    soup=BeautifulSoup(result.text, "html.parser") #html
    results=soup.find_all("div",attrs={"class":"jobsearch-SerpJobCard"}) #each job info
    for result in results:
      job=extract_jobs(result)
      jobs.append(job)
  return jobs


def get_jobs():
  last_pages=get_last_pages()
  jobs=get_extract_jobs(last_pages)
  return jobs