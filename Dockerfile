FROM alpine/git:v2.36.1 as profiles

ENV PROFILE_VERSION=0.2.2

RUN git clone --depth 1 \
    --branch $PROFILE_VERSION \
    https://gitlab.com/flywheel-io/public/fw-classification/fw-classification-profiles.git \
    /root/profiles

FROM flywheel/python:main.a30a2597 AS deps

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry install --no-dev --no-root

# Installing the current project (most likely to change, above layer can be cached)
# Note: poetry requires a README.md to install the current project
COPY . .
COPY --from=profiles /root/profiles/profiles ./fw_gear_file_classifier/classification_profiles
RUN poetry install --no-dev

# Configure entrypoint
ENTRYPOINT ["python","/flywheel/v0/run.py"]
