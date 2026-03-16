%global with_tag 1

Name:                  wmbusmeters
%global forgeurl       https://github.com/weetmuts/%{name}

%if %{with_tag}
%global tag            2.0.0
Version:               %{tag}
%else
%global date           20210813
%global commit         8dd3e87c44ecb2e3fc46f7bc6df9ea6195c8b988
Version:               1.4.0
%endif

%forgemeta

Release:               1%{?dist}
Summary:               Read the wireless mbus protocol to acquire utility meter readings
License:               GPL-3.0-or-later
Url:                   %{forgeurl}
Source0:               %{forgesource}
# Default configuration file
# Stores all logs in journald
Source1:               file://%{name}.conf
# Systemd service file
Source2:               file://%{name}.service

BuildRequires:         /usr/bin/git
BuildRequires:         /usr/bin/make
BuildRequires:         gcc-c++
BuildRequires:         systemd-rpm-macros
BuildRequires:         pkgconfig(ncurses)
BuildRequires:         pkgconfig(librtlsdr)
BuildRequires:         pkgconfig(libusb-1.0)
BuildRequires:         pkgconfig(libxml-2.0)

Requires:              rtl-wmbus >= 0-18


%description
The program receives and decodes C1,T1 or S1 telegrams
(using the wireless mbus protocol) to acquire utility meter readings.
The readings can then be published using MQTT, curled to a REST api,
inserted into a database or stored in a log file.


%prep
%forgeautosetup -S git
# For https://fedoraproject.org/wiki/Changes/Unify_bin_and_sbin
# Unfortunately other distros does not have similar plan so we cannot
# upstream the change for now.
sed -i 's#/sbin#/bin#g' scripts/install_binaries.sh


%build
%set_build_flags
%{make_build} STRIP=true COMMIT_HASH="" TAG=%{version} COMMIT=%{version} \
    TAG_COMMIT=%{version}%{distprefix} CHANGES=""


%install
%set_build_flags
%{make_install} STRIP=true COMMIT_HASH="" TAG=%{version} COMMIT=%{version} \
    TAG_COMMIT=%{version} CHANGES="" \
    DESTDIR=%{buildroot} EXTRA_INSTALL_OPTIONS="--no-adduser"

# We are using journald
rm -rf %{buildroot}%{_sysconfdir}/logrotate.d/

# Create directory for storing pid files.
install -m 0755 -d %{buildroot}/%{_rundir}/%{name}/

# Fix systemd unit dir location
mv %{buildroot}/lib %{buildroot}/%{_prefix}

# We are installing template version
rm -f %{buildroot}%{_unitdir}/%{name}.service

# Install default configuration file
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

# Install systemd service file
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service


%files
%license LICENSE
%doc README.md CHANGES
%dir %{_sysconfdir}/%{name}.d/
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/wmbusmetersd
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}*
%ghost %{_rundir}/%{name}/


%post
%systemd_post %{name}.service
 
%preun
%systemd_preun %{name}.service
 
%postun
%systemd_postun_with_restart %{name}.service


%changelog
* Mon Mar 16 2026 Jan Kundrát <jkt@jankundrat.com> - 2.0.0-1
- Initial release
