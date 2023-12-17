function install_erlang {
  if [ ! -d otp_src_26.1.2 ]; then
    echo "Downloading Erlang sources"
    wget -q https://github.com/erlang/otp/releases/download/OTP-26.1.2/otp_src_26.1.2.tar.gz
    tar -xzf otp_src_26.1.2.tar.gz
    rm otp_src_26.1.2.tar.gz
  else
    echo "Erlang sources already downloaded"
  fi
  cd otp_src_26.1.2
  export ERL_TOP=`pwd`
  ./configure --prefix=$HOME/.local
  make install
  cd ..
}

function install_rabbit_g5k {
  echo "Switching to local install folder (~/Install-tmp)"
  OLD_PWD=$(pwd)
  mkdir -p ~/Install-tmp
  cd ~/Install-tmp

  echo "Installing Erlang"
  if [ ! command -v erl &> /dev/null ]; then
    echo "Erlang not found"
    install_erlang
  else
    echo "Erlang already installed"
  fi

  echo "Installing RabbitMQ"
  wget -q https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.12.10/rabbitmq-server-generic-unix-3.12.10.tar.xz
  tar -xf rabbitmq-server-generic-unix-3.12.10.tar.xz

  mkdir -p ~/.local/share
  rm -rf ~/.local/share/rabbitmq
  mv rabbitmq_server-3.12.10 ~/.local/share/rabbitmq

  rm rabbitmq-server-generic-unix-3.12.10.tar.xz

  cd $OLD_PWD
}
