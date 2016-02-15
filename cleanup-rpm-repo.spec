Name:		cleanup-rpm-repo
Version:	1
Release:	1%{?dist}
Summary:	Simple tool to cleanup old files from an RPM repository

Group:		Applications/System
License:	WTFPL
URL:		https://github.com/abustany/cleanup-rpm-repo
Source0:	argparse.py
Source1:	cleanup-rpm-repo.py
Source2:	COPYING

Requires:	rpm-python
Requires:	yum

%description
Simple script to cleanup the old files from an RPM repository, optionally
keeping a number of old versions for each package.

%prep

%build

%install
install -m 0644 -D %{SOURCE0} %{buildroot}/opt/%{name}/argparse.py
install -m 0755 -D %{SOURCE1} %{buildroot}/opt/%{name}/cleanup-rpm-repo.py

%files
/opt/%{name}

%changelog
* Tue Dec 03 2013 Adrien Bustany <adrien@bustany.org> - 1
- Initial specfile
