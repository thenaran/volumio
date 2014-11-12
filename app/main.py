# -*- coding: utf-8 -*-
# Copyright 2012-2014 Narantech Inc.
#
# This program is a property of Narantech Inc. Any form of infringement is
# strictly prohibited. You may not, but not limited to, copy, steal, modify
# and/or redistribute without appropriate permissions under any circumstance.
#
#  __    _ _______ ______   _______ __    _ _______ _______ _______ __   __
# |  |  | |   _   |    _ | |   _   |  |  | |       |       |       |  | |  |
# |   |_| |  |_|  |   | || |  |_|  |   |_| |_     _|    ___|       |  |_|  |
# |       |       |   |_||_|       |       | |   | |   |___|       |       |
# |  _    |       |    __  |       |  _    | |   | |    ___|      _|       |
# | | |   |   _   |   |  | |   _   | | |   | |   | |   |___|     |_|   _   |
# |_|  |__|__| |__|___|  |_|__| |__|_|  |__| |___| |_______|_______|__| |__|

# default
import os
import os.path
import atexit
import subprocess
import logging

# clique
import clique.web
import clique.event
import clique.runtime
from clique import runtime
from clique.isc import endpoint
from clique.isc import find

# ambiency 
import ambiency
from ambiency import build_actuator
from ambiency import build_action
from ambiency import build_source
from ambiency import actuators

__FLAG__ = os.path.join(clique.runtime.home_dir(), "_check")


def volumio_action(data):
  logging.debug("volumn io action data:%s", str(data))
  action = data.action_id
  if 'play' == action:
    subprocess.check_call('mpc play', shell=True)
  elif 'stop' == action:
    subprocess.check_call('mpc stop', shell=True)
  elif 'quite' == action:
    subprocess.check_call('mpc volume 70', shell=True)
  elif 'normal' == action:
    subprocess.check_call('mpc volume 80', shell=True)
  elif 'loud' == action:
    subprocess.check_call('mpc volume 90', shell=True)
  elif 'louder' == action:
    subprocess.check_call('mpc volume 100', shell=True)


@actuators
def get_actuators():
  sources = []
  sources.append(build_source('volumio', 'Volumio',
                              desc='Volumio music player.'))
  actions = [['play', 'Play', sources, [], 'Play music'],
             ['stop', 'Stop', sources, [], 'Stop music'],
             ['quite', 'Quite', sources, [], 'Set volume queit'],
             ['normal', 'Normal', sources, [], 'Set volume Normal'],
             ['loud', 'Loud', sources, [], 'Set volume Loud'],
             ['louder', 'Louder', sources, [], 'Set volume Louder']]
  volumio_actions = []
  for action in actions:
    volumio_actions.append(build_action(*action))
  actuators = []
  actuators.append(build_actuator('volumio',
                                  'Volumio',
                                  volumio_actions,
                                  volumio_action,
                                  'Control volumio player.'))
  return actuators


def start():
  if not os.path.exists(__FLAG__):
    cmd = "sh {script};touch {flag}".format(script=os.path.join(clique.runtime.res_dir(), "prepare.sh"),
                                            flag=__FLAG__)
    try:
      subprocess.check_call(cmd, shell=True)
      logging.info("Success execute prepare script.")
    except:
      logging.warn("Failed execute prepare script.", exc_info=True)
      if os.path.exists(__FLAG__):
        subprocess.check_call("rm {flag}".format(flag=__FLAG__), shell=True)

  clique.web.set_static_path(os.path.join(clique.runtime.res_dir(), "web"))
  subprocess.check_call('sudo /etc/init.d/alsa-utils start', shell=True)
  subprocess.check_call('sudo /etc/init.d/mpd start', shell=True)
  subprocess.check_call('sudo /etc/init.d/php5-fpm start', shell=True)
  subprocess.check_call('sudo /etc/init.d/nginx start', shell=True)
  subprocess.check_call('sudo /etc/init.d/nfs-common start', shell=True)
  try:
    subprocess.check_call('sudo /etc/init.d/dbus start', shell=True)
    subprocess.check_call('sudo /etc/init.d/avahi-daemon start', shell=True)
    subprocess.check_call('sudo /etc/init.d/shairport start', shell=True)
    subprocess.check_call('mpc update', shell=True)
  except:
    logging.warn("Failed to start the shairport. Airplay might not be available.", exc_info=True)

  logging.info("The daemon services (nginx, php5) started.")


@atexit.register
def stop():
  logging.info("stopping the daemon services (nginx, php5)...")
  subprocess.call('sudo /etc/init.d/shairport stop', shell=True)
  subprocess.call('sudo /etc/init.d/avahi-daemon stop', shell=True)
  subprocess.call('sudo /etc/init.d/dbus stop', shell=True)
  subprocess.call('sudo /etc/init.d/nfs-common stop', shell=True)
  subprocess.call('sudo /etc/init.d/php5-fpm stop', shell=True)
  subprocess.call('sudo /etc/init.d/nginx stop', shell=True)
  subprocess.call('sudo /etc/init.d/mpd stop', shell=True)
  subprocess.call('sudo /etc/init.d/alsa-utils stop', shell=True)


if __name__ == "__main__":
  start()
