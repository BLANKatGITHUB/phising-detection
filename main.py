import os
import math
import ipaddress
from urllib.parse import urlparse, parse_qs

from flask import Flask, render_template,request


import pickle




app = Flask(__name__)

filename = './rf_model.pkl'
with open(filename, 'rb') as file:
    loaded_model = pickle.load(file)


def preprocessing(url):
    url_length = len(url)
    dot_count = url.count(".")
    slash_count = url.count("/")
    dash_count = url.count("-")
    underscore_count = url.count("_")
    at_count = url.count("@")
    question_count = url.count("?")
    equal_count = url.count("=")
    and_count = url.count("&")
    digit_count = sum(c.isdigit() for c in url)
    letter_count = sum(c.isalpha() for c in url)
    has_http = int("http" in url)
    has_https = int("https" in url)
    has_www = int("www" in url)

    return [
        url_length,
        dot_count,
        slash_count,
        dash_count,
        underscore_count,
        at_count,
        question_count,
        equal_count,
        and_count,
        digit_count,
        letter_count,
        has_http,
        has_https,
        has_www,
    ]


@app.route("/")
def index():
    return render_template('index.html')

@app.post("/url")
def prediction():
    url = request.form["url"]
    
    x = preprocessing(url)
    value = loaded_model.predict([x])

    if value == 1:
        prediction = "Legitmate"
    else:
        prediction = "Phising"

    return render_template('index.html',prediction=prediction)

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
def shannon_entropy(s):
    """Calculate the Shannon entropy of a string."""
    if not s:
        return 0
    frequencies = {}
    for ch in s:
        frequencies[ch] = frequencies.get(ch, 0) + 1
    entropy = 0
    for freq in frequencies.values():
        p = freq / len(s)
        entropy -= p * math.log2(p)
    return entropy

def is_ip_address(host):
    """Check if host is an IP address."""
    try:
        ipaddress.ip_address(host)
        return 1
    except ValueError:
        return 0

def preprocessing(url):
    url_length = len(url)
    dot_count = url.count(".")
    slash_count = url.count("/")
    dash_count = url.count("-")
    underscore_count = url.count("_")
    at_count = url.count("@")
    question_count = url.count("?")
    equal_count = url.count("=")
    and_count = url.count("&")
    digit_count = sum(c.isdigit() for c in url)
    letter_count = sum(c.isalpha() for c in url)
    # Use startswith to be more specific
    has_http = int(url.startswith("http://"))
    has_https = int(url.startswith("https://"))
    has_www = int("www" in url.lower())

    # Parse URL components using urlparse
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path
    query = parsed.query

    # --- Domain and Subdomain features ---
    # Simple split on '.' to separate subdomains from the registered domain.
    host_parts = host.split('.')
    if len(host_parts) >= 2:
        registered_domain = ".".join(host_parts[-2:])
        subdomains = host_parts[:-2]
    else:
        registered_domain = host
        subdomains = []
    subdomain_count = len(subdomains)
    registered_domain_length = len(registered_domain)
    
    # Check if the host is an IP address
    host_is_ip = is_ip_address(host)
    
    # --- TLD features ---
    # Simple extraction: assume the last part of the registered_domain is the TLD.
    if '.' in registered_domain:
        tld = registered_domain.split('.')[-1]
    else:
        tld = ''
    tld_length = len(tld)
    
    # --- Ratio and Entropy features ---
    digit_letter_ratio = (digit_count / letter_count) if letter_count > 0 else 0
    domain_entropy = shannon_entropy(host)
    
    # --- Path and Query features ---
    # Compute path depth: number of "/" in path (excluding any trailing slash)
    cleaned_path = path.rstrip('/')
    path_depth = len(cleaned_path.split('/')) - 1 if cleaned_path else 0
    
    # Query parameters: count number of key-value pairs in query (using parse_qs)
    query_dict = parse_qs(query)
    query_param_count = len(query_dict)
    
  
    feature_array = [
        url_length,           
        dot_count,            
        slash_count,          
        dash_count,           
        underscore_count,     
        at_count,             
        question_count,       
        equal_count,          
        and_count,            
        digit_count,         
        letter_count,         
        has_http,             
        has_https,            
        has_www,              
        subdomain_count,      
        registered_domain_length,  
        host_is_ip,           
        tld_length,           
        digit_letter_ratio,   
        domain_entropy,       
        path_depth,           
        query_param_count     
    ]
    
    return feature_array