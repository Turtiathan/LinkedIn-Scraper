# import web driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

class LinkedInScraper():
	def __init__(self, search_keyword, number_of_pages):
		self.search_keyword = search_keyword
		self.number_of_pages = number_of_pages
		self.page_links = []
		self.recruiter_names = []
		self.linkedin_links = []

		# specifies the path to the chromedriver.exe
		self.driver = webdriver.Chrome("C:/Users/Alex/SkyDrive/Python/Webdrivers/chromedriver_win32_version_78/chromedriver.exe")

	def fetch_page_links(self):
		"""
		Begins the web scraping when it goes to Google and searches what we want from LinkedIn. Also gets the links 
		for all the pages we will scrape.
		"""
		# Open up web browser and go to Google.
		self.driver.get('https://www.google.com')

		# Search on Google.
		search_query = self.driver.find_element_by_name('q')
		search_query.send_keys('site:linkedin.com/in/ AND ' + self.search_keyword)
		search_query.send_keys(Keys.RETURN)

		links = self.driver.find_elements_by_class_name("fl")
		print(links)
		links = [link.get_attribute('href') for link in links]
		print(links)

		for link in links:
			if "https://www.google.com/search?q=site:linkedin.com/in/+AND+" not in link:
				continue

			self.page_links.append(link)

			if len(self.page_links) == self.number_of_pages-1:
				break

		# We don't need every link. For example, if self.number_of_pages = 10, we just need the first 10 pages.
		# We subtract one because the first page is already loaded.
		self.page_links = self.page_links[:self.number_of_pages-1]

		self.scrape()

	def scrape(self):
		"""
		This function scrapes the page for names and their LinkedIn profiles. At the end, we go to the next 
		page and scrape the same things. It stops once we scraped all the pages that we want.
		"""
		current_page_recruiters = self.driver.find_elements_by_class_name("LC20lb")
		[self.recruiter_names.append(recruiter.text.split(" -")[0]) for recruiter in current_page_recruiters]

		divs = self.driver.find_elements_by_class_name('r')
		[self.linkedin_links.append(div.find_element_by_css_selector('a').get_attribute('href')) for div in divs]

		self.number_of_pages -= 1
		while self.number_of_pages > 0:
			self.driver.get(self.page_links[0])
			self.page_links = self.page_links[1:] # Remove the link from the list of links once it loads.
			self.scrape()

	def write_to_csv(self):
		"""
		This takes the names and LinkedIn profiles we obtained, and stores them into a csv file.
		"""
		with open("technical_recruiters.csv", 'w', newline='') as f:
			write = csv.writer(f)
			write.writerow(["Recruiter Name", "LinkedIn Profile"])

			for i in range(len(self.recruiter_names)):
				write.writerow([self.recruiter_names[i], self.linkedin_links[i]])

scrape = LinkedInScraper("technical recruiter", 10)
scrape.fetch_page_links()
scrape.write_to_csv()
