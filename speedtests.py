# -*- coding: utf-8 -*-
import re
import time
import datetime
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

pattern2 = r'title="Download Latency".*?<span class="result-data-value">(\d+)</span>.*?title="Upload Latency".*?<span class="result-data-value">(\d+)</span>'
pattern3 = r'title="Download Latency".*?<span class="result-data-value">(\d+)</span>.*?title="Upload Latency".*?<span class="result-data-value">(\d+)</span>'
ptn_matches_result_value_span =  r'<span class="result-data-value">(\d+)<\/span>'


debug=[1, 48, "06:00","12:00","18:00",2]
release=[2,"06:00","12:00","18:00",2]


def xtract_speeds_from_html(html):
    speeds_report_string = ""
    matches = re.findall(r'<span class="result-data-value">(\d+)<\/span>', html) # speedtest.net - specific naming may need change in future
    download_speed = matches[1]
    upload_speed = matches[2] #re.search(r'<span class="result-data-value">(\d+)<\/span>', html).group(0)[2]
    # Check if a match was found
 
    speeds_report_string = f'Download Speed: {download_speed} mbit/s, Upload Speed: {upload_speed} mbit/s'
    #print(speeds_report_string)
    
    return speeds_report_string
# Funktion zum Starten des Speedtests und Speichern der URL
def process_speed_test():
    # Chrome-Optionen setzen
    chrome_options = Options()
    
    options = Options()
    options.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
    driver_path = "C:/Program Files/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    
    chrome_options.add_argument("--headless")  # Optionale Kopflos-Ausführung des Browsers

    # WebDriver initialisieren

    try:
        print("try accessing website")
        # Auf speedtest.net gehen
        driver.get("https://www.speedtest.net/result/17451389016")
        time.sleep(debug[0])  # Warten auf die Weiterleitung
        try:
            reject_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
            reject_button.click()
            print("Cookies abgelehnt.")
        except Exception as e:
            print("Ablehn-Button nicht gefunden oder bereits abgelehnt:", e)
        time.sleep(1)
        current_time = datetime.datetime.now()
        

        div_element = driver.find_element(By.CLASS_NAME, "result-container-speed")
        html_content = div_element.get_attribute("outerHTML")
        speeds_report_string = xtract_speeds_from_html(html_content)
            
        
        # Die URL in einer Textdatei speichern
        with open("redirected_urls.txt", "a") as file:          
            # Log the current date and time to the console
            
            file.write(" TIME: " + str(current_time) + " RESULT: " + "url-not-important-here" + speeds_report_string + "\n")
            print("speedtest url written to file.")
    except Exception as e:
        print(f"Fehler beim Ausführen des Speedtests: {e}")

    finally:
        # Browser schließen
        driver.quit()
        
        
        
def rerun_speed_test():
    # Chrome-Optionen setzen
    chrome_options = Options()
    
    options = Options()
    options.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
    driver_path = "C:/Program Files/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    
    chrome_options.add_argument("--headless")  # Optionale Kopflos-Ausführung des Browsers

    # WebDriver initialisieren
   
            
    try:
        print("try accessing website")
        # Auf speedtest.net gehen
        driver.get("https://www.speedtest.net")
        time.sleep(debug[0])  # Warten auf die Weiterleitung
        try:
            reject_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
            reject_button.click()
            print("Cookies abgelehnt.")
        except Exception as e:
            print("Ablehn-Button nicht gefunden oder bereits abgelehnt:", e)
        time.sleep(1)
        current_time = datetime.datetime.now()
        # Auf den Button mit aria-label="start speed test - connection type multi" klicken
        button = driver.find_element(By.XPATH, '//*[contains(@aria-label, "start speed test - connection type multi")]') #speedtest.net - specific naming may need change in future
        button.click()

        # Warten, bis der Test abgeschlossen ist oder die Weiterleitung passiert
        time.sleep(debug[1])  # Warten auf die Weiterleitung

        # Die aktuelle URL ausgeben
        redirected_url = driver.current_url
        print("Redirected URL:", redirected_url)
        speeds_report_string = ""

        span1 = driver.find_elements(By.CSS_SELECTOR, '.result-data-large , .number , .result-data-value ,  .download-speed')[0]
        span2 = driver.find_elements(By.CSS_SELECTOR, '.result-data-large , .number , .result-data-value ,  .upload-speed')[1]
# speedtest.net - specific naming may need change in future
        speeds_report_string = " Down: " + span1.text +" Mbps "+ " Up: " + span2.text + " Mbps"
        

        # Die URL in einer Textdatei speichern
        with open("redirected_urls.txt", "a") as file:          
            # Log the current date and time to the console
            
            file.write(" TIME: " + str(current_time) + " RESULT: " + redirected_url + speeds_report_string + "\n")
            print("speedtest url written to file.")
    except Exception as e:
        print(f"Fehler beim Ausführen des Speedtests: {e}")

    finally:
        # Browser schließen
        driver.quit()

# Zeitplan für das Skript
schedule.every().day.at(debug[2]).do(rerun_speed_test)
schedule.every().day.at(debug[3]).do(rerun_speed_test)
schedule.every().day.at(debug[4]).do(rerun_speed_test)

# Endlosschleife, die den Zeitplan überprüft
while True:
    print("check again now!")
    schedule.run_pending()
    time.sleep(60)  # Alle 60 Sekunden überprüfen
    
dummyhtml = '''
            <div class="result-item-details">


              <div class="result-item result-item-ping" title="Reaction Time">
                <span class="result-label">
                  Ping
                </span>
                <span class="result-data-unit">ms</span>
                <span class="result-data-latency-item" title="Idle Latency">
                  <svg class="svg-icon svg-icon-bump"><use xlink:href="#icon-ping"></use></svg>
                  <span class="result-data-value">17</span>
                </span>

                  <span class="result-data-latency-item" title="Download Latency">
                    <svg class="svg-icon icon-download test-mode-multi"><use xlink:href="#icon-download"></use></svg>
                    <span class="result-data-value">98</span>
                  </span>

                  <span class="result-data-latency-item" title="Upload Latency">
                    <svg class="svg-icon icon-upload test-mode-multi"><use xlink:href="#icon-upload"></use></svg>
                    <span class="result-data-value">32</span>
                  </span>
              </div>



        </div>'''
# print(dummyhtml)
# print(xtract_speeds_from_html(dummyhtml))

rerun_speed_test()