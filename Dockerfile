FROM alpine/git:v2.36.1 as profiles

ENV PROFILE_VERSION=0.3.2

RUN git clone --depth 1 \
    --branch $PROFILE_VERSION \
    https://gitlab.com/flywheel-io/public/fw-classification/fw-classification-profiles.git \
    /root/profiles/

FROM flywheel/python:main.a30a2597 AS deps

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Dev install. git for pip editable install.
RUN apt-get update &&  \
    apt-get install --no-install-recommends -y git=1:2.30.2-1+deb11u2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Installing main dependencies
COPY requirements.txt $FLYWHEEL/
RUN pip install --no-cache-dir -r $FLYWHEEL/requirements.txt

# Installing the current project (most likely to change, above layer can be cached)
COPY ./ $FLYWHEEL/
RUN pip install --no-cache-dir .

# Copying profiles
COPY --from=profiles /root/profiles/profiles ./fw_gear_file_classifier/classification_profiles

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["python","/flywheel/v0/run.py"]
