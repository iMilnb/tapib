FROM python:3-onbuild

EXPOSE 5001

CMD [ "python", "./tapib.py" ]
