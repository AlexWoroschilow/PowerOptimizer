RPM_PROJECT= power-optimizer-0.2
RPM_SOURCE= ~/rpmbuild/SOURCES

dump-source-clean:
	@rm -rf $(RPM_SOURCE)/$(RPM_PROJECT)
	@mkdir -p $(RPM_SOURCE)/$(RPM_PROJECT)

dump-source-copy:
	@mkdir -p $(RPM_SOURCE)/$(RPM_PROJECT)/usr/bin
	@mkdir -p $(RPM_SOURCE/usr/lib/power-optimizer/)/$(RPM_PROJECT)/usr/lib/power-optimizer
	@mkdir -p $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/power-optimizer/udev/rules.d
	
	@cp -R lib $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/power-optimizer
	@cp -R src $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/power-optimizer
	@cp -R res $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/power-optimizer
	@cp power-optimizer.py $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/power-optimizer/
	@cp 70-power.rules $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/power-optimizer/udev/rules.d/
	
	@find $(RPM_SOURCE)/$(RPM_PROJECT) -name '.git' -exec rm -rf {} +
	@find $(RPM_SOURCE)/$(RPM_PROJECT) -name '*.pyc' -exec rm -f {} +
	@find $(RPM_SOURCE)/$(RPM_PROJECT) -name '*.class' -exec rm -f {} +

dump-source-compress:
	tar -czf $(RPM_SOURCE)/$(RPM_PROJECT).tar.gz -C $(RPM_SOURCE) $(RPM_PROJECT)

rpm: dump-source-clean dump-source-copy dump-source-compress
	@rpmbuild -ba ./project.spec
