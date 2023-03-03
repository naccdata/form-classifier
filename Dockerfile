FROM flywheel/python:main.a30a2597

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry install --no-dev --no-root

# Installing the current project (most likely to change, above layer can be cached)
# Note: poetry requires a README.md to install the current project
COPY . .
RUN poetry install --no-dev

# Configure entrypoint
ENTRYPOINT ["python","/flywheel/v0/run.py"]
