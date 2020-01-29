FROM pytorch/pytorch:1.0-cuda10.0-cudnn7-runtime
ENV INSTALL_PATH /opt/runtime
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
EXPOSE 5001 5002 23456
ENTRYPOINT ["python", "$INSTALL_PATH/admin.py"]
