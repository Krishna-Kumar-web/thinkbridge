import csv
import json
import asyncio
from flask import Flask, request, jsonify
from playwright.async_api import async_playwright

app = Flask(__name__)

async def scrape_company_details(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url)
            # Perform scraping and extract the desired data from the page
            # Replace the following lines with your own scraping logic
            company_name = await page.text('.company-name')
            description = await page.text('.description')
            rating = await page.text('.rating')
            
            return {
                'company_name': company_name,
                'description': description,
                'rating': rating
            }
        except Exception as e:
            # Handle any exceptions that occur during scraping
            return {'error': str(e)}
        finally:
            await browser.close()

@app.route('/scrape', methods=['POST'])
async def scrape():
    try:
        csv_file = request.files['csv_file']
        reader = csv.reader(csv_file)
        urls = [row[0] for row in reader]
        
        results = []
        tasks = []
        
        # Scrape each URL asynchronously
        for url in urls:
            task = asyncio.create_task(scrape_company_details(url))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
