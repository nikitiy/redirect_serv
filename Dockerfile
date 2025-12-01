FROM python:3.13-slim

# Install Poetry
RUN pip install poetry==1.8.3

# Configure poetry to not create virtual env
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set work directory
WORKDIR /app

# Copy application code
COPY . .

# Install the package itself
RUN poetry install --only main && rm -rf $POETRY_CACHE_DIR

# Expose port
EXPOSE 8000

# Add venv to PATH for direct access
ENV PATH="/app/.venv/bin:$PATH"

# Run the application with root_path for reverse proxy
CMD ["uvicorn", "src.redirect_serv.main:app", "--host", "0.0.0.0", "--port", "8000"]
