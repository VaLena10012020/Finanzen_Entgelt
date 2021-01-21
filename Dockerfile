FROM python
ADD /home/valentin/Projekte/Finanzen/. app/
RUN pip install -r requirements.txt
RUN make /app
WORKDIR /app/Entgelt/mail_receiver
CMD [ "python", "mail_receiver.py" ]