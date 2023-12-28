from flask import request
import sqlite3 as sql
import result
import asearch
import requests
import smtplib
import re
from email.mime.text import MIMEText
from datetime import datetime
from urllib.parse import urlparse, parse_qs, unquote

def match():
    # Connect to the SQLite database
    con = sql.connect("/home/ubuntu/course/database.db")
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
            print(parsed_product_link)

            """  # Remove 'qid' from the query parameters
            query_params1 = parse_qs(parsed_final_link.query)
            query_params2 = parse_qs(parsed_product_link.query)
            tracking_parameters = ['qid', 'ref', 'pf_rd_p', 'pf_rd_r', 'smid', 'psc']
            for param in tracking_parameters:
                query_params1.pop(param, None)
                query_params2.pop(param, None) """

            """ print(parsed_final_link.netloc)
            print(parsed_final_link.path)
            print(query_params1)
            print("space")
            print(parsed_product_link.netloc)
            print(parsed_product_link.path)
            print(query_params2) """
        
            # # Extract the product ID from the URLs
            # product_id_final_link = parsed_final_link.path.split('/')[3]
            # product_id_product_link = parsed_product_link.path.split('/')[3]
            # Extract the product ID from the URLs

            # Decode the query part of the URL
            query_final_link = parse_qs(parsed_final_link.query)
            query_product_link = parse_qs(parsed_product_link.query)

            # Extract the 'url' parameter from the query
            url_final_link = unquote(query_final_link.get('url', [''])[0])
            url_product_link = unquote(query_product_link.get('url', [''])[0])

            print("Final link URL:", url_final_link)
            print("Product link URL:", url_product_link)

            # Use the regular expression to search for the product ID in the 'url' parameter
            product_id_final_link = re.search(r'/(dp|gp)/(\w+)', url_final_link)
            product_id_product_link = re.search(r'/(dp|gp)/(\w+)', url_product_link)

            print("Final link match:", product_id_final_link)
            print("Product link match:", product_id_product_link)

            if product_id_final_link and product_id_product_link:
                # Compare the product IDs
                if product_id_final_link.group(2) == product_id_product_link.group(2):
                    today = datetime.now().strftime('%Y-%m-%d-%H:%M')
                    cur.execute("""INSERT INTO stats (fav_id, product_price_stats, price_date_stats) VALUES (?, ?, ?)""", (id, new_product_price, today))
                    # message = MIMEText("The price of " + id + "is now" + new_product_price)
                    # message["From"] = "zcameronwebb@icloud.com"
                    # message["To"] = cur.execute("SELECT email FROM login WHERE username = ?", session["username"])
                    # message["Subject"] = "Price Update"

                    # mail_server = smtplib.SMTP("smtp.mail.me.com", 587)
                    # mail_server.starttls()
                    # mail_server.login("zcameronwebb@icloud.com", "z.aCapril.30!")
                    # mail_server.send_message(message)
                    # mail_server.quit()
                    print("LINK FOUND")

                    con.commit()
                else:
                    print("No link found - error inserting into Status DB")
            else:
                print("not even a match")

           
            
                
            
    con.commit()  # Commit the transaction
    con.close()

# Call the function
match()
print("all good")

