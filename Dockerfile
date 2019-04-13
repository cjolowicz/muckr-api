FROM python:3.7-alpine as base

FROM base as builder

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
COPY requirements/base.txt /requirements.txt
WORKDIR /build
RUN pip install --upgrade pip \
    && pip install --install-option="--prefix=." --no-cache-dir -r /requirements.txt

FROM base
COPY --from=builder /build /usr/local

ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache libffi libpq
WORKDIR /usr/local/src/muckr-service
COPY . .

CMD ["./docker-entrypoint.sh"]
