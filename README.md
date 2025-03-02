# AI-Stock-Dashboard

## Description

**AI-Stock-Dashboard** is an interactive dashboard that combines financial data visualization with AI-driven analysis. The application fetches real-time stock price data and displays interactive charts with key technical indicators. It leverages a multimodal AI model to analyze stock charts and provide insightful commentary on trends, patterns, and potential signals. By integrating Streamlit for the user interface and an AI vision model for chart analysis, the dashboard helps traders and investors make sense of market movements in an intuitive way.

## Installation and Setup

1. **Clone the Repository** – Download or clone the *AI-Stock-Dashboard* project from the repository to your local machine

2. **Install Dependencies** – Navigate to the project directory and install required packages:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the AI Model** – Install [Ollama](https://ollama.com) and download the Llama 3.2 Vision model. You can pull the model by running. This step ensures the AI model for image (chart) analysis is available locally:
```bash
ollama pull llama3.2-vision
```

4. Launch the AI Backend – In a separate terminal, start the Llama 3.2 Vision model service with Ollama:
```bash
ollama run llama3.2-vision
```

6. Run the Streamlit App – Start the dashboard web application by running the Streamlit app:
```bash
streamlit run main.py
```
