FROM python:3.12.3-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from writing .pyc files (compiled bytecode)
# Why? -> Docker layers work better without these changing files

ENV PYTHONUNBUFFERED=1
# Makes Python output appear immediaterly in logs
# Without this, print() statements might be delayed


# Set working directory
WORKDIR /app
# All future commands run from /app folder


# Copy requirements file
COPY requirements.txt /app/
# Copies from your computer -> into container
# Why separate? -> Docker caching! -- If requirements don't change,
# this layer is reused (faster builds)


# Install Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt
# RUN executes commands during image building
# Analogy: Installing apps before giving someone the computer


# Copy entire project
COPY . /app/
# Copies everything from current folder -> /app in container
# The '.' means "current directory on your computer"


# Create directories
RUN mkdir -p /app/staticfiles /app/media
# -p flag: create parent directories if needed, no error if exists


# Expose port
EXPOSE 8000
# Documentation: "This container listens on port 8000"
# Does not actually opens the port (docker-compose does that)


# Default command
CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
# Runs when container starts
# && means "run second command only if first success"
# 0.0.0.0 = Listen on all network interfaces (allows external access)
