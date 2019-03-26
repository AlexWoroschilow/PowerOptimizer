build = build
buildroot = $(shell pwd)/build
Release=$(shell date +"%Y%m%d")
Version = 0.1

all: build

build:
	rm -f ./noarch/*
	rpmbuild -bb ./project.spec --build-in-place --buildroot=$(buildroot) --define "_rpmdir $(shell pwd)"
	sudo alien --to-deb --scripts noarch/performance-$(Version)-$(Release).noarch.rpm
	mv *.deb ./noarch

