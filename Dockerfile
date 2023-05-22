ARG WHEEL_DIST="tmp/wheels"

FROM python:3.10.3-slim-bullseye as base

ENV DEBIAN_FRONTEND=noninteractive

ARG WHEEL_DIST
ARG REQUIREMENTS_FILE

RUN echo deb http://deb.debian.org/debian bullseye contrib non-free > /etc/apt/sources.list.d/debian-contrib.list \
  && apt-get update \
  && apt-get --no-install-recommends install -y build-essential wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man

RUN pip install --no-cache-dir --upgrade pip

COPY ${REQUIREMENTS_FILE} /requirements.txt
RUN python3 -m pip wheel -w  "${WHEEL_DIST}" -r /requirements.txt

##########################################################
# We don't need all build-essential stuff to run the app 
##########################################################

FROM python:3.10.3-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND=noninteractive

ARG WHEEL_DIST

COPY --from=base "${WHEEL_DIST}" "${WHEEL_DIST}"

RUN echo deb http://deb.debian.org/debian bullseye contrib non-free > /etc/apt/sources.list.d/debian-contrib.list \
    && apt-get update \
    && apt-get --no-install-recommends install -y tzdata libpq-dev libmagic-dev libffi-dev \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man

WORKDIR "${WHEEL_DIST}"

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir *.whl

WORKDIR /src

COPY . /src

USER nobody

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]