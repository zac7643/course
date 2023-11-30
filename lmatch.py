from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os
import sqlite3 as sql
import result
import asearch
from datetime import datetime



# Define a function named "match"
def match():
    # Connect to the database
    con = sql.connect("database.db")
    # Create a cursor object
    cur = con.cursor()
    # Execute a SQL query to select the search term from the stats table where the fav_id matches the provided id
    cur.execute(""" 
                SELECT sterm
                FROM stats 
                WHERE fav_id = ? """,
                (id)) # id is not defined in this function
    # Fetch the first row from the result set
    rows = cur.fetchone() 
    # Use the asearch module to search using the search term fetched from the database
    r = asearch.search(rows) 
    # Get the job_id from the result of the search
    jobid = r["job_id"]
    # Use the result module to get the results of the search using the job_id
    o = result.result(jobid) 
    # Execute a SQL query to select the product link from the favs table where the fav_id matches the provided id
    cur.execute("""
                SELECT product_link
                FROM favs 
                WHERE fav_id = ? """,
                (id)) # id is not defined in this function
    # Fetch the first row from the result set
    link = cur.fetchone() 
    # Check if the product link is in the values of the search results
    if link in o.values(): 
        # If it is, print a message indicating that a match was found
        print("match found:" + str(link))
    else:
        # If it isn't, print an error message
        print("error")







#search through o to find the same link found in the results page