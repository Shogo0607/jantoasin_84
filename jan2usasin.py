import time
from numpy import ma
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import pickle
import glob
import os
from selenium_stealth import stealth
import ray
import streamlit as st
import datetime

price_list = list()
asin_list = list()
item_list = list()

def driver_set():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument('--log-level=1')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-desktop-notifications')
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(3)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    return driver

def dir_exist(dir_name):
    if not os.path.exists(dir_name):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(dir_name)

def click_button(driver, xpath_button):
    button = driver.find_element_by_xpath(xpath_button)
    button.click()

def input_text(driver, input_xpath, input_text):
    input_element = driver.find_element_by_xpath(input_xpath)
    input_element.send_keys(input_text)
  

def save_csv(data, file_path):
    with open(file_path, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(data)

def get_product_title(driver,product_title_xpath):
    try:
        product_title = driver.find_element_by_xpath(product_title_xpath).text
      
    except:
        product_title = ''
    return product_title

def get_asin(driver):
    asin = ""
    for i in range(1,10):
        try:
            asin_text_xpath = '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i)+']/th'
            asin_text = driver.find_element_by_xpath(asin_text_xpath).get_attribute("textContent")
            if "ASIN" in asin_text:
                asin_xpath = '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i)+']/td'
                asin = driver.find_element_by_xpath(asin_xpath).get_attribute("textContent")
                break
        except:
            asin = ""
    return asin

def get_asin2(driver):
    asin = ""
    for i in range(1,20):
        try:
            asin_text_xpath = '//*[@id="detailBullets_feature_div"]/ul/li['+str(i)+']/span/span[1]'
            asin_text = driver.find_element_by_xpath(asin_text_xpath).get_attribute("textContent")
            if "ASIN" in asin_text:
                asin_xpath = '//*[@id="detailBullets_feature_div"]/ul/li['+str(i)+']/span/span[2]'
                asin = driver.find_element_by_xpath(asin_xpath).get_attribute("textContent")
                break
        except:
            asin = ""
        try:
            asin_text_xpath = '//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i)+']/th'
            asin_text = driver.find_element_by_xpath(asin_text_xpath).get_attribute("textContent")
            if "ASIN" in asin_text:
                asin_xpath = '//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i)+']/td'
                asin = driver.find_element_by_xpath(asin_xpath).get_attribute("textContent")
                break
        except:
            pass

    return asin

def read_link(keyword,page_number):
    note = []
    try:
        driver = driver_set()
        driver.get(f"https://www.amazon.com/s?k={keyword}&page={page_number}")
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver=driver, timeout=30)
        wait.until(EC.presence_of_all_elements_located)
        note.append("Amazonへのアクセス可能・")
    except:
        note.append("Amazonへのアクセス不可・")
        wait.until(EC.presence_of_all_elements_located)
        driver.close()
    
    try:
        # xpath一覧
        products_link_xpath = "//h2/a"
        # 商品リンク一覧取得
        products = driver.find_elements_by_xpath(products_link_xpath)
        links = [product.get_attribute('href') for product in products]
        if len(links) == 0:
            note.append("検索結果なし・")
            links = "None"
        else:
            note.append("検索結果あり・")
    except:
        links ="None"
        note.append("リンク取得不可・")

    print("#############LINK##################",keyword,links)
    wait.until(EC.presence_of_all_elements_located)
    driver.close()
    return links,note

def read_link2(keyword,page_number):
    note = []
    try:
        driver = driver_set()
        driver.get(f"https://www.amazon.co.jp/s?k={keyword}&page={page_number}&language=en-US")
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver=driver, timeout=30)
        wait.until(EC.presence_of_all_elements_located)
        note.append("Amazonへのアクセス可能・")
    except:
        note.append("Amazonへのアクセス不可・")
        wait.until(EC.presence_of_all_elements_located)
        driver.close()
    
    try:
        # xpath一覧
        products_link_xpath = "//h2/a"
        # 商品リンク一覧取得
        products = driver.find_elements_by_xpath(products_link_xpath)
        links = [product.get_attribute('href') for product in products]
        if len(links) == 0:
            note.append("検索結果なし・")
            links = "None"
        else:
            note.append("検索結果あり・")
    except:
        links ="None"
        note.append("リンク取得不可・")

    print("#############LINK##################",keyword,links)
    wait.until(EC.presence_of_all_elements_located)
    driver.close()
    return links,note

