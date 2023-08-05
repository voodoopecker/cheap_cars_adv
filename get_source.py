import time

import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument('--headless=new')
# New class for preventing browser shutdown
# class New_Chrome(uc.Chrome):
#     def __del__(self):
#         pass
# driver = New_Chrome(use_subprocess=True, options=options)
driver = uc.Chrome(use_subprocess=True, options=options)
driver.get('https://auto.ru/sankt-peterburg/cars/all/?top_days=1&with_empty_groups=true&seller_group=PRIVATE&sort=cr_date-desc')
time.sleep(3)
driver.save_screenshot('screenshoot.png')
page = driver.page_source

with open('source.html', 'w', encoding='utf-8') as output_file:
    output_file.write(page)
