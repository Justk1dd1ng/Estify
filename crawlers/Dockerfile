FROM python:3.8

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p ~/.aws/
COPY ./.aws/credentials ~/.aws

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y xvfb


CMD ["python", "app.py"]
