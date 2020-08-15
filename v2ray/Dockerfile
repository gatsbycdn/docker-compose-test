FROM v2fly/v2fly-core
LABEL maintainer="nobody"
ARG vlessuuid
ARG vmessuuid
ARG vlesspath
ARG vmesspath

RUN echo "vlessuuid: ${vlessuuid}, vlesspath: ${vlesspath}"
RUN echo "vmessuuid: ${vmessuuid}, vmesspath: ${vmesspath}"

WORKDIR /etc/v2ray/
COPY ./config.json /etc/v2ray/

RUN sed -i -e "s/vlessuuid/${vlessuuid}}/g" /etc/v2ray/config.json
RUN sed -i -e "s/vlesspath/${vlesspath}}/g" /etc/v2ray/config.json

RUN sed -i -e "s/vmessuuid/${vmessuuid}}/g" /etc/v2ray/config.json
RUN sed -i -e "s/vmesspath/${vmesspath}}/g" /etc/v2ray/config.json
RUN cat /etc/v2ray/config.json
CMD ["/usr/bin/v2ray/v2ray","--config=/etc/v2ray/config.json"]