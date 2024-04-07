[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]

# Stock Recommender with OpenAI Chatbot Integration

Welcome to the GitHub repository for the Stock Recommender system, enhanced with an OpenAI Chatbot interface. This innovative tool is designed to assist users in making informed stock investment decisions by leveraging the power of AI and advanced analytics. 

## Features

- Stock Recommendations: Utilizes advanced algorithms to analyze market trends and provide personalized stock recommendations.
- OpenAI Chatbot Integration: Engage with our AI-powered chatbot for interactive queries about stock insights and investment advice.
- Unit Tests: Ensures reliability and performance through comprehensive unit testing, including tests for the OpenAI chatbot functionalities.

## Demo Videos

Get a closer look at our Stock Recommender system in action through these demo videos:

- [Chatbot Demo](https://youtu.be/M_kXf1QOYpA) 
- [Recommender Demo](https://youtu.be/iXdAlRiB-s0) 

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- streamlit
- rasa
- yfinance
  
Additionally you'll need:
- openai api key


1. Clone the repository:
```bash

git clone https://github.com/ostweg/Stock-Recommender.git
cd Stock-Recommender
```
2. Navigate to Rasa Chatbot, open two terminals & execute it
```bash
cd chatbot
rasa run actions # in first terminal
rasa shell # in second terminal
```
3. Navigate to OpenAI Chabot & execute it
```bash
cd chatbot
streamlit run main.py
```
4. Navigate to Recommender
```bash
cd stockrecolib/recommender
streamlit run app.py
```


[contributors-shield]: https://img.shields.io/github/contributors/ostweg/Stock-Recommender.svg?style=for-the-badge
[contributors-url]: https://github.com/ostweg/Stock-Recommender/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/ostweg/Stock-Recommender.svg?style=for-the-badge
[issues-url]: https://github.com/ostweg/Stock-Recommender/issues
