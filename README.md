# LLM_POC_RAG_OCR_BOT

## Overview

This application is a Proof of Concept (POC) focused on exploring new-age Generative AI (GenAI) applications. The app consists of a home page and three main features, each showcasing cutting-edge AI capabilities.

## Features

### 1. RAG Q&A System
The Retrieve-and-Generate (RAG) Q&A system is designed to deliver accurate and contextual answers by utilizing three different methods:
- **Simple RAG**: Retrieves and generates responses based on relevant data.
- **Corrective RAG**: Enhances accuracy by correcting retrieved information.
- **Self RAG**: Self-improving method to refine answers based on feedback.

### 2. Advanced OCR Module
This feature leverages an enhanced Optical Character Recognition (OCR) solution that combines PaddleOCR with a Large Language Model (LLM). It converts various document structures into structured JSON key-value pairs, surpassing the limitations of traditional OCR systems. This allows for more accurate data extraction and structuring from diverse document formats.

### 3. Agentic Chatbot
The Agentic Chatbot is an adaptive and intelligent chatbot designed to resolve complex user queries dynamically. Equipped with integrated tools, the chatbot leverages multiple AI-driven resources to provide precise and context-aware responses.

## Home Page

The home page of the application serves as a personal portfolio showcase. Built using Streamlit, it offers a simple and elegant way to present your profile and work.

## Getting Started

To run the application locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    streamlit run app.py
    ```
