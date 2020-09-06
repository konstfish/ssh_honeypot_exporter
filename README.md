# ssh_honeypot_exporter

![alt text](img/demo.png)


requires the log file from [droberson/ssh-honeypot](https://github.com/droberson/ssh-honeypot)

## docker

```bash
docker build -t konstfish/ssh_honeypot_exporter .
docker run -p 9567:9567 -v /path/to/log/honeypot.json:/opt/honeypot.json konstfish/ssh_honeypot_exporter
```

## docker-compose

```yaml
prometheus_ssh_honeypot:
    build: ./ssh_honeypot_exporter
    ports:
        - 9567:9567
    volumes:
        - /path/to/log/honeypot.json:/opt/honeypot.json
```

## prometheus config

```yaml
- job_name: 'ssh_honeypot'
  scrape_interval: 10m
  scrape_timeout: 5m
  static_configs:
    - targets: ['prometheus_ssh_honeypot:9567']
```
