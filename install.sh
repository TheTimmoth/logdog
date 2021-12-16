#!/bin/bash

echo "log2mail installation script"
echo "Author: Tim Schlottmann"
echo "(C) 2021"


check_prerequisits() {
  if [ $UID -ne 0 ]
  then
    echo "This script has to be run as root!"
    exit 1
  fi

  which python3 > /dev/null 2>&1
  if [[ $? -ne 0 ]]
  then
    echo "Please install python3 first, before installing this program! (Or make it available via \$PATH)"
    exit 2
  fi

  # TODO: Check for pip installation using "python3 -m pip --version"
}

install_python() {
  echo "Install python module..."

  python3 -m pip install -e ./

  echo "Done..."
}

install_bin() {
  echo "Add logdog and log2mail to /usr/bin..."

  # Remove old executable if applicable
  rm /bin/logdog > /dev/null 2>&1
  rm /bin/log2mail > /dev/null 2>&1

  # Copy executable
  cp ./bin/logdog /usr/bin
  cp ./bin/log2mail /usr/bin

  chmod 775 /bin/logdog
  chmod 775 /bin/log2mail

  echo "Done..."
}

install_service() {
  echo "Installing logdog service..."

  # Insert PWD into logdog.service
  cp -pn  $PWD/service/logdog.service.template $PWD/service/logdog.service
  sed -i s*%%LOGDOG_PATH%%*$PWD*g $PWD/service/logdog.service

  ln -s $PWD/service/logdog.service /lib/systemd/system

  echo "Enable and start service..."
  systemctl daemon-reload
  systemctl enable logdog

  echo "Done..."
}

# Change path to script directory
cd $(dirname $0)

check_prerequisits
install_python
install_bin
install_service

exit 0
