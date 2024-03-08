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
print(f"Time taken: {elapsed_time:.2f} seconds")

for ev in event_links:
  r = driver.get(ev)
  fight_elems = driver.find_element(By.CLASS_NAME, "b-fight-details__table-body").find_elements(By.CSS_SELECTOR, ".b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click")
  fight_links.extend([fe.get_attribute('onclick')[7:-2] for fe in fight_elems])

# print length of fight links array, first and last
print(f'\nLength of fights: {len(fight_links)}\nFirst fight: {fight_links[0]}\nLast fight: {fight_links[-1]}')

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")
# specific data scraping function for ufc-stats website
def row_stat_fetcher(row_elem, col):
  return [e.text for e in row_elem[col].find_elements(By.CLASS_NAME, "b-fight-details__table-text")]

# scrape important data from each fight webpage 

fights = []

fight_links = [fight_links[0]]
for fl in fight_links:
  r = driver.get(fl)

  fighter_elems = driver.find_elements(By.CSS_SELECTOR, ".b-link.b-fight-details__person-link")
  fighter1, fighter2 = [el.text for el in fighter_elems]

  result = driver.find_element(By.CSS_SELECTOR, ".b-fight-details__person-status").text.strip()

  method = driver.find_element(By.CSS_SELECTOR, ".b-fight-details__text-item_first").find_elements(By.TAG_NAME, "i")[1].text.strip()

  detail_elems = driver.find_elements(By.CLASS_NAME, "b-fight-details__text-item")

  round_elem = detail_elems[0]
  round_text = round_elem.find_element(By.CSS_SELECTOR, ".b-fight-details__label").text
  round = int(round_elem.text.replace(round_text, '').strip())

  time_elem = detail_elems[1]
  time_text = time_elem.find_element(By.CSS_SELECTOR, ".b-fight-details__label").text
  fight_time = time_elem.text.replace(time_text, '').strip()

  referee = detail_elems[3].find_element(By.TAG_NAME, "span").text.strip()

  stat_elems = driver.find_elements(By.CSS_SELECTOR, ".b-fight-details__table-row")[1].find_elements(By.CSS_SELECTOR, ".b-fight-details__table-col")
  kd1, kd2 = list( map(lambda x: int(x), row_stat_fetcher(stat_elems, 1)) )
  strk1, strk2 = row_stat_fetcher(stat_elems, 4)
  td1, td2 = row_stat_fetcher(stat_elems, 5)
  suba1, suba2 = list( map(lambda x: int(x), row_stat_fetcher(stat_elems, 7)) )
  rev1, rev2 = list( map(lambda x: int(x), row_stat_fetcher(stat_elems, 8)) )
  ctrl1, ctrl2 = row_stat_fetcher(stat_elems, 9)

  sig_stat_elems = driver.find_element(By.CSS_SELECTOR, ".b-fight-details > table").find_elements(By.CSS_SELECTOR, ".b-fight-details__table-row")[1].find_elements(By.CSS_SELECTOR, ".b-fight-details__table-col")
  sigstrk1, sigstrk2 = row_stat_fetcher(sig_stat_elems, 1)
  head1, head2 = row_stat_fetcher(sig_stat_elems, 3)
  body1, body2 = row_stat_fetcher(sig_stat_elems, 4)
  leg1, leg2 = row_stat_fetcher(sig_stat_elems, 5)
  dis1, dis2 = row_stat_fetcher(sig_stat_elems, 6)
  clinch1, clinch2 = row_stat_fetcher(sig_stat_elems, 7)
  grnd1, grnd2 = row_stat_fetcher(sig_stat_elems, 8)

  fights.append(dict({
    "fighter_1": fighter1,
    "fighter_2": fighter2,
    "knockdowns_1": kd1,
    "knockdowns_2": kd2,
    "total_strikes_1": strk1,
    "total_strikes_2": strk2,
    "significant_strikes_1": sigstrk1,
    "significant_strikes_2": sigstrk2,
    "head_strikes_1": head1,
    "head_strikes_2": head2,
    "body_strikes_1": body1,
    "body_strikes_2": body2,
    "leg_strikes_1": leg1,
    "leg_strikes_2": leg2,
    "distance_strikes_1": dis1,
    "distance_strikes_2": dis2,
    "clinch_strikes_1": clinch1,
    "clinch_strikes_2": clinch2,
    "ground_strikes_1": grnd1,
    "ground_strikes_2": grnd2,
    "takedowns_1": td1,
    "takedowns_2": td2,
    "submission_attempts_1": suba1,
    "submission_attempts_2": suba2,
    "reversals_1": rev1,
    "reversals_2": rev2,
    "control_time_1": ctrl1,
    "control_time_2": ctrl2,
    "result": result,
    "method": method,
    "round": round,
    "time": fight_time,
    "referee": referee,
    "ufc_stats_com_url": fl
  }))

df = pd.DataFrame.from_dict(fights)
df.head()

df.to_csv('my_fight_stats.csv', index=False)

print("\nScraped fight details")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")