FOLDER=$(realpath .)
USER=$(shell whoami)
# USER=ramkhamhaeng
PYTHON_BIN=$(shell which python3 || which python)
SYSTEMD_INSTALL_DIR=/etc/systemd/system

WATCHDOG_ARGS=wls3 192.168.0.99 /home/olaf/Civ4/PBs/PB1

# To use subcommand output as file [ cat <(echo "Test") ]
SHELL=/bin/bash

SITE_PACKAGES=site-packages
PIP_PACKAGES='scapy' \

help:
	@echo -e "Common targets:\n" \
		"make run                 -- Start daemon. Quit with Ctl+C.\n" \
		"make install_service     -- Install systemd service for automatic start\n" \
		"                            Service will started as user '${USER}'\n" \
		"make uninstall_service   -- Uninstall systemd service\n" \
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

create_service_file: pitboss_watchdog.service

install_service: pitboss_watchdog.service
	sudo cp "$(FOLDER)/$<" "$(SYSTEMD_INSTALL_DIR)/$<"
	sudo systemctl daemon-reload
	sudo systemctl enable "$<"
	@echo "Service enabled, but not started. " \
		"Call 'systemctl start $<' to start service."

uninstall_service: pitboss_watchdog.service
	sudo systemctl stop "$<"
	sudo systemctl disable "$<"
	sudo rm "$(SYSTEMD_INSTALL_DIR)/$<"

start_service: pitboss_watchdog.service
	sudo systemctl start "$<"

# ====================================================

install_deps_local:
	$(PYTHON_BIN) -m pip install -t $(SITE_PACKAGES) $(PIP_PACKAGES)

install_deps_global:
	sudo $(PYTHON_BIN) -m pip install $(PIP_PACKAGES)
