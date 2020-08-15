FROM python:3
ARG yourownbearer
ARG yourownzoneid
ARG vlesspath
ARG vmesspath
#RUN curl http://v2caddy:2019/config/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#CMD ["curl","http://v2caddy:2019/config/"]
#RUN python ./getname.py $yourownbearer $yourownzoneid $vmesspath $vlesspath
RUN echo yourownbearer
RUN echo yourownzoneid
RUN echo vlesspath
RUN echo vmesspath
CMD ["sh","-c","python getname.py $yourownbearer $yourownzoneid $vlesspath $vmesspath"]