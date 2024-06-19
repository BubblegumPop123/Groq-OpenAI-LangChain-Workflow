### Project Guide and Description

#### Overview
This project is designed to leverage advanced AI technologies, specifically Groq AI and OpenAI's language models (LLMs), in conjunction with LangChain, to automate and streamline web scraping and task completion processes. The primary objective is to scrape HTML interactable div elements from a website, interpret user input to generate actionable steps, and provide action recommendations to complete specified tasks.

#### Components

1. **Decomposition API**:
   - **Description**: This component handles the initial processing and decomposition of tasks. It sets up the environment and dependencies required for the project.
   - **Files**:
     - `.env`: Configuration file for environment variables.
     - `main.py`: The main script that runs the decomposition process.
     - `requirements.txt`: Lists the dependencies and libraries needed.

2. **Filtering**:
   - **Description**: This module is responsible for web scraping and filtering the relevant HTML elements from the target website.
   - **Files**:
     - `app.py`: Main application script for filtering and scraping.
     - `crawler_script.py`: Script dedicated to crawling and extracting interactable div elements from the web pages.

3. **Recommendation**:
   - **Description**: This part of the project interprets user input and generates a list of action steps to accomplish the desired tasks. It uses the outputs from the decomposition and filtering stages.
   - **Files**:
     - `main.py`: The main script that processes user input and generates action recommendations.

#### Process Workflow

1. **Scraping HTML Interactable Divs**:
   - The project begins by scraping HTML interactable div elements from the specified website. This is handled by the `filtering` component, which uses a web crawler to navigate through web pages and identify div elements that are interactable (e.g., buttons, forms, links).

2. **Task Decomposition**:
   - Once the relevant div elements are scraped, the `decomposition_api` component processes these elements and decomposes the overall task into manageable sub-tasks. This step prepares the system to handle user input effectively by understanding the structure and functionality of the web elements.

3. **Generating Action Steps**:
   - Using the decomposed tasks, the project employs OpenAI's language models (LLMs) to interpret user input. The models analyze the input to understand the user's intent and generate actionable steps. LangChain plays a crucial role in linking these steps with the appropriate web elements and functions.

4. **Action Recommendation Lists**:
   - Finally, the `recommendation` component uses Groq AI to create detailed action recommendation lists. These lists provide a step-by-step guide on how to complete the specified tasks based on the user's input and the previously scraped and decomposed web elements.

#### Technologies Used

- **Groq AI**: Utilized for creating efficient and optimized action recommendation lists.
- **OpenAI LLMs**: Employed to understand user input and generate action steps using natural language processing.
- **LangChain**: Acts as a framework to integrate various AI models and streamline the process of linking action steps with web elements.
- **Web Scraping**: Techniques used to extract interactable HTML div elements from websites for further processing.

By scraping HTML elements, decomposing tasks, interpreting user input, and generating action recommendations, the project offers a comprehensive solution for task automation and completion.
