FROM nikolaik/python-nodejs:python3.13-nodejs18 AS base

# Setup env
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

FROM base AS build

COPY . /app/

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc
# RUN pip install pipenv (aleady installed in base)

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.13 --deploy

FROM build AS submodule

# Initialize and update submodules
WORKDIR /app/fasset-bots
RUN git submodule update --init --recursive

# Build the submodule
RUN yarn install
RUN yarn clean
RUN yarn build

FROM base AS runner

# set workdir
WORKDIR /app

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Copy submodule
COPY --from=submodule /app/fasset-bots ./fasset-bots

# Copy python executables
COPY --from=build /app/qa_lib/ ./qa_lib/
COPY --from=build /app/run/ ./run/
COPY --from=build /app/run.py ./run.py

COPY entrypoint.sh ./entrypoint.sh
