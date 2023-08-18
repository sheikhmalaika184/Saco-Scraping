from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import csv

#change this driver path
DRIVER_PATH = '/Users/malaikasheikh/python/chromedriver'
Street_name = "Zachary LN"

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

driver.get('https://gis.vgsi.com/sacome/Search.aspx')
time.sleep(2)

# input street 
street_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "MainContent_txtSearchAddress"))
)
street_field.clear()
street_field.send_keys(Street_name)

# Click the "Search" button
search_button = driver.find_element(By.XPATH, "//span[@class='btn btn-primary']")
search_button.click()
time.sleep(4)

def get_basic_info():
    try:
        data = {"Location":"None","MBLU":"None","Account No":"None","Owner":"None","Assesment":"None",
                "PID":"None","Building Count":"None","User Field 4":"None","User Field 5":"None",
                "TopoTopography":"None","Utility":"None","Location 2":"None","Street Road":"None"}
        tab1 = driver.find_element(By.XPATH, "//div[@id='tabs-1']")
        data["Location"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblLocation']").text
        data["MBLU"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblMblu']").text
        data["Account No"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblAcctNum']").text
        data["Owner"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblGenOwner']").text
        data["Assesment"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblGenAssessment']").text
        data["PID"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblPid']").text
        data["Building Count"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblBldCount']").text
        data["User Field 4"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblUf04']").text
        data["User Field 5"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblUf05']").text
        data["TopoTopography"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblPrcTopo']").text
        data["Utility"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblPrcUtil']").text
        data["Location 2"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblPrcLocn']").text
        data["Street Road"] = tab1.find_element(By.XPATH, "//span[@id='MainContent_lblPrcRoad']").text
    except:
        pass
    finally:
        return data

def get_current_value():
    try:
        data = {"Current Valuation Year":"None","Current Improvements":"None",
                "Current Land":"None","Current Total":"None"}
        tab3 = driver.find_element(By.XPATH, "//div[@id='tabs-3']")
        tr_tag = tab3.find_element(By.XPATH, "//tr[@class='RowStyle']")
        td_tags = tr_tag.find_elements(By.TAG_NAME, "td")
        data["Current Valuation Year"] = td_tags[0].text
        data["Current Improvements"] = td_tags[1].text
        data["Current Land"]  = td_tags[2].text
        data["Current Total"] = td_tags[3].text
    except:
        pass
    finally:
        return data

def get_owner_of_record():
        try:
          data = {"Current Owner":"None","Current Co Owner":"None","Address":"None","Current Sale Price":"None",
                  "Current Certificate":"None","Current Book Page":"None", "Current Sale Date":"None","Current Instrument":"None"}
          tab2 = driver.find_element(By.XPATH, "//div[@id='tabs-2']")
          data["Current Owner"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblOwner']").text
          data["Current Sale Price"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblPrice']").text
          data["Current Certificate"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblCertificate']").text
          data["Current Book Page"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblBp']").text
          data["Current Sale Date"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblSaleDate']").text
          data["Current Co Owner"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblCoOwner']").text
          data["Address"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblAddr1']").text
          data["Current Instrument"] = tab2.find_element(By.XPATH, "//span[@id='MainContent_lblInstrument']").text
        except:
            pass
        finally:
            return data

def get_ownership_history():
    try:
      data = {"Previous Owners": [], "Previous Sale Prices": [], "Previous Certificates": [], "Previous Books & Pages": [],
              "Previous Instruments": [], "Previous Sale Dates": []}
      tab2 = driver.find_element(By.XPATH, "//div[@id='tabs-2']")
      table_tag = tab2.find_element(By.XPATH, "//table[@id='MainContent_grdSales']")
      tr_tags = table_tag.find_elements(By.TAG_NAME, "tr")
      if(len(tr_tags) > 2):
          tr_tags = tr_tags[2:]
          for tr in tr_tags:
              td_tags = tr.find_elements(By.TAG_NAME, "td")
              if(len(td_tags) == 6):
                  data["Previous Owners"].append(td_tags[0].text)
                  data["Previous Sale Prices"].append(td_tags[1].text)
                  data["Previous Certificates"].append(td_tags[2].text)
                  data["Previous Books & Pages"].append(td_tags[3].text)
                  data["Previous Instruments"].append(td_tags[4].text)
                  data["Previous Sale Dates"].append(td_tags[5].text)
              elif(len(td_tags) == 5):
                  data["Previous Owners"].append(td_tags[0].text)
                  data["Previous Sale Prices"].append(td_tags[1].text)
                  data["Previous Certificates"].append(td_tags[2].text)
                  data["Previous Books & Pages"].append(td_tags[3].text)
                  data["Previous Sale Dates"].append(td_tags[4].text)
                  

    except:
        pass
    finally:
        return data

def get_building_info():
    try:
      data = {"Gross Area":"None", "Living Area":"None", "Building":"None", "Section":"None","Year Built":"None",
              "Replacement Cost":"None","Building Percent Good":"None","Replacement cost less depreciation":"None"}
      tab4 = driver.find_element(By.XPATH, "//div[@id='tabs-4']")
      building_section = tab4.find_element(By.XPATH, "//span[@id='MainContent_ctl02_lblHeading']").text
      building_section = building_section.split(":")
      data["Building"] = building_section[0].replace("Building", "").strip()
      data["Section"]= building_section[1].replace("Section", "").strip()
      data["Year Built"] = tab4.find_element(By.XPATH, "//span[@id='MainContent_ctl02_lblYearBuilt']").text
      data["Living Area"]= tab4.find_element(By.XPATH, "//span[@id='MainContent_ctl02_lblBldArea']").text
      data["Replacement Cost"] = tab4.find_element(By.XPATH, "//span[@id='MainContent_ctl02_lblRcn']").text
      data["Building Percent Good"] = tab4.find_element(By.XPATH, "//span[@id='MainContent_ctl02_lblPctGood']").text
      data["Replacement cost less depreciation"] = tab4.find_element(By.XPATH, "//span[@id='MainContent_ctl02_lblRcnld']").text

      table_tag = tab4.find_element(By.XPATH, "//table[@id='MainContent_ctl02_grdCns']")
      tr_tags = table_tag.find_elements(By.TAG_NAME, "tr")
      tr_tags = tr_tags[1:]
      for tr_tag in tr_tags:
          td_tags = tr_tag.find_elements(By.TAG_NAME, "td")
          key = td_tags[0].text.replace(":","")
          data[key] = td_tags[1].text
      
      table_tag = tab4.find_element(By.XPATH, "//table[@id='MainContent_ctl02_grdSub']")
      tr_tags = table_tag.find_elements(By.TAG_NAME, "tr")
      if(len(tr_tags) > 0):
          tr = tr_tags[-1]
          td_tags = tr.find_elements(By.TAG_NAME, "td")
          data["Gross Area"] = td_tags[2].text
          
    except:
        pass
    finally:
        return data

def get_land_info():
    try:
        data = {"Use Code":"None", "Description":"None", "Zone":"None", "Neighborhood":"None", "Alt Land Appr":"None",
                "Category":"None", "Size (Acres)":"None", "Frontage":"None", "Depth":"None", "Assessed Value":"None"}
        tab6 = driver.find_element(By.XPATH, "//div[@id='tabs-6']")
        data["Use Code"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblUseCode']").text
        data["Description"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblUseCodeDescription']").text
        data["Zone"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblZone']").text
        data["Neighborhood"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblNbhd']").text
        data["Alt Land Appr"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblAltApproved']").text
        data["Category"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblLndCategory']").text
        data["Size (Acres)"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblLndAcres']").text
        data["Frontage"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblLndFront']").text
        data["Depth"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblDepth']").text
        data["Assessed Value"] = tab6.find_element(By.XPATH, "//span[@id='MainContent_lblLndAsmt']").text

    except:
        pass
    finally:
        return data

def get_valuation_history():
    try:
        data={"Valuation Year history":[],"Improvements history":[],"Land history":[],"Total History":[]}
        tab7 = driver.find_element(By.XPATH, "//div[@id='tabs-7']")
        table_tag = tab7.find_element(By.XPATH, "//table[@id='MainContent_grdHistoryValuesAsmt']")
        tr_tags = table_tag.find_elements(By.TAG_NAME, "tr")
        tr_tags = tr_tags[1:]
        for tr in tr_tags:
            td_tags = tr.find_elements(By.TAG_NAME, "td")
            data["Valuation Year history"].append(td_tags[0].text)
            data["Improvements history"].append(td_tags[1].text)
            data["Land history"].append(td_tags[2].text)
            data["Total History"].append(td_tags[3].text)

    except:
        pass
    finally:
        return data

def save_data(basic_data,current_value_data,owner_data,ownership_history_data,building_data,land_data,valuation_history_data):
    file_path = 'saco_data.csv'
    if not os.path.isfile(file_path):
        column_names = ["Location","MBLU","Account No","Owner","Assesment","PID","Building Count","User Field 4","User Field 5",
                "TopoTopography","Utility","Location 2","Street Road","Current Valuation Year","Current Improvements",
                "Current Land","Current Total","Current Owner","Current Co Owner","Address","Current Sale Price",
                "Current Certificate","Current Book Page", "Current Sale Date","Current Instrument","Previous Owners",
                "Previous Sale Prices", "Previous Certificates", "Previous Books & Pages","Previous Instruments", "Previous Sale Dates",
                'Gross Area', 'Living Area', 'Building', 'Section', 'Year Built', 'Replacement Cost', 'Building Percent Good',
                'Replacement cost less depreciation', 'Style', 'Model', 'Grade', 'Stories', 'Occupancy', 'Exterior Wall 1', 
                'Exterior Wall 2', 'Roof Structure', 'Roof Cover', 'Interior Wall 1', 'Interior Wall 2', 'Interior Flr 1', 
                'Interior Flr 2', 'Heat Fuel', 'Heat Type', 'AC Type', 'Total Bedrooms', 'Total Bthrms', 'Total Half Baths', 
                'Total Xtra Fixtrs', 'Total Rooms', 'Bath Style', 'Kitchen Style', 'Num Kitchens', 'Cndtn', 
                'Num Park', 'Fireplaces', 'Fndtn Cndtn', 'Basement',"Use Code", "Description", "Zone", "Neighborhood","Alt Land Appr",
                "Category", "Size (Acres)", "Frontage", "Depth", "Assessed Value","Valuation Year history","Improvements history",
                "Land history","Total History"]
        df = pd.DataFrame(columns=column_names)
        # Save the DataFrame as a CSV file
        df.to_csv(file_path, index=False)
    merged_dict = {}
    merged_dict.update(basic_data)
    merged_dict.update(current_value_data)
    merged_dict.update(owner_data)
    merged_dict.update(ownership_history_data)
    merged_dict.update(building_data)
    merged_dict.update(land_data)
    merged_dict.update(valuation_history_data)
    df = pd.read_csv(file_path)
    if(len(merged_dict) == 82):
        # Create a DataFrame with column names
        df = pd.DataFrame(columns=merged_dict.keys())
        df = df.append(merged_dict, ignore_index=True)
        df.to_csv(file_path, mode='a', index=False, header =  False)

def get_info(urls):
    print(len(urls))
    i = 1
    urls = urls[:]
    for url in urls:
        try:
            print(i)
            driver.get(url)
            time.sleep(2)
            basic_data = get_basic_info()
            current_value_data = get_current_value()
            owner_data = get_owner_of_record()
            ownership_history_data = get_ownership_history()
            building_data = get_building_info()
            land_data = get_land_info()
            valuation_history_data = get_valuation_history()
            save_data(basic_data,current_value_data,owner_data,ownership_history_data,building_data,land_data,valuation_history_data)
            i = i + 1
        except:
            continue
urls = []
current_page = 1
def get_urls():
    global urls
    global current_page
    table_tag = driver.find_element(By.XPATH, "//table[@id='MainContent_grdSearchResults']")
    tr_tags = table_tag.find_elements(By.TAG_NAME, "tr")
    tr_tags = tr_tags[1:]
    for tr in tr_tags:
      try:
        td_tags = tr.find_elements(By.TAG_NAME, "td")
        pid = td_tags[7].text
        urls.append(f"https://gis.vgsi.com/sacome/Parcel.aspx?pid={pid}")
      except:
          continue
    # for pagination
    try:
        pager = table_tag.find_element(By.XPATH, "//tr[@class='PagerStyle']")
        td_tags = pager.find_elements(By.TAG_NAME, "td")
        if(len(td_tags) > current_page):
            a_tag = td_tags[current_page]
            current_page = current_page + 1
            a_tag.click()
            time.sleep(2)
            get_urls()
    except Exception as e:
        pass
    urls = list(set(urls))
    return urls

urls = get_urls()
get_info(urls)

driver.quit()