#!/bin/bash

eval $(grep -v '^#' /container-config/.cronenv | xargs -d "\n" -I {} echo export \"{}\" )
env
whoami
if [ -z "$SUDO_OIM_ENCRYPTED_PASSWORD" ]; then
    echo "SUDO_OIM_ENCRYPTED_PASSWORD Ignored":
else
    # create a new password.
    echo "SUDO_OIM_ENCRYPTED_PASSWORD Preparing";
    SUDO_OIM_ENCRYPTED_PASSWORD_SIZE="$(echo $SUDO_OIM_ENCRYPTED_PASSWORD | wc -m)"
    if [ "$SUDO_OIM_ENCRYPTED_PASSWORD_SIZE" -gt "10" ]; then
    usermod -p "$SUDO_OIM_ENCRYPTED_PASSWORD" oim
    echo "SUDO_OIM_ENCRYPTED_PASSWORD Updated";
    fi
fi


if [ $ENABLE_CRON == "True" ];
then
    echo "Starting Cron"
    service cron start &
    status=$?
    if [ $status -ne 0 ]; then
    echo "Failed to start cron: $status"
    exit $status
    fi
fi
else
   echo "ENABLE_WEB environment vairable not set to True, web server is not starting."
   /bin/bash
fi
