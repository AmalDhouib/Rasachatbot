from flask import Flask, jsonify, render_template,send_file, redirect, url_for, session
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import re
import numpy as np


app = Flask(__name__)
app.secret_key = 'amal'
@app.route('/')
def index():
    """Render the main page."""
    return render_template('acueil.html')


def scrape_data():
    # Path to chromedriver.exe with raw string literal
    path = r"C:\Users\21697\OneDrive\Bureau\chromedriver-win64\chromedriver.exe"
    service = Service(path)

    # Initialize the Chrome WebDriver with the service
    driver = Chrome(service=service)

    # URL of the website to scrape
    url = "https://lespepitestech.com"
    driver.get(url)
    time.sleep(4)
    
    # Scroll and collect data
    names = []
    sites_web = []
    secteurs = []
    descriptions = []

    for i in range (0,3):

        last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(4)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        elements = soup.find_all('div', class_='s-e-title-c')
        for article in elements:
            h3 = article.find('h3')
            if h3 and h3.text.rstrip("0123456789") not in names:
                names.append(h3.text.rstrip("0123456789"))

        try:
            secteur1 = soup.select('div.lpt-dropdown-counter a')
            secteur1 = [sc.text for sc in secteur1]

            nombre = soup.select('span.count')
            nombre = [int(nb.text.strip("+ ")) for nb in nombre]

            i = 0
            for nb in nombre:
                if ",".join(secteur1[i:i+nb+1]) not in secteurs:
                    secteurs.append(",".join(secteur1[i:i+nb+1]))
                i = i + nb + 1
        except:
            secteurs.append("")

        description = soup.select('div.s-u-summary')
        for d in description:
            if d.text not in descriptions:
                descriptions.append(d.text)

        els = soup.find_all('a', class_='startup-entry-hitbox')
        for element in els:
            href_value = element.get('href')
            if href_value and "https://lespepitestech.com" + href_value not in sites_web:
                sites_web.append("https://lespepitestech.com" + href_value)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
          

    driver.quit()
    return names, sites_web, secteurs, descriptions
def enlever_chiffres(nom):
    """Remove digits from a string."""
    return re.sub(r'\d+', '', nom)

def highlight_not_found(s):
    """Highlight cells with 'NOT FOUND' text."""
    if s == "NOT FOUND":
        return 'color: red'
    else:
        return ''


def process_and_save_data(names, sites_web, secteurs, descriptions, output_path):
    """Process the scraped data and save it to an Excel file."""
    m = min(len(names), len(sites_web), len(secteurs), len(descriptions))
    
    names1 = names[:m]
    sites1 = sites_web[:m]
    secteurs1 = secteurs[:m]
    descriptions1 = descriptions[:m]
    
    coo1 = [enlever_chiffres(nom) for nom in names1]
    linkdinks1 = [""] * m
    jaimes1 = [""] * m

    data = {
        "Name": names1,
        "Website": sites1,
        "LinkedIn": linkdinks1,
        "Coordinator": coo1,
        "Secteur": secteurs1,
        "Description": descriptions1,
        "NB_JAIME": jaimes1
    }

    df = pd.DataFrame(data)
    df.replace("", np.nan, inplace=True)
    styled_df = df.style.applymap(highlight_not_found)
    styled_df.to_excel(output_path, engine='openpyxl', index=False)



@app.route('/scrape')
def scrape():
    """Handle the scraping and prepare the Excel file."""
    names, sites_web, secteurs, descriptions = scrape_data()
    
    file_path = 'scraped_data.xlsx'
    process_and_save_data(names, sites_web, secteurs, descriptions, file_path)
    
    session['file_path'] = file_path
    return redirect(url_for('index') + '?scraped=true')

@app.route('/download')
def download():
    """Send the Excel file for download."""
    file_path = session.get('file_path')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)