# Upstream is not really good in doing timely releases, so we use
# a git snapshot of the dxx-rebirth stable-0.60.x branch
%global rebirth_version 0.60
%global snapshotdate 20181218
%global commit af25483d01e444553b70cf70c2c7fb8403875f71
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:	Descent 1 game and shareware data files (d1x-rebirth version)
Name:		d1x
Version:	1.43
Release:	21.rebirth_v%{rebirth_version}.%{snapshotdate}git%{shortcommit}%{?dist}
License:	non-commercial
Source0:	https://github.com/dxx-rebirth/dxx-rebirth/archive/%{commit}/dxx-rebirth-%{shortcommit}.tar.gz
Source1:	d1x-rebirth.sh
Source2:	d2x-rebirth.sh
Source3:	d1swdf.tar.gz
Source4:	https://www.icculus.org/d2x/data/d2shar10.tar.gz
Source5:	d1x-rebirth.appdata.xml
Source6:	d2x-rebirth.appdata.xml
URL:		https://www.dxx-rebirth.com/
BuildRequires:	gcc gcc-c++ libpng-devel
BuildRequires:	SDL-devel SDL_mixer-devel mesa-libGL-devel mesa-libGLU-devel
BuildRequires:	physfs-devel scons desktop-file-utils dos2unix
BuildRequires:	ImageMagick libappstream-glib
Requires:	opengl-games-utils >= 0.2
Requires:	hicolor-icon-theme
Provides:	%{name}-full = %{version}-%{release}
Obsoletes:	%{name}-full < %{version}-%{release}
Provides:	%{name}-shareware = %{version}-%{release}
Obsoletes:	%{name}-shareware < %{version}-%{release}

%description
D1X is a modification of the Descent 1 source that was released by
Parallax. It's mostly compatible with the Descent 1 v1.5, both in
multiplayer and on the local machine.

This package comes with the shareware version of the game. If you want to
play the full (registered/commercial) version of the game, place the
descent.hog and descent.pig data-files from your registered descent version
in %{_datadir}/d1x/full; or in $HOME/.d1x-rebirth.


%package -n d2x
Summary:	Descent 2 game and shareware data files (d2x-rebirth version)
Requires:	opengl-games-utils >= 0.2
Requires:	hicolor-icon-theme

%description -n d2x
D2X is a modification of the Descent 2 source that was released by Parallax.
It's mostly compatible with the original Descent 2, both in multiplayer and
on the local machine.

This package comes with the shareware version of the game. If you want to
play the full (registered/commercial) version of the game, place the
alien1.pig, alien2.pig, fire.pig, groupa.pig, ice.pig, water.pig, descent2.hog,
descent2.ham, descent2.s11 and descent2.s22 data-files from your registered
descent version in %{_datadir}/d2x/full; or in $HOME/.d2x-rebirth.

If you want to have the movies also add the intro-h.mvl, other-h.mvl and
robots-h.mvl files to the dir.


