FROM pytorch/pytorch:latest
ENV INSTALL_PATH /opt/runtime
RUN mkdir -p $INSTALL_PATH
RUN mkdir /models
WORKDIR $INSTALL_PATH
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./
EXPOSE 5001 23456
VOLUME [ "/models" ]
ENTRYPOINT ["python", "./manager.py"]
