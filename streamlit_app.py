import streamlit as st
import requests
import openai
import json

# Replace YOUR_API_KEY with your actual Bing Search API key
BING_API_KEY = st.secrets["BING_API_KEY"]
openai.api_key =  st.secrets["OPENAI_KEY"]
GPT_MODEL = "text-davinci-003"

st.title('cleversearch.ai')

st.header("An AI powered search tool.")


# Create a textbox for the user to input their search query
query = st.text_input("Enter a search query:")

# Send a request to the Bing Search API with the user's search query
# and display the results in the app
if query:
    # Set the headers and parameters for the request
    params = {
        "q": query,
        "textDecorations": True,
        "textFormat": "HTML",
        "count": 4
    }

    # Set the Bing API endpoint and headers
    endpoint = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    
    # Make the request to the Bing API
    response = requests.get(endpoint, headers=headers, params=params)
    # Check the status code of the response
    if response.status_code != 200:
        st.error({"error": response.exceptions.RequestException})
    
    # Get the search results from the response
    results = response.json()["webPages"]["value"]

    # Display the search results in the app
   
    
    temperature = 0.7
    
    article_urls = {}

    for i, result in enumerate(results):
        article_urls[i] = result["snippet"]

    prompt = f"answer this question: {query}, using these references: {article_urls}"
    
    summary = openai.Completion.create(engine=GPT_MODEL, prompt=prompt, temperature=temperature, max_tokens=128)
    st.subheader("AI Response:")
    st.write(summary["choices"][0]["text"])

    st.subheader("References: ")

    for result in results:
        st.write(result["name"])
        st.write(result["url"])
        st.write(result["snippet"])


st.write("Created by Johannes du Plessis")