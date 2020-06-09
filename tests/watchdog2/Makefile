FOLDER=$(realpath .)
USER=$(shell whoami)
# USER=ramkhamhaeng
PYTHON_BIN=$(shell which python3 || which python)

SYSTEMD_INSTALL_DIR=/etc/systemd/system
SYSTEMCTL_BIN=$(shell which systemctl)

# To use subcommand output as file [ cat <(echo "Test") ]
SHELL=/bin/bash

SITE_PACKAGES=site-packages
PIP_PACKAGES='scapy' \

# WATCHDOG_ARGS=[NET INTERFACE] [PITBOSS SERVER IP] [LIST OF GAMES]
# Example:
# WATCHDOG_ARGS=wls3 192.168.0.99 /home/$(USER)/PBs/PB1
# 
# Not required anymore! Set args in file 'pitboss_watchdog.args'!
WATCHDOG_ARGS=

help:
	@echo -e "Common targets:\n" \
		"make run                 -- Start daemon. Quit with Ctl+C.\n" \
		"make start|stop|reload   -- Control systemd service\n" \
		"make install_service     -- Install systemd service for automatic start\n" \
		"                            Service will started as user '${USER}'\n" \
		"make uninstall_service   -- Uninstall systemd service\n" \
		"make log                 -- Show journalctl log\n" \
		"\n" \
		"make install_deps_local  -- Install dependencies locally for this user\n" \
		"make install_deps_global -- Install dependencies global on system\n" \
		"\n" \
		"" \

run: 
	sudo PYTHONPATH='$(SITE_PACKAGES)' $(PYTHON_BIN) pitboss_watchdog.py $(WATCHDOG_ARGS)

%.service: %.service.template
	@echo "Create systemd service file for startup."
	sed -e "s#{USER}#$(USER)#g" \
		-e "s#{FOLDER}#$(FOLDER)#g" \
		-e "s#{PYTHON_BIN}#$(PYTHON_BIN)#g" \
		-e "s#{SITE_PACKAGES}#$(SITE_PACKAGES)#g" \
		-e "s#{WATCHDOG_ARGS}#$(WATCHDOG_ARGS)#g" \
		$< > $(basename $<)

%.sudoers: %.sudoers.template
	@echo "Create sudoers file for unit control (start stop restart)"
	sed -e "s#{GROUP}#$(USER)#g" \
		-e "s#{SYSTEMCTL_BIN}#$(SYSTEMCTL_BIN)#g" \
		$< > $(basename $<)

create_service_files: pitboss_watchdog.service

pitboss_watchdog.argsx:
	@echo -e "   Before you install the systemd unit, create '$@'\n"\
		"  and insert proper startup arguments for the script.\n"\
		"\n" \
	  "          Values: [NET INTERFACE] [PITBOSS SERVER IP] [LIST OF GAMES]\n"\
		"  Example values: eth0 192.168.0.99 /home/$(USER)/PBs/PB1\n"\
		"\n"\
		"  You can edit this arguments later without re-installing the\n"\
	  "  systemd unit file.\n"

install_service: pitboss_watchdog.service pitboss_watchdog.sudoers pitboss_watchdog.args
	sudo cp "$(FOLDER)/$<" "$(SYSTEMD_INSTALL_DIR)/$<"
	sudo systemctl daemon-reload
	sudo systemctl enable "$<"
	sudo install -m 0440 "pitboss_watchdog.sudoers" "/etc/sudoers.d/pitboss_watchdog.conf"
	@echo -e "Service enabled, but not started.\n" \
		"Call 'sudo systemctl start $<' to start service."

uninstall_service: pitboss_watchdog.service
	sudo systemctl stop "$<"
	sudo systemctl disable "$<"
	sudo rm	"/etc/sudoers.d/pitboss_watchdog.conf"
	sudo rm "$(SYSTEMD_INSTALL_DIR)/$<"

start: pitboss_watchdog.service
	sudo systemctl start "$<"

stop: pitboss_watchdog.service
	sudo systemctl stop "$<"

restart: pitboss_watchdog.service
	sudo systemctl restart "$<"

log: pitboss_watchdog.service
	journalctl -u "$<"

# ====================================================

install_deps_local:
	$(PYTHON_BIN) -m pip install -t $(SITE_PACKAGES) $(PIP_PACKAGES)

install_deps_global:
	sudo $(PYTHON_BIN) -m pip install $(PIP_PACKAGES)
