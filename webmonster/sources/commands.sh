#!/bin/bash


#run web
/usr/local/bin/apache2-foreground &
status = $?
if [$status -ne 0]; then
    echo "Failed to start web server: $status"
    exit $status
fi

#run ssh-server
/usr/sbin/sshd -D
status = $?
if [$status -ne 0]; then
    echo "Failed to start web server: $status"
    exit $status
fi