%prep
%setup -q -n dxx-rebirth-%{commit} -a 3 -a 4
# Fixup encoding and CTRL+Z at the end of the orderfrm.txt files
iconv -f CP850 -t UTF-8 d1shar/ORDERFRM.TXT | head -n-3 > ORDERFRM.TXT
touch -r d1shar/ORDERFRM.TXT ORDERFRM.TXT
mv ORDERFRM.TXT d1shar/ORDERFRM.TXT
cat d2shar10/orderfrm.txt | head -n-1 > orderfrm.txt
touch -r d2shar10/orderfrm.txt orderfrm.txt
mv orderfrm.txt d2shar10/orderfrm.txt
# Prepare txt files for %%doc
dos2unix -k d?x-rebirth/*.txt d1shar/*.TXT d1shar/README d2shar10/*.txt
mkdir descent1-shareware-readmes descent2-shareware-readmes
mv d1shar/*.TXT d1shar/README descent1-shareware-readmes
mv d2shar10/*.txt descent2-shareware-readmes
# Prepare the icons for installation
convert d1x-rebirth/d1x-rebirth.xpm d1x-rebirth.png
convert d2x-rebirth/d2x-rebirth.xpm d2x-rebirth.png


%build
COMMON_FLAGS="prefix=/usr d1x_sharepath=%{_datadir}/d1x/full d2x_sharepath=%{_datadir}/d2x/full ipv6=1 verbosebuild=1"
export CXXFLAGS="$RPM_OPT_FLAGS"
scons $COMMON_FLAGS opengl=0
mv d1x-rebirth/d1x-rebirth d1x-rebirth-sdl
mv d2x-rebirth/d2x-rebirth d2x-rebirth-sdl
scons $COMMON_FLAGS opengl=1
mv d1x-rebirth/d1x-rebirth d1x-rebirth-gl
mv d2x-rebirth/d2x-rebirth d2x-rebirth-gl


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/d1x/full
mkdir -p $RPM_BUILD_ROOT%{_datadir}/d1x/d1shar
mkdir -p $RPM_BUILD_ROOT%{_datadir}/d2x/full
mkdir -p $RPM_BUILD_ROOT%{_datadir}/d2x/d2shar
install -m 755 d1x-rebirth-sdl $RPM_BUILD_ROOT%{_bindir}
install -m 755 d1x-rebirth-gl $RPM_BUILD_ROOT%{_bindir}
install -m 755 d2x-rebirth-sdl $RPM_BUILD_ROOT%{_bindir}
install -m 755 d2x-rebirth-gl $RPM_BUILD_ROOT%{_bindir}
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/d1x-rebirth
install -p -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/d2x-rebirth
# Install descent 1 shareware files
install -p -m 644 d1shar/descent.* $RPM_BUILD_ROOT%{_datadir}/d1x/d1shar
# Install descent 2 shareware files
install -p -m 644 d2shar10/d2demo.{pig,hog,ham} \
	$RPM_BUILD_ROOT%{_datadir}/d2x/d2shar
# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
desktop-file-install \
  --remove-key="Version" \
  --set-key="Keywords" --set-value="game;fps;first;person;shooter;descent;" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  d1x-rebirth/d1x-rebirth.desktop
desktop-file-install \
  --remove-key="Version" \
  --set-key="Keywords" --set-value="game;fps;first;person;shooter;descent;" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  d2x-rebirth/d2x-rebirth.desktop
install -m 644 d1x-rebirth.png d2x-rebirth.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
install -p -m 644 %{SOURCE5} %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/appdata
appstream-util validate-relax --nonet \
  $RPM_BUILD_ROOT%{_datadir}/appdata/d1x-rebirth.appdata.xml \
  $RPM_BUILD_ROOT%{_datadir}/appdata/d2x-rebirth.appdata.xml


%files
%doc d1x-rebirth/README.txt d1x-rebirth/RELEASE-NOTES.txt
%license COPYING.txt GPL-3.txt descent1-shareware-readmes
%{_bindir}/d1x-rebirth*
%{_datadir}/d1x
%{_datadir}/appdata/d1x-rebirth.appdata.xml
%{_datadir}/applications/d1x-rebirth.desktop
%{_datadir}/icons/hicolor/128x128/apps/d1x-rebirth.png

%files -n d2x
%doc d2x-rebirth/README.txt d2x-rebirth/RELEASE-NOTES.txt
%license COPYING.txt GPL-3.txt descent2-shareware-readmes
%{_bindir}/d2x-rebirth*
%{_datadir}/d2x
%{_datadir}/appdata/d2x-rebirth.appdata.xml
%{_datadir}/applications/d2x-rebirth.desktop
%{_datadir}/icons/hicolor/128x128/apps/d2x-rebirth.png


%changelog
* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.43-21.rebirth_v0.60.20181218gitaf25483
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 18 2018 Hans de Goede <j.w.r.degoede@gmail.com> - 1.43-20.rebirth_v0.60.20181218gitaf25483
- Update to upstream d1x-rebirth stable-0.60.x branch a.d. 18-12-2018
- Fixes d2x-rebirth crashing when the descent 2 mvl (movie) files are present

* Sun Dec 16 2018 Hans de Goede <j.w.r.degoede@gmail.com> - 1.43-19.rebirth_v0.60
- Update to upstream d1x-rebirth stable-0.60.x branch a.d. 16-12-2018 (rf5026)
- Merge d1x-shareware package into the main-package so that installing d1x
  from e.g. gnome-software always results in a functional game
- Add appdata
- New upstream includes d2x, add a d2x sub-package, including d2x demo levels
- Trim changelog

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.43-18.rebirth_v0.58.1
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.43-17.rebirth_v0.58.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.43-16.rebirth_v0.58.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.43-15.rebirth_v0.58.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 25 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.43-14.rebirth_v0.58.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.43-13.rebirth_v0.58.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar  2 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.43-12.rebirth_v0.58.1
- Update to latest d1x-rebirth release v0.58.1 (rf3162)
- Drop all patches, all upstreamed

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.43-11.rebirth_v0.57.1
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.43-10.rebirth_v0.57.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 1.43-9.rebirth_v0.57.1
- Update to latest d1x-rebirth release v0.57.1
- One binary now can now handle both the shareware and full versions:
  - Drop the -full subpackage
  - Put the engine in the main package
  - Make the main package obsolete the -full subpackage
  - Make the -shareware package only contain the shareware data files
- Add a desktop file and icon
