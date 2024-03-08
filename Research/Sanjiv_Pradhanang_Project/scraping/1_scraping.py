import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

start_time = time.time()

# ufc 100 is page 22
# ~1 second per page
pages = 1

event_links = []
fight_links = []

# hiding browser
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)

# driver = webdriver.Chrome()

for p in range(1, pages+1):
  r = driver.get(f"http://ufcstats.com/statistics/events/completed?page={p}")
  elems = driver.find_elements(By.CSS_SELECTOR, ".b-statistics__table-row .b-statistics__table-content")
  event_links.extend([el.find_element(By.CSS_SELECTOR, "a.b-link.b-link_style_black").get_attribute('href') for el in elems])

# print length of events links array, first and last
print(f'\nLength of events: {len(event_links)}\nFirst event: {event_links[0]}\nLast event: {event_links[-1]}')

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTime taken: {elapsed_time:.2f} seconds")