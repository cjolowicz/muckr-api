FROM python:3.7-alpine as base

FROM base as builder

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
WORKDIR /wheels
COPY ./requirements/base.txt ./requirements.txt
RUN pip install --upgrade pip && pip wheel -r requirements.txt

FROM base

RUN apk add --no-cache libffi libpq
COPY --from=builder /wheels /wheels
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r /wheels/requirements.txt -f /wheels \
  && rm -rf /wheels \
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/local/src/app
COPY . .

CMD ["./docker-entrypoint.sh"]
