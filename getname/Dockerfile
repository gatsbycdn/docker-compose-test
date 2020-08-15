FROM python:3
ARG yourownbearer
ARG yourownzoneid
ARG vlesspath
ARG vmesspath
RUN curl http://v2caddy:2019/config/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python ./getname.py $yourownbearer $yourownzoneid $vmesspath $vlesspath