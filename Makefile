RPM_PROJECT= pcoptimizer-0.2
RPM_SOURCE= ~/rpmbuild/SOURCES

dump-source-clean:
	@rm -rf $(RPM_SOURCE)/$(RPM_PROJECT)
	@mkdir -p $(RPM_SOURCE)/$(RPM_PROJECT)

dump-source-copy:
	@mkdir -p $(RPM_SOURCE)/$(RPM_PROJECT)/usr/bin
	@mkdir -p $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/pcoptimizer
	@mkdir -p $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/pcoptimizer/udev/rules.d
	
	@cp -R lib $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/pcoptimizer
	@cp -R modules $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/pcoptimizer
	@cp -R res $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/pcoptimizer

	@cp main.py $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/pcoptimizer/
	@cp 70-power.rules $(RPM_SOURCE)/$(RPM_PROJECT)/usr/lib/pcoptimizer/udev/rules.d/
	
	@find $(RPM_SOURCE)/$(RPM_PROJECT) -name '.git' -exec rm -rf {} +
	@find $(RPM_SOURCE)/$(RPM_PROJECT) -name '*.pyc' -exec rm -f {} +
	@find $(RPM_SOURCE)/$(RPM_PROJECT) -name '*.class' -exec rm -f {} +

dump-source-compress:
	tar -czf $(RPM_SOURCE)/$(RPM_PROJECT).tar.gz -C $(RPM_SOURCE) $(RPM_PROJECT)

rpm: dump-source-clean dump-source-copy dump-source-compress
	@rpmbuild -ba ./project.spec
