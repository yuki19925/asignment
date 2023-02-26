# asignment
First of all,Thank CTW for giving me the opportunity to try to make an API.
It was challenging and fun.
I already do my best.
           write by Tinny

Project Description

This project is a Financial API service that retrieves financial data for IBM and Apple Inc using the AlphaVantage API and stores it in a SQLite database. It also provides endpoints to retrieve and analyze the stored data.

Tech Stack

This API service is built using the following technologies:

Python 3.10.9
Flask
SQLite
Docker
Running the Code Locally

To run the code locally, follow these steps:

Clone the repository to your local machine.
Create a virtual environment using Python 3.10.9
Install the dependencies listed in requirements.txt using pip.
Export your AlphaVantage API key as an environment variable: export ALPHAVANTAGE_API_KEY=<your_api_key>
Run the Flask server: flask run.
The API service will now be available at http://localhost:5000.

Maintaining the AlphaVantage API Key

To maintain the AlphaVantage API key in both local development and production environments, you can store it as an environment variable and access it in your code using os.environ['ALPHAVANTAGE_API_KEY']. In a production environment, you should avoid hard-coding the API key in your code to keep it secure. Instead, you can set the environment variable using your server's configuration tools or container orchestration platform.
