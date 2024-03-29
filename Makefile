#
# Makefile - build wrapper for py2pack on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	PY2PACKPKGS below
#
#	Set up local 

REPOBASE=file://$(PWD)
#REPOBASE=http://localhost

PY2PACKPKGS+=python-metaextract-srpm

PY2PACKPKGS+=python-py2pack-srpm

REPOS+=py2packrepo/el/7
REPOS+=py2packrepo/el/8
REPOS+=py2packrepo/fedora/35

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=py2packrepo-7-x86_64.cfg
CFGS+=py2packrepo-8-x86_64.cfg
CFGS+=py2packrepo-f35-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=centos+epel-7-x86_64.cfg
MOCKCFGS+=centos-stream+epel-8-x86_64.cfg
MOCKCFGS+=fedora-35-x86_64.cfg

all:: $(CFGS) $(MOCKCFGS) $(REPODIRS)
install:: $(CFGS) $(MOCKCFGS) $(REPODIRS)
install:: $(PY2PACKPKGS)
all:: install

.PHONY: build getsrc install clean
build getsrc install clean::
	@for name in $(PY2PACKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# Dependencies
python-py2pack-srpm:: python-metaextract-srpm

# Actually build in directories
.PHONY: $(PY2PACKPKGS)
$(PY2PACKPKGS)::
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
.PHONY: $(REPOS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo -q `dirname $@`

.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

py2packrepo-7-x86_64.cfg: /etc/mock/centos+epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/centos+epel-7-x86_64/py2packrepo-7-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[py2packrepo]' >> $@
	@echo 'name=py2packrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/py2packrepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

py2packrepo-8-x86_64.cfg: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/centos-stream+epel-8-x86_64/py2packrepo-8-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[py2packrepo]' >> $@
	@echo 'name=py2packrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/py2packrepo/el/8/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

py2packrepo-f35-x86_64.cfg: /etc/mock/fedora-35-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-35-x86_64/py2packrepo-f35-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[py2packrepo]' >> $@
	@echo 'name=py2packrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/py2packrepo/fedora/35/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@


$(MOCKCFGS)::
	ln -sf --no-dereference /etc/mock/$@ $@

repo: py2packrepo.repo
py2packrepo.repo:: Makefile py2packrepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	@for name in $(PY2PACKPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean: clean
	rm -rf $(REPOS)

maintainer-clean: distclean
	rm -rf $(PY2PACKPKGS)
