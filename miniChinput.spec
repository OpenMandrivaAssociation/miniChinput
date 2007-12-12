%define name miniChinput
%define ver 0.1.9
%define release %mkrel 4

# to define when building for PRC
#%define build_for_PRC 1

Summary: A X Input Method Server for Chinese
Name: %{name}
Version: %{ver}
Release: %{release}

License: GPL
Group: System/Internationalization
Requires: locales-zh
URL: http://sourceforge.net/projects/minichinput
Source: %{name}-0.1.9.tar.gz
Patch0: %{name}-0.1.9-rxvt.patch
# allow spaces invalue fields of config file (a lot of fonts have
# spaces in their names) -- pablo
Patch4: miniChinput-0.1.9-spaces.patch.bz2
# patch to make Chinput work in all Chinese locales (that is, also
# with 'zh_HK' and 'zh_SG' -- pablo
Patch5: miniChinput-0.1.9-zh_locales.patch.bz2
# patch to comply with Chinese policy requirements about -- pablo
Patch6: miniChinput-0.1.9-oem_CN.patch.bz2

Patch7:	minichinput-fix-compile.patch.bz2

BuildRequires: imlib-devel XFree86-devel fontconfig
Prefix: %{_prefix}
Buildroot: %_tmppath/%name-%version-%release-root
Conflicts: Chinput
Obsoletes: Chinput

%description
Chinput is an X Input Method allowing to type in chinese in X applications
that follow the XIM input method standard.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch0 -p1 -b .rxvt
%patch4 -p1 -b .spaces
%patch5 -p1 -b .zh_locales
%if %build_for_PRC
%patch6 -p0
%endif

%patch7 -p1 -b .fix_gcc_3_4_compile

%build
%configure
make
make data

%install
make prefix=$RPM_BUILD_ROOT/usr install
make prefix=$RPM_BUILD_ROOT/usr data-install

install -d %buildroot/%_iconsdir
install -m644 src/icons/chinput.xpm %buildroot/%_iconsdir

install -d %buildroot/%_sysconfdir/chinese
ln -s /usr/lib/Chinput/Chinput.ad %buildroot/%_sysconfdir/chinese/Chinput.ad

%post
# gbrxvt will use the chinput as the input server for GB2312 users.
if [ -r /usr/X11R6/bin/rxvt ]; then
    if [ -f /usr/X11R6/bin/rxvt ]; then
            perl -pi -e "s/xcin-zh_CN.GB2312/Chinput/g" /usr/X11R6/bin/rxvt
    fi
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc doc/{BUGS,CHANGES,COPYING,Chinese/,INSTALL,README,TODO,USAGE}
%dir %_sysconfdir/chinese
%_sysconfdir/chinese/Chinput.ad
/usr/bin/chinput
/usr/lib/Chinput
%_iconsdir/*.xpm
%_mandir/man1/chinput.1*

