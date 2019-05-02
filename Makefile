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
REPOS+=py2packrepo/fedora/29
REPOS+=py2packrepo/fedora/30

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=py2packrepo-7-x86_64.cfg
CFGS+=py2packrepo-f29-x86_64.cfg
CFGS+=py2packrepo-f30-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=fedora-30-x86_64.cfg
MOCKCFGS+=fedora-29-x86_64.cfg
MOCKCFGS+=epel-7-x86_64.cfg

all:: $(CFGS) $(MOCKCFGS)
all:: $(REPODIRS)
all:: $(PY2PACKPKGS)

all install clean:: FORCE
	@for name in $(PY2PACKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# Build for locacl OS
build:: FORCE
	@for name in $(PY2PACKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done

# Dependencies
python-py2pack-srpm:: python-metaextract-srpm

# Actually build in directories
$(PY2PACKPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo `dirname $@`


.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

$(MOCKCFGS)::
	ln -sf /etc/mock/$@ $@

py2packrepo-7-x86_64.cfg: epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-7-x86_64/py2packrepo-7-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[py2packrepo]' >> $@
	@echo 'name=py2packrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/py2packrepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=3' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@.out
	@mv $@.out $@

py2packrepo-f29-x86_64.cfg: fedora-29-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-29-x86_64/py2packrepo-29-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[py2packrepo]' >> $@
	@echo 'name=py2packrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/py2packrepo/fedora/29/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=3' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@.out
	@mv $@.out $@

py2packrepo-f30-x86_64.cfg: fedora-30-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-30-x86_64/py2packrepo-30-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[py2packrepo]' >> $@
	@echo 'name=py2packrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/py2packrepo/fedora/30/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=3' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@.out
	@mv $@.out $@



repo: py2packrepo.repo
py2packrepo.repo:: py2packrepo.repo.in
	sed 's|@REPOBASEDIR@|$(PWD)|g' $@.in > $@
py2packrepo.repo::
	@cmp -s $@ /etc/yum.repos.d/$@ || \
	    diff -u $@ /etc/yum.repos.d/$@

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	@for name in $(PY2PACKPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean:
	rm -rf $(REPOS)

maintainer-clean:
	rm -rf $(PY2PACKPKGS)

FORCE::

