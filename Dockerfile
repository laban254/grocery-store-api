FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /var/run/sshd \
    && echo 'PermitRootLogin no' >> /etc/ssh/sshd_config \
    && echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user and set up SSH
RUN useradd -m -s /bin/bash appuser \
    && mkdir -p /home/appuser/.ssh \
    && chown -R appuser:appuser /app /home/appuser/.ssh \
    && chmod 700 /home/appuser/.ssh

# Set up SSH key
ARG SSH_PUBLIC_KEY
RUN echo "$SSH_PUBLIC_KEY" > /home/appuser/.ssh/authorized_keys \
    && chmod 600 /home/appuser/.ssh/authorized_keys \
    && chown appuser:appuser /home/appuser/.ssh/authorized_keys

# Copy the startup script
COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh

USER root
# Run both SSH and Django application
CMD ["/start.sh"]
