# Invoke with "make -f checks.mk" to run all checks locally

commits := master..HEAD

ifeq ($(shell whoami),docker)
	PREFIX :=
	SUFFIX :=
else
	PREFIX := debpic "
	SUFFIX := "
endif

all: black mypy pytest package lintian clean
	@echo SUCCESS

black:
	$(PREFIX) black --check . $(SUFFIX)

isort:
	$(PREFIX) isort --check . $(SUFFIX)

mypy:
	$(PREFIX) mypy . $(SUFFIX)

pytest:
	$(PREFIX) pytest-3 --cov-report=xml --cov $(SUFFIX)

package:
	$(PREFIX) dpkg-buildpackage && mv-debs $(SUFFIX)

lintian: package
	$(PREFIX) lintian --fail-on warning ./built_packages/*.changes  $(SUFFIX)

clean:
	$(PREFIX) dpkg-buildpackage --target=clean && \
			  py3clean . && \
			  rm -rf .mypy_cache .pytest_cache .coverage coverage.xml $(SUFFIX)