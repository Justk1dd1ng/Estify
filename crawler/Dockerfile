FROM python:3.8

RUN pip install --upgrade pip
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p ~/.aws/
COPY .aws ~/.aws/

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y xvfb

ENV PATH="$PATH:/crawlers"
ENV PATH="$PATH:/db"

# Although it's not far too safe, we may provide aws secrets here with the following syntax:
# ENV <MY_SECRET_KEY>=<MY_SECRET_VALUE>

#ENV AWS_ACCESS_KEY_ID=<value>
#ENV AWS_SECRET_ACCESS_KEY=<value>


CMD ["python", "app.py"]

