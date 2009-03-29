Summary:	Modified version of Descent 1
Name:		d1x
Version:	1.43
Release:	8%{?dist}
License:	non-commercial
Group:		Amusements/Games
Source0:	http://home.zonnet.nl/jwrdegoede/d1x143sc.tar.bz2
Source1:	http://home.zonnet.nl/jwrdegoede/d1swdf.tar.gz
Source2:	http://d1x.warpcore.org/files/d1bigfnt.zip
# first batch of patches, many many patches because upstream is dead.
Patch0:		%{name}-config.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-fix.patch
Patch3:		%{name}-paths.patch
Patch4:		%{name}-maths.patch
Patch5:		%{name}-types.patch
Patch6:		%{name}-gcc3.patch
Patch7:		%{name}-joystick.patch
Patch8:		%{name}-assert.patch
Patch9:		%{name}-fixc.patch
Patch10:	%{name}-gcc34.patch
Patch11:	%{name}-shareware-fixes.patch
Patch12:	%{name}-cvs-fixes.patch
Patch13:	%{name}-miscfixes.patch
Patch14:	%{name}-cvs-fixes2.patch
Patch15:	%{name}-gnuasm.patch
Patch16:	%{name}-new-sdl.patch
# d1x has been revived as the dxx-rebirth project, I'm honored to say that they
# have used the livna SRPM's as a starting position and that their tarballs
# thus include all of the above patches. However there releases aren't all
# that stable so I've done a diff between 1.43 + all our above patches and
# their latest release (0.42), and cherry picked the good stuff (I hope):
Patch21:        d1x-rebirth-fixes.patch
Patch22:        d1x-rebirth-highresbrief.patch
Patch23:        d1x-rebirth-mode-handling.patch
Patch24:        d1x-rebirth-mouselook.patch
Patch25:        d1x-rebirth-ogl.patch
# these patches are fixes/improvements on top of the d1x-rebirth patches
Patch31:        d1x-post-rebirth-fixes.patch
Patch32:        d1x-fix-rebirth-ogl.patch
Patch33:        d1x-music.patch
Patch34:        d1x-help.patch
Patch35:        d1x-unixify.patch
Patch36:        d1x-store-res-in-plx.patch
Patch37:        d1x-playerfile-compat.patch
Patch38:        d1x-use-reg-save-in-sw.patch
Patch39:        d1x-playerfile-compat-fix.patch
# and patches added much later to keep things compiling with the latest gcc
Patch40:        d1x-gcc43.patch
URL:		http://d1x.warpcore.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	SDL-devel >= 1.1
BuildRequires:	mesa-libGL-devel mesa-libGLU-devel
%ifarch %{ix86}
BuildRequires:	nasm
%endif

%description
D1X is a modification of the Descent 1 source that was released by
Parallax. It's mostly compatible with the Descent 1 v1.5, both in
multiplayer and on the local machine.


%package full
Summary:	D1X - binaries for full version of game
Group:		Amusements/Games

%description full
D1X is a modification of the Descent 1 source that was released by
Parallax. It's mostly compatible with the Descent 1 v1.5, both in
multiplayer and on the local machine.

This package contains D1X binaries for the full (registered/commercial) version
of the game. You will need to place the full version data-files in
/usr/share/%{name}/full .


%package shareware
Summary:	D1X - binaries for shareware version of game
Group:		Amusements/Games

%description shareware
D1X is a modification of the Descent 1 source that was released by
Parallax. It's mostly compatible with the Descent 1 v1.5, both in
multiplayer and on the local machine.

This package contains D1X binaries and data-files for the shareware version of
the game.


%prep
%setup -q -n %{name}
# lots of patches, so no backups as those are useless, since some files
# get patched many times.
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

%patch21 -p1 
%patch22 -p1
%patch23 -p1
%patch24 -p1
# patch25 is opengl only and gets applied after building the non ogl version.

%patch31 -p1
# patch32 is opengl only and gets applied after building the non ogl version.
%patch33 -p1 -E
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1

%patch40 -p1


%build
mkdir -p lib
echo "DEBUGABLE = 1" >> defines.in
%ifnarch %{ix86}
echo "NO_ASM = 1" >> defines.in
%endif
%ifarch sparc sparc64
echo "BIGENDIAN = 1" >> defines.in
%endif

cp defines.in defines.mak
echo "SDL_IO = 1" >> defines.mak
make	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPTFLAGS="$RPM_OPT_FLAGS \
	-DD1XDATAPATH=\\\"%{_datadir}/%{name}/full/\\\""
mv d1x143 d1x-sdl-full

make clean
echo "SHAREWARE = 1" >> defines.mak
make	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPTFLAGS="$RPM_OPT_FLAGS \
	-DD1XDATAPATH=\\\"%{_datadir}/%{name}/d1shar/\\\""
mv d1x143sh d1x-sdl-share

# this patch isn't applied until now as this makes some huge video changes
# (d1x-rebirth scalable cockpit code) which seem to break (cause crashes in) 
# the software renderer
patch -p1 < %{PATCH25}
patch -p1 < %{PATCH32}
make clean
cp -f defines.in defines.mak
echo "SDLGL_IO = 1" >> defines.mak
make	CC="%{__cc}" \
	CXX="%{__cxx}" \
	LFLAGS="-L/usr/X11R6/%{_lib}" \
	OPTFLAGS="$RPM_OPT_FLAGS \
	-DD1XDATAPATH=\\\"%{_datadir}/%{name}/full/\\\""
mv d1x143_ogl d1x-gl-full

make clean
echo "SHAREWARE = 1" >> defines.mak
make	CC="%{__cc}" \
	CXX="%{__cxx}" \
	LFLAGS="-L/usr/X11R6/%{_lib}" \
	OPTFLAGS="$RPM_OPT_FLAGS \
	-DD1XDATAPATH=\\\"%{_datadir}/%{name}/d1shar/\\\""
mv d1x143sh_ogl d1x-gl-share


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/d1x
install -d $RPM_BUILD_ROOT%{_datadir}/d1x/full
install -d $RPM_BUILD_ROOT%{_datadir}/d1x/d1shar
install d1x-*-* $RPM_BUILD_ROOT%{_bindir}
tar x -z -C $RPM_BUILD_ROOT%{_datadir}/d1x -f %{SOURCE1}
unzip -d $RPM_BUILD_ROOT%{_datadir}/d1x/d1shar %{SOURCE2}
unzip -d $RPM_BUILD_ROOT%{_datadir}/d1x/full   %{SOURCE2}


%clean
rm -rf $RPM_BUILD_ROOT


%files full
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/d1x-sdl-full
%attr(755,root,root) %{_bindir}/d1x-gl-full
%{_datadir}/d1x/full/*
%doc bugs.txt d1x.faq d1x.ini d1x.txt d1x140.txt license.txt readme.d1x readme.org todo.txt
%dir %{_datadir}/d1x
%dir %{_datadir}/d1x/full

%files shareware
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/d1x-sdl-share
%attr(755,root,root) %{_bindir}/d1x-gl-share
%{_datadir}/d1x/d1shar/*
%doc bugs.txt d1x.faq d1x.ini d1x.txt d1x140.txt license.txt readme.d1x readme.org todo.txt
%dir %{_datadir}/d1x
%dir %{_datadir}/d1x/d1shar


%changelog
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
  -Search for custom levels in %{_datadir}/d1x/full,~/.d1x and a
   user configurable dir.
  -Fix/add music playback.
  -DesktopEntries
