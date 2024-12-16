# Project Overview

In this project, I aimed to create a Python script (`autolysis.py`) that accepts a CSV dataset, performs generic data analysis, visualizes the results, and generates a story about the findings. The script was designed to interact with a language model (LLM) to generate the narrative based on the data analysis. 

However, during development, I encountered an issue when attempting to use the **GPT-4o-Mini proxy API** to generate the story.

## Issue with GPT-4o-Mini API
I attempted to use the GPT-4o-Mini model via the provided API proxy to create the story about the dataset and its analysis. Unfortunately, the output was not as expected, and the story generation was either incomplete or lacked coherence.

The issues I faced included:
- **Inconsistent Responses**: The API often returned incomplete or nonsensical responses that didn't align with the data analysis.
- **Failed API Calls**: Some API calls failed to generate the desired results, causing interruptions in the workflow.
- **Output Quality**: The quality of the narrative produced by the GPT-4o-Mini model did not meet the expectations for a well-structured and insightful story.

Due to these challenges, I decided to switch to an alternative API for generating the story.

## Switching to Gemini API
As an alternative, I used the **Gemini API** for story generation. This API provided more consistent and coherent output, making it a better choice for this task. I implemented Gemini through a Python script (`henith.py`) and integrated it into the project to generate the story based on the analysis results.

The new setup with Gemini allowed me to:
- Generate more accurate and contextually relevant narratives.
- Ensure that the story was well-structured, including analysis insights and their implications.

## Conclusion
While the GPT-4o-Mini proxy API was initially the intended model for generating the story, the issues I encountered with its responses led me to switch to the Gemini API. This decision helped ensure that the project met the required standards for generating a coherent and insightful narrative from the dataset analysis.
