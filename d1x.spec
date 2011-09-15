%global rebirth_version 0.57.1

Summary:	Descent 1 game engine (d1x-rebirth version)
Name:		d1x
Version:	1.43
Release:	9.rebirth_v%{rebirth_version}%{?dist}
License:	non-commercial
Group:		Amusements/Games
Source0:	http://downloads.sourceforge.net/dxx-rebirth/d1x-rebirth_v%{rebirth_version}-src.tar.gz
Source1:	d1x-rebirth.sh
Source2:	d1swdf.tar.gz
Patch0:		d1x-rebirth-v0.57.1-libmath.patch
Patch1:		d1x-rebirth-v0.57.1-physfs_v1.patch
Patch2:		d1x-rebirth-v0.57.1-split-regular-and-slide-invert.patch
Patch3:		d1x-rebirth-v0.57.1-desktop.patch
URL:		http://www.dxx-rebirth.com/
BuildRequires:	SDL-devel mesa-libGL-devel mesa-libGLU-devel
BuildRequires:	desktop-file-utils dos2unix
Requires:	opengl-games-utils >= 0.2
Requires:	hicolor-icon-theme
Provides:	%{name}-full = %{version}-%{release}
Obsoletes:	%{name}-full < %{version}-%{release}

%description
D1X is a modification of the Descent 1 source that was released by
Parallax. It's mostly compatible with the Descent 1 v1.5, both in
multiplayer and on the local machine.

To play Descent1 you need to either need the full (registered/commercial)
version of the game and place the full version data-files in
%{_datadir}/%{name}/full; or install the d1x-shareware package.


%package shareware
Summary:	Shareware version of Descent 1
Group:		Amusements/Games
Requires:	%{name} = %{version}-%{release}

%description shareware
D1X is a modification of the Descent 1 source that was released by
Parallax. It's mostly compatible with the Descent 1 v1.5, both in
multiplayer and on the local machine.

This package contains the shareware version of the game.


%prep
%setup -q -n d1x-rebirth_v%{rebirth_version}-src
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
dos2unix -k *.txt


%build
COMMON_FLAGS="prefix=/usr sharepath=%{_datadir}/%{name}/full ipv6=1 verbosebuild=1"
export CFLAGS="$RPM_OPT_FLAGS"
scons $COMMON_FLAGS opengl=0
mv d1x-rebirth d1x-rebirth-sdl
scons $COMMON_FLAGS opengl=1
mv d1x-rebirth d1x-rebirth-gl


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/d1x/full
mkdir -p $RPM_BUILD_ROOT%{_datadir}/d1x/d1shar
install -m 755 d1x-rebirth-sdl $RPM_BUILD_ROOT%{_bindir}
install -m 755 d1x-rebirth-gl $RPM_BUILD_ROOT%{_bindir}
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/d1x-rebirth
tar x -z -C $RPM_BUILD_ROOT%{_datadir}/d1x -f %{SOURCE2}
# fixup permissions from tarbal
chmod 644 $RPM_BUILD_ROOT%{_datadir}/d1x/d1shar/README
# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor "" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  d1x-rebirth.desktop
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
install -p -m 644 d1x-rebirth.xpm \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc COPYING.txt README.txt RELEASE-NOTES.txt
%{_bindir}/d1x-rebirth*
%dir %{_datadir}/d1x
%dir %{_datadir}/d1x/full
%{_datadir}/applications/d1x-rebirth.desktop
%{_datadir}/icons/hicolor/128x128/apps/d1x-rebirth.xpm

%files shareware
%defattr(-,root,root,-)
%{_datadir}/d1x/d1shar


%changelog
* Thu Sep 15 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 1.43-9.rebirth_v0.57.1
- Update to latest d1x-rebirth release v0.57.1
- One binary now can now handle both the shareware and full versions:
  - Drop the -full subpackage
  - Put the engine in the main package
  - Make the main package obsolete the -full subpackage
  - Make the -shareware package only contain the shareware data files
- Add a desktop file and icon

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.43-8
- rebuild for new F11 features

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-7
- Rebuild for buildsys cflags issue

* Wed Jul 23 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-6
- Release bump for rpmfusion build

* Sat Oct 14 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-5
- Fix reading of player file (playerfile compat code) when using addon missions

* Tue Sep 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-4
- Fix building with newer SDL lib which is not directly linked against libX11

* Sun Sep 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-3
- Rebuild for FC-6
- Tried switching to d1x-rebirth sources but didn't because they are unstable
  instead the following d1x-rebirth features were lifted:
  -scaleable cockpits in opengl mode
  -support for highres briefingscreens (download them from the dxx-rebirth web)
  -mouselook support
  -16:9 monitor support
  -store the resolution you're playing at in playername.dlx
- Add/restore music playback, now you can enjoy the original descent music!
- The player and other descent config files are now stored in ~/.d1x, so
  if you've got a player you want to keep move its files to ~/.d1x
- The shareware version now uses the same game load/save code as the registered
  version allowing in game saving (ALT-F2 saves, ALT-F3 restores)
- The shareware version can now properly read player files written by the
  registered version and vica versa

* Sat Mar 18 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.43-2
- Increase release after fixing BRs once more

* Fri Mar 17 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-1
- Fix BuidRequires for FC-5  

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Aug 10 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-0.lvn.4
- Remove -Wno-pointer-sign from CFLAGS, this option is not valid for gcc 3.4 .

* Sun Aug  7 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-0.lvn.3
- Drop Patch 13, intergrate into Patch 0.
- Add new Patch 13 which introduces some fixes from CVS.
- Added Patch 14 which fixes:
  -a few buffer overflows caught by gcc 4 and an uninitialised var warning.
  -the sliders in the menus with newer gcc / glibc
   (or x86_64, but doesn't seem 64 bit related)
  -the 2 initial screens with opengl
  -made /usr/share/d1x/d1shar or /full the default mission dir
  -don't use descent2 fonts, these aren't in the hog file instead use fonts
   from d1bigfnt.zip .
- Add d1bigfnt.zip and install the fonts in /usr/share/d1x/d1shar or /full.
- Build without -fomit-framepointer to allow debugging (DEBUGABLE = 1).
- Add Patch 15 to fix i386 (asm) compile.

* Mon Apr 29 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-0.lvn.2
- Added Patch 13 which fixes compilation with gcc4

* Mon Jan  3 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.43-0.lvn.1
- First Livna release, based on PLD SRPM.
- Patches 0-10 are from PLD, have been reviewed and are all compilation fixes.
- Patch 11 fixes 2 issues with the shareware version:
  -Pressing F1 no longer causes a segfault.
  -Saving now works.
- Patch 12 brings in various fixes from the d1x cvs version.
- Plans:
  -Save settings/games in ~/.d1x instead of in wd.
  -Search for custom levels in /usr/share/d1x/full,~/.d1x and a
   user configurable dir.
  -Fix/add music playback.
  -DesktopEntries
