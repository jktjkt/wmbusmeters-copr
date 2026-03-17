%global with_tag 1

Name:       wmbusmeters
Version:    {{{ git_version name=wmbusmeters lead= }}}
VCS:        {{{ git_dir_vcs }}}
Source:     {{{ git_dir_pack }}}

%global forgeurl       https://github.com/wmbusmeters/%{name}

%forgemeta

Release:               1%{?dist}
Summary:               Read the wireless mbus protocol to acquire utility meter readings
License:               GPL-3.0-or-later
Url:                   %{forgeurl}

BuildRequires:         /usr/bin/git
BuildRequires:         /usr/bin/make
BuildRequires:         gcc-c++
BuildRequires:         systemd-rpm-macros
BuildRequires:         pkgconfig(ncurses)
BuildRequires:         pkgconfig(librtlsdr)
BuildRequires:         pkgconfig(libusb-1.0)
BuildRequires:         pkgconfig(libxml-2.0)


%description
The program receives and decodes C1,T1 or S1 telegrams
(using the wireless mbus protocol) to acquire utility meter readings.
The readings can then be published using MQTT, curled to a REST api,
inserted into a database or stored in a log file.

%prep
{{{ git_dir_setup_macro }}}

# For https://fedoraproject.org/wiki/Changes/Unify_bin_and_sbin
# Unfortunately other distros does not have similar plan so we cannot
# upstream the change for now.
sed -i 's#/sbin#/bin#g' scripts/install_binaries.sh


%build
%configure
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


%changelog
{{{ git_changelog name=wmbusmeters }}}
