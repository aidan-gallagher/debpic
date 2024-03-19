ARG DISTRIBUTION=debian:12
FROM $DISTRIBUTION
LABEL MAINTAINER="Aidan Gallagher <aidgal2@gmail.com>"
USER root

# ---------------------------------------------------------------------------- #
# Prevent apt from asking the user questions like which time zone.
ARG DEBIAN_FRONTEND=noninteractive
# Set the locale
ENV LANG=C.UTF-8
# ---------------------------------------------------------------------------- #


# --------------------- Add docker user & set working dir -------------------- #
# Create docker user and enable sudo permissions.
ARG UID=1000
RUN useradd --shell /bin/bash --uid $UID --create-home docker && \
    echo "docker:docker" | chpasswd && \
    apt-get update --yes && \
    apt-get install --yes sudo && \
    echo "docker ALL = (root) NOPASSWD: ALL\n" > /etc/sudoers.d/docker
WORKDIR /workspaces/code
# ---------------------------------------------------------------------------- #


# ----------------- Parent directory permissions work around ----------------- #
# dpkg-buildpackage deposits debs (and temp files) in the parent directory.
# Currently there is no way to specify a different directory (https://groups.google.com/g/linux.debian.bugs.dist/c/1KiGKfuFH3Y).
# Non root users do not always have permission to write to the parent directory (depending on where the workspace is mounted).
# Change parent directories of known mount location to have write permissions for all users.

# Jenkins mounts the directory at /var/lib/jenkins/workspace/DANOS_{REPO}_PR-XXX.
# VSCode mounts the directory at /workspaces/{REPO}
RUN mkdir -p /var/lib/jenkins/workspace && \
    chown -R docker:docker /var/lib/jenkins/workspace && \
    mkdir -p /workspaces && \
    chown -R docker:docker /workspaces

RUN mkdir --parents /home/docker/.cache/ccache && \
    chown -R docker:docker /home/docker/.cache
# ---------------------------------------------------------------------------- #


# --------------------------- Add convenience script-------------------------- #
# If the user is in interactive mode and runs `dpkg-buildpackage` the generated
# .debs are placed in the parent directory which isn't mounted and therefore not
# avilable to the host.
RUN echo "#!/bin/bash \n\
rm -rf /workspaces/code/built_packages \n\
mkdir --parents /workspaces/code/built_packages/ \n\
mv /workspaces/*.* /workspaces/code/built_packages \
" > /usr/bin/mv-debs && chmod +x /usr/bin/mv-debs
# ---------------------------------------------------------------------------- #


# ----------------------------- Set apt settings ----------------------------- #
RUN echo '\
Acquire::Retries "10";\n\
Acquire::http::Timeout "240"; \n\
Acquire::ftp::Timeout "240";\n\
APT::Get::Assume-Yes "true";\n\
APT::Install-Recommends "false";\n\
APT::Install-Suggests "false";\n\
APT::Get::Fix-Missing;' > /etc/apt/apt.conf.d/99debpic
# ---------------------------------------------------------------------------- #


# -------------- Install mk-build-deps, apt-ftparchive & ccache -------------- #
RUN apt-get update && \
    apt-get install devscripts equivs apt-utils ccache
# ---------------------------------------------------------------------------- #


# -------------------------- Setup local repository -------------------------- #
COPY ./local_repositor[y] ./debian/changelog /tmp/local_repository/
# [y] allows conditional copying (https://stackoverflow.com/a/31532674/13365272)
# ./debian/changelog isn't needed, but without BUILDKIT conditional copying requires
# at least one file is copied so chose a file that is guaranted to be there and won't
# change often. I can't work out how to get VSCode to use BUILDKIT on debian.
RUN if [ -d /tmp/local_repository ]; then \
        cd /tmp/local_repository && \
        apt-ftparchive packages . > Packages && \
        echo "\
Types: deb \n\
URIs: file:/tmp/local_repository \n\
Suites: ./ \n\
Trusted: yes \n" >> /etc/apt/sources.list.d/01debpic.sources && \
    echo "\
Package: * \n\
Pin: origin \"\" \n\
Pin-Priority: 1001 \n" >> /etc/apt/preferences.d/01debpic; \
    fi
# ---------------------------------------------------------------------------- #


# ------------------------- Add additional apt repos ------------------------- #
ARG ADDITIONAL_SOURCES=""
RUN echo "$ADDITIONAL_SOURCES" >> /etc/apt/sources.list.d/01debpic.sources

ARG ADDITIONAL_PREFERENCES=""
RUN echo "$ADDITIONAL_PREFERENCES" >> /etc/apt/preferences.d/01debpic.pref
# ---------------------------------------------------------------------------- #


# -------------------------- Install Extra Packages -------------------------- #
ARG EXTRA_PKGS=""
RUN apt-get update && \
    apt-get install $EXTRA_PKGS
# ---------------------------------------------------------------------------- #


# ------------------ Install optional developer dependencies ----------------- #
# "2>/dev/null" will prevent cat from printing an error if the file doesn't exit.
COPY ./developer-packages.tx[t] ./debian/changelog /tmp/
RUN apt-get update && \
    apt-get install $(cat /tmp/developer-packages.txt 2>/dev/null)
# ---------------------------------------------------------------------------- #


# ---------------- Install Debian build/packaging dependencies --------------- #
# Install application's build/packaging dependencies.
COPY ./debian/control ./debian/changelog /tmp/
RUN apt-get update && \
    mk-build-deps /tmp/control && \
    apt-get install ./*build-deps*.deb
# ---------------------------------------------------------------------------- #