@ray.remote
def main(keyword,mode):
    page_number = 1
    if mode == "US版":
        path = "./3_HISTORY/US/exist_links/"+str(keyword)+'.pkl'
        path2 = "./3_HISTORY/US/no_links/"+str(keyword)+'.pkl'
    else:
        path = "./3_HISTORY/JP/exist_links/"+str(keyword)+'.pkl'
        path2 = "./3_HISTORY/JP/no_links/"+str(keyword)+'.pkl'

    if os.path.exists(path) or os.path.exists(path2):
        links = "already"
        print(str(keyword) +"  "+ "Already searched")
    else:
        if mode == "US版":
            links,note = read_link(keyword,str(page_number))
        else:
            links,note = read_link2(keyword,str(page_number))

    if links == "already":
        pass
    elif links == "None":
        with open(path2, 'ab') as f:
            product_detail = [keyword,"","","",note]
            pickle.dump(product_detail, f)
    else:
        for link in links:
            note2 = []
            note2.extend(note)
            try:
                driver.close()
            except:
                pass
            try:
                driver = driver_set()
                driver.get(link)
                wait = WebDriverWait(driver=driver, timeout=30)
                print(driver.title)
                wait.until(EC.presence_of_all_elements_located)
                note2.append("商品ページへアクセス可能")
            except:
                note2.append("商品ページへアクセス不可")

            try:
                product_title_xpath = "//span[contains(@id, 'productTitle')]" 
                product_title = get_product_title(driver,product_title_xpath)
                note2.append("商品タイトル取得可能")
                
            except:
                product_title =""
                note2.append("商品タイトル取得不可")

            if mode == "US版":
                try:
                    asin = get_asin(driver)
                    note2.append("ASIN取得可能")
                except:
                    asin = ""
                    note2.append("ASIN取得不可")
            else:
                try:
                    asin = get_asin2(driver)
                    note2.append("ASIN取得可能")
                except:
                    asin = ""
                    note2.append("ASIN取得不可")

            product_detail = [keyword, product_title,asin,link,note2]
            with open(path, 'ab') as f:
                pickle.dump(product_detail, f)
            try:
                driver.close()
            except:
                pass

    return str(keyword)+"END"

