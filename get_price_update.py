from flask import request
import sqlite3 as sql
import result
import asearch
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs

def match():
    # Connect to the SQLite database
    con = sql.connect("database.db")
    cur = con.cursor()

    # Execute a SQL command to get the search terms from the 'favs' table
    cur.execute('SELECT sterm, id FROM favs')
    rows = cur.fetchall() # Fetch all the rows as a list of tuples

    # Create a dictionary where the keys are ids and the values are search terms
    search_terms_dict = {}
    for row in rows:
        sterm, id = row
        search_terms_dict[id] = sterm

    # For each search term, perform a search and get the list of products
    for id, search in search_terms_dict.items():
        # Perform the search
        r = asearch.search(search)
        jobid = r["job_id"]
        product_list = result.result(jobid)

        # For each product in the list, get its details
        for product in product_list:
            product_link = product["link"]["href"]
            # Get the final redirected URL of the product
            response = requests.get(product_link)
            final_product_link = response.url
            new_product_price = product["price"]

            # Execute a SQL command to get the product link from the 'favs' table
            cur.execute("""SELECT product_link FROM favs WHERE id = ?""", (id,))
            link = cur.fetchone() # Fetch the first row

            # Get the final redirected URL of the link
            response = requests.get(link[0])
            final_link = response.url

            # Parse the URLs
            parsed_final_link = urlparse(final_link)
            parsed_product_link = urlparse(final_product_link)

            # Remove 'qid' from the query parameters
            query_params1 = parse_qs(parsed_final_link.query)
            query_params2 = parse_qs(parsed_product_link.query)
            query_params1.pop('qid', None)
            query_params2.pop('qid', None)

            # If the links match, insert the new price into the 'stats' table
            if (parsed_final_link.netloc, parsed_final_link.path, query_params1) == (parsed_product_link.netloc, parsed_product_link.path, query_params2):
                today = datetime.now().strftime('%Y-%m-%d-%H:%M')
                cur.execute("""INSERT INTO stats (fav_id, product_price, price_date) VALUES (?, ?, ?)""", (id, new_product_price, today))
                con.commit()
            else:
                print("No link found - error inserting into Status DB")

# Call the function
match()
