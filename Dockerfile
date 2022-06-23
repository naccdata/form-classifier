FROM flywheel/python:main.a30a2597 AS deps

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry install --no-dev --no-root

# Installing the current project (most likely to change, above layer can be cached)
# Note: poetry requires a README.md to install the current project
COPY run.py manifest.json .gitmodules README.md $FLYWHEEL/
COPY fw_gear_file_classifier $FLYWHEEL/fw_gear_file_classifier
COPY .git $FLYWHEEL/.git
RUN git submodule init && \
    git submodule update --recursive && \
    poetry install --no-dev

# Configure entrypoint
RUN chmod a+x "$FLYWHEEL"/run.py
ENTRYPOINT ["poetry","run","python","/flywheel/v0/run.py"]
