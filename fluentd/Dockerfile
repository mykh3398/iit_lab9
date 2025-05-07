FROM fluent/fluentd:v1.14-1

USER root

RUN apk add --no-cache --virtual .build-deps \
    sudo build-base ruby-dev \
 && gem install faraday -v 2.8.1 \
 && gem install faraday-net_http -v 1.0.1 \
 && gem install elasticsearch -v 7.17.0 \
 && gem install fluent-plugin-elasticsearch -v 4.0.0 \
 && gem sources --clear-all \
 && apk del .build-deps \
 && rm -rf /var/cache/apk/* /home/fluent/.gem/ruby/*/cache/*.gem

USER fluent
