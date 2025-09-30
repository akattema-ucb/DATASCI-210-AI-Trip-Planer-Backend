FROM amazon/aws-lambda-python:3.12

# Install system dependencies
RUN dnf install -y gcc-c++

# Copy requirements first for better caching
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ${LAMBDA_TASK_ROOT}

# Command to run the application
CMD [ "main.handler" ]
