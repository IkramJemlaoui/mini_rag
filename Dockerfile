# Use Ollama base image
FROM ollama/ollama:latest

# Work directory
WORKDIR /app

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean

# Copy your project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pull models once during build
RUN ollama pull mistral && ollama pull nomic-embed-text

# Expose app & Ollama ports
EXPOSE 7860 11434

# Start Ollama + your app
CMD bash -c "ollama serve & sleep 5 && python3 app.py"
