FROM debian:bookworm

ARG USERNAME=ansible
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && \
    apt install -y --no-install-recommends git \
      curl \
      sudo \
      tzdata \
      build-essential \
      ca-certificates \
      python3-full \
      zsh

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -G sudo -s /bin/zsh \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER $USERNAME

WORKDIR /home/$USERNAME

RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
    git clone https://github.com/borland502/dotfiles && \
    cd dotfiles && \
    ./install.sh

CMD ["zsh", "-c", "sleep infinity"]

