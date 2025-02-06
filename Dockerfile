FROM python:3.10

WORKDIR /app

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    chromium \
    chromium-driver \
    ffmpeg \
    imagemagick \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Configure ImageMagick policy to allow text operations
RUN if [ -f /etc/ImageMagick-6/policy.xml ]; then \
    # Allow reading/writing PDFs
    sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml && \
    # Allow reading text files for text-to-image operations
    sed -i 's/rights="none" pattern="@\*"/rights="read|write" pattern="@\*"/' /etc/ImageMagick-6/policy.xml && \
    # Increase memory limits
    sed -i 's/domain="resource" name="memory" value="[0-9]*"/domain="resource" name="memory" value="8GiB"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/domain="resource" name="disk" value="[0-9]*"/domain="resource" name="disk" value="8GiB"/' /etc/ImageMagick-6/policy.xml; \
    fi

# Create fonts directory and copy custom fonts
RUN mkdir -p /usr/local/share/fonts/custom
COPY fonts /usr/local/share/fonts/custom

# Update font cache
RUN fc-cache -f -v

# Install the correct Chromedriver version dynamically
RUN CHROMIUM_VERSION=$(chromium --version | awk '{print $2}') && \
    wget -q -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMIUM_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver* && \
    chmod +x /usr/local/bin/chromedriver

# Verify installation
RUN echo "Checking Chromium and Chromedriver versions..." && \
    chromium --version && \
    chromedriver --version && \
    which chromedriver

# Copy and install requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src /app/
COPY video_templates /app/video_templates
COPY client_secrets.json /app/
COPY service-account.json /app/

CMD ["python3", "main.py"]