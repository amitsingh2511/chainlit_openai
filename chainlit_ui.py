import openai
import pandas as pd
import io
import os
import chainlit as cl 
# from openai.error import RateLimitError, APIError

from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = openai_api_key

# Function to create an agent
def create_agent(df, llm):
    
    return lambda query: process_with_openai(query, df)

# Function to process with OpenAI API
def process_with_openai(query, df,  retries=3, delay=5):
    # Create a prompt from the user's query and the dataframe information
    attempt = 0
    # while attempt < retries:
    try:
        # Create a prompt from the user's query and the dataframe information
        prompt = f"Here is the data you can reference: {df.head(5).to_string(index=False)}\n\nAnswer the following question based on this data:\n{query}"
        
        print("=========",prompt)

        # Call OpenAI's API to process the prompt
        response = openai.Completion.create(
            model="gpt-3.5-turbo", 
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )

        # Extract the answer from the OpenAI response
        return response['choices'][0]['text'].strip()
    
        # except RateLimitError as e:
        #     attempt += 1
        #     print(f"RateLimitError: Attempt {attempt}/{retries} failed. Retrying in {delay} seconds...")
            
        # except APIError as e:
        #     # Handle other API errors like server errors
        #     print(f"APIError: {str(e)}")
        #     raise Exception("OpenAI API is temporarily unavailable. Please try again later.")
    except Exception as e:
        # Handle any other errors (e.g., network issues, invalid input)
        print(f"Unexpected error: {str(e)}")
            # raise Exception(f"An unexpected error occurred: {str(e)}")

    # If retries are exhausted and it still fails, raise an error
    return ("You exceeded your current quota, please check your plan and billing details. Please try again later.")


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hello Manager!").send()

    files = None
    # Waits for user to upload CSV data
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a csv file to begin!", accept=["text/csv"], max_size_mb=100
        ).send()

    # If file is received, access it properly
    file = files[0]
    
    # Read the file from the path
    try:
        with open(file.path, 'rb') as f:
            csv_file = io.BytesIO(f.read())  # Read file content into memory as bytes
    except Exception as e:
        raise ValueError(f"Failed to read the file: {str(e)}")
    
    
    # Load the CSV data and store it in user session
    df = pd.read_csv(csv_file, encoding="utf-8")

    # Create user session to store data
    cl.user_session.set('data', df)

    # Send response back to user
    await cl.Message(
        content=f"`{file.name}` uploaded! Now you can ask me anything related to your csv."
    ).send()



@cl.on_message
async def respond_to_user_message(message: str):
    # Get data from user session
    df = cl.user_session.get('data')
    print(df)

    # Create an agent using the dataframe and the OpenAI API
    agent = create_agent(df, openai)

    # Run the model and get the response
    response = agent(message)

    # Send the response back to the user
    await cl.Message(
        content=response,
    ).send()
