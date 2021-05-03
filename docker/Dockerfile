# Pulls python base image, configure dependancies
FROM python:3 as BASE

# Store pointer to venv path and init venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH=$VIRTUAL_ENV/bin:$PATH

ENV PYTHONUNBUFFERED 1

# Make path for requirements
RUN mkdir /opt/requirements

# Copy requirments in container
ADD requirements /opt/requirements

# build libraries for developent
RUN pip install -r /opt/requirements/development.txt


# Stage 2 handles application code
FROM BASE as RUN

# Point workdir to volume listed in docker-compose file
WORKDIR /opt/code

# Commented out for speedier reloading during development
# RUN addgroup --system quantum && adduser --system --no-create-home --group tpb
# RUN chown -R tpb:quantum /opt/code && chmod -R 755 /opt/code
# RUN chown -R tpb:quantum /opt/code/application/admin/backups

# USER tpb:quantum

# Pull cached runtime from base container
COPY --from=BASE /opt/venv /opt/venv 

# Load environment
ENV PATH="/opt/venv/bin:$PATH"