if __name__ == "__main__":
    dt_now = datetime.datetime.now()
    filename_dt = dt_now.strftime('%Y年%m月%d日%H時%M分')
    st.set_page_config(page_title="JANtoASIN")
    dir_list = ["./1_INPUT","./2_RESULT","./3_HISTORY","./3_HISTORY/JP","./3_HISTORY/US","./3_HISTORY/JP/no_links","./3_HISTORY/JP/exist_links","./3_HISTORY/US/no_links","./3_HISTORY/US/exist_links","./2_RESULT/US","./2_RESULT/JP/"]
    for dir_name in dir_list:
        dir_exist(dir_name)

    st.title("JANtoASIN")
    st.sidebar.title("JANtoASIN")
    st.subheader("①入力データ")
    file = st.sidebar.file_uploader("XLSXファイルを入れてください。",type=["xlsx"])
    if not file:
        st.warning("カラムに「JAN/EAN」と書いて、その下にJANコードを記入したXLSXファイルを入れてください。")
        st.stop()

    st.success("データ入力完了")
    st.subheader("②データ読み込み")
    df = pd.read_excel(file)
    st.dataframe(df)
    try:
        keywords = df["JAN/EAN"].values.tolist()
    except:
        st.warning("カラムに「JAN/EAN」と記入してあるか確認をしてください。")
    st.success("データ読み込み完了")

    st.subheader("③US版or日本版")
    mode = st.sidebar.selectbox("US版or日本版",["US版","日本版"])
    st.success(mode+"を選択中")
    pkl_list =[]
    with st.spinner("過去の履歴を検索しています・・・"):
        if mode =="US版":
            for keyword in keywords:
                try:
                    pkl_list.extend(glob.glob("./3_HISTORY/US/exist_links/"+str(keyword)+".pkl"))
                except:
                    pass
                try:
                    pkl_list.extend(glob.glob("./3_HISTORY/US/no_links/"+str(keyword)+".pkl"))
                except:
                    pass
        else:
            for keyword in keywords:
                try:
                    pkl_list.extend(glob.glob("./3_HISTORY/JP/exist_links/"+str(keyword)+".pkl"))
                except:
                    pass
                try:
                    pkl_list.extend(glob.glob("./3_HISTORY/JP/no_links/"+str(keyword)+".pkl"))
                except:
                    pass
        test_list = list()
        for pkl in pkl_list:
            with open(pkl, 'rb') as f:
                while True:
                    try:
                        test = pickle.load(f)
                        test_list.append(test)
                    except:
                        break  
        no_asin_list = []       
        if not test_list == []:
            product_details = pd.DataFrame(test_list)
            product_details.columns = ["JAN","商品名","ASIN","URL","注釈"]
            
            for i in range(len(product_details)): 
                if product_details["ASIN"].iloc[i] == "":
                    no_asin_list.append(product_details["JAN"].iloc[i])

        for no_asin in no_asin_list:
            if mode =="US版":
                try:
                    os.remove("./3_HISTORY/US/exist_links/"+str(no_asin)+".pkl")
                except:
                    pass
                try:
                    os.remove("./3_HISTORY/US/no_links/"+str(no_asin)+".pkl")
                except:
                    pass
            else:
                try:
                    os.remove("./3_HISTORY/JP/exist_links/"+str(no_asin)+".pkl")
                except:
                    pass
                try:
                    os.remove("./3_HISTORY/JP/no_links/"+str(no_asin)+".pkl")
                except:
                    pass

    # if mode =="US版":
    #     pkl_list = glob.glob("./3_HISTORY/US/exist_links/*.pkl")
    #     pkl_list.extend(glob.glob("./3_HISTORY/US/no_links/*.pkl"))
    # else:
    #     pkl_list = glob.glob("./3_HISTORY/JP/exist_links/*.pkl")
    #     pkl_list.extend(glob.glob("./3_HISTORY/JP/no_links/*.pkl"))

    # 仕様変更
    # try:
    #     for pklist in pkl_list:
    #         os.remove(pklist)
    # except:
    #     pass

    st.subheader("③ASIN検索")
    if st.sidebar.button("検索実行"):
        
        ray.shutdown()
        ray.init(ignore_reinit_error=True,num_cpus=4)
        with st.spinner("現在検索中です・・・"):
            futures = [main.remote(keyword,mode) for keyword in keywords]
            for future in futures:
                _ = ray.get(future)
        ray.shutdown()
        pkl_list = []
        with st.spinner("結果をまとめています・・・"):
            if mode =="US版":
                for keyword in keywords:
                    try:
                        pkl_list.extend(glob.glob("./3_HISTORY/US/exist_links/"+str(keyword)+".pkl"))
                    except:
                        pass
                    try:
                        pkl_list.extend(glob.glob("./3_HISTORY/US/no_links/"+str(keyword)+".pkl"))
                    except:
                        pass
            else:
                for keyword in keywords:
                    try:
                        pkl_list.extend(glob.glob("./3_HISTORY/JP/exist_links/"+str(keyword)+".pkl"))
                    except:
                        pass
                    try:
                        pkl_list.extend(glob.glob("./3_HISTORY/JP/no_links/"+str(keyword)+".pkl"))
                    except:
                        pass
                    
            test_list = list()
            for pkl in pkl_list:
                print(pkl)
                with open(pkl, 'rb') as f:
                    while True:
                        try:
                            test = pickle.load(f)
                            test_list.append(test)
                        except:
                            break         
        
        product_details = pd.DataFrame(test_list)
        product_details.columns = ["JAN","商品名","ASIN","URL","注釈"]
        st.dataframe(product_details)
        if mode =="US版":
            product_details.to_excel("./2_RESULT/US/"+filename_dt+"_検索結果.xlsx",encoding="utf-8-sig",index=False)
        else:
            product_details.to_excel("./2_RESULT/JP/"+filename_dt+"_検索結果.xlsx",encoding="utf-8-sig",index=False)
        


