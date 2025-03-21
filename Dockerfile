# Use Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


ENV PORT=8003
# Expose port for Chainlit
EXPOSE 8003

# Set environment variables
# ENV OPENAI_API_KEY=your-openai-api-key

# Run the Chainlit app
CMD ["chainlit", "run", "chainlit_ui.py", "-w", "--host", "0.0.0.0", "--port", "8003"]
