FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install alpha_vantage
RUN pip install pandas
RUN pip install requests
RUN pip install matplotlib
RUN pip install times
RUN pip install plotly

COPY . .
