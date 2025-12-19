FROM nikolaik/python-nodejs:python3.13-nodejs20 AS base

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

# Initialize, update, and build submodules
WORKDIR /app/fasset-bots
RUN git submodule update --init --recursive && yarn install --frozen-lockfile && yarn build && yarn cache clean;

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
COPY --from=build /app/cli ./cli

# copy entrypoint
COPY --from=build /app/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]