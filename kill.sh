#!/usr/bin/env bash
ps aux | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} python | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} -v "grep python" | awk '{print $2}' | xargs kill -9
