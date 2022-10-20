#####################
# Hardcode PLF build
%define build_plf 0
#####################

%{?_with_plf: %{expand: %%global build_plf 1}}

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

%define majorver %(echo %{version} | cut -d. -f 1-2)

Summary:	MPD, the Music Player Daemon

Name:		mpd
Version:	0.23.10
Release:	1
License:	GPLv2+
Group:		Sound
Url:		http://www.musicpd.org/
Source0:	http://www.musicpd.org/download/%{name}/%{majorver}/%{name}-%{version}.tar.xz
Source1:	%{name}.conf
Source2:        %{name}.tmpfiles.d
Source3:	%{name}.logrotate
Source100:	%{name}.rpmlintrc
Requires(pre,post):	rpm-helper
Requires(preun,postun):	rpm-helper
BuildRequires:	meson
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(atomic_ops)
%ifnarch %{ix86} %{arm}
BuildRequires:	pkgconfig(smbclient)
%endif
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	avahi-common-devel
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	boost-devel
BuildRequires:	boost-core-devel
BuildRequires:	bzip2-devel
BuildRequires:  python3dist(sphinx)
BuildRequires:	pkgconfig(libcurl) >= 7.18
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(liburing)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(libchromaprint)
# sound servers
BuildRequires:	pkgconfig(alsa) >= 0.9.0
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpulse) >= 0.9.16
BuildRequires:	pkgconfig(fluidsynth) >= 1.1
BuildRequires:	pkgconfig(fmt)
BuildRequires:	pkgconfig(libmms) >= 0.4
BuildRequires:	pkgconfig(openal)
# multimedia formats
BuildRequires:	pkgconfig(ao)
BuildRequires:	pkgconfig(audiofile) >= 0.3
BuildRequires:	pkgconfig(flac) >= 1.2
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libiso9660)
BuildRequires:	pkgconfig(libmodplug)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(libnfs)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libupnp)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(samplerate) >= 0.0.15
BuildRequires:	pkgconfig(shout)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(soxr)
BuildRequires:	pkgconfig(twolame)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vorbisenc)
BuildRequires:	pkgconfig(vorbisfile)
BuildRequires:	pkgconfig(wavpack)
BuildRequires:	pkgconfig(yajl) >= 2.0
BuildRequires:	pkgconfig(zziplib) >= 0.13
BuildRequires:	ffmpeg-devel
BuildRequires:	libgme-devel
BuildRequires:	libmikmod-devel
# doesnt work with version in cooker
#BuildRequires:	libmpcdec-devel
BuildRequires:	wildmidi-devel
BuildRequires:	lame-devel
BuildRequires:	wrap-devel
%if %{build_plf}
BuildRequires:	libfaad2-devel
%endif

%description
Music Player Daemon (MPD) allows remote access for playing music (MP3, Ogg
Vorbis, FLAC, Mod, and wave files) and managing play-lists. MPD is designed
for integrating a computer into a stereo system that provides control for music
playback over a local network. It is also makes a great desktop music player,
especially if you are a console junkie, like front-end options, or restart X
often.
%if %{build_plf}
This package is in restricted repository because it is built with AAC support
of libfaad2, which is patent-protected.
%endif


%prep
%setup -q
%autopatch -p1

%build
# Mad and sidplay option make the build to fail
%meson \
	-Dsystemd_system_unit_dir=%{_unitdir} \
	-Dzeroconf=auto \
	-Dalsa=enabled \
	-Dao=enabled \
	-Daudiofile=enabled \
	-Dcdio_paranoia=enabled \
	-Dcurl=enabled \
	-Dflac=enabled \
	-Dffmpeg=enabled \
	-Dfluidsynth=enabled \
	-Dgme=enabled \
	-Did3tag=enabled \
	-Diso9660=enabled \
	-Djack=enabled \
	-Dopenmpt=disabled \
%ifarch %{ix86} %{arm}
	-Dsmbclient=disabled \
%endif
	-Dsoundcloud=enabled \
	-Dmad=disabled \
	-Dmikmod=enabled \
	-Dmms=enabled \
	-Dmodplug=enabled \
	-Dmpg123=enabled \
	-Dopenal=enabled \
	-Dopus=enabled \
	-Dpulse=enabled \
	-Drecorder=true \
	-Dshout=enabled \
	-Dsidplay=disabled \
	-Dsndfile=enabled \
	-Dtwolame=enabled \
	-Dvorbis=enabled \
	-Dvorbisenc=enabled \
	-Dwave_encoder=true \
	-Dwavpack=enabled \
	-Dwildmidi=enabled \
	-Dzzip=enabled \
        -Dmpcdec=disabled \
	-Dadplug=disabled \
	-Dsndio=disabled \
	-Dlibmpdclient=disabled \
	-Dshine=disabled \
	-Dtremor=disabled \
	-Dsolaris_output=disabled \
%if !%{build_plf}
	-Dfaad=disabled \
%endif
	-Dsqlite=enabled
%meson_build


%install
%meson_install

mkdir -p %{buildroot}%{_localstatedir}/lib/mpd
touch %{buildroot}%{_localstatedir}/lib/mpd/mpd.db
touch %{buildroot}%{_localstatedir}/lib/mpd/mpdstate
mkdir -p %{buildroot}%{_localstatedir}/log/mpd
touch %{buildroot}%{_localstatedir}/log/mpd/mpd.log
touch %{buildroot}%{_localstatedir}/log/mpd/mpd.error
mkdir -p %{buildroot}%{_localstatedir}/run/mpd
mkdir -p %{buildroot}%{_localstatedir}/lib/mpd/playlists
mkdir -p %{buildroot}%{_localstatedir}/lib/mpd/music
mkdir -p %{buildroot}/lib/systemd/system

install -D -m 644 %{SOURCE1} %{buildroot}/etc/mpd.conf
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
rm -rf %{buildroot}/%{_docdir}/mpd

install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/mpd.conf

mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/mpd.conf <<EOF
u mpd
m mpd audio
EOF

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-mpd.preset << EOF
enable mpd.socket
EOF

%files
%doc README.md AUTHORS NEWS doc/mpdconf.example
%{_bindir}/%{name}
#{_mandir}/man1/*
#{_mandir}/man5/*
%{_tmpfilesdir}*
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,mpd,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%defattr(644,mpd,audio)
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd/music
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd/playlists
%ghost %{_localstatedir}/lib/mpd/mpd.db
%ghost %{_localstatedir}/lib/mpd/mpdstate
%attr(755,mpd,audio) %dir /var/log/mpd
%attr(755,mpd,audio) %dir /var/run/mpd
%ghost /var/log/mpd/mpd.log
%ghost /var/log/mpd/mpd.error
%{_presetdir}/86-mpd.preset
%attr(644,root,root) %{_unitdir}/%{name}.service
%attr(644,root,root) %{_unitdir}/%{name}.socket
%attr(644,root,root) %{_userunitdir}/%{name}.service
%attr(644,root,root) %{_sysusersdir}/%{name}.conf
%attr(644,root,root) %{_prefix}/lib/systemd/user/%{name}.socket
%{_mandir}/man1/mpd.1.*
%{_mandir}/man5/mpd.conf.5.*
