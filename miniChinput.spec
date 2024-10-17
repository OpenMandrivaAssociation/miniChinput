%define name miniChinput
%define ver 0.1.9
%define release  9


Summary: A X Input Method Server for Chinese
Name: %{name}
Version: %{ver}
Release: %{release}

License: GPL
Group: System/Internationalization
Requires: locales-zh
URL: https://sourceforge.net/projects/minichinput
Source: %{name}-0.1.9.tar.gz
Patch0: %{name}-0.1.9-rxvt.patch
# allow spaces invalue fields of config file (a lot of fonts have
# spaces in their names) -- pablo
Patch4: miniChinput-0.1.9-spaces.patch
# patch to make Chinput work in all Chinese locales (that is, also
# with 'zh_HK' and 'zh_SG' -- pablo
Patch5: miniChinput-0.1.9-zh_locales.patch
# patch to comply with Chinese policy requirements about -- pablo
Patch6: miniChinput-0.1.9-oem_CN.patch

Patch7:	minichinput-fix-compile.patch
Patch8: miniChinput-0.1.9-gcc45.patch
Patch9: miniChinput-0.1.9-link.patch
BuildRequires: imlib-devel
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xft)
BuildRequires: pkgconfig(xt)
Conflicts: Chinput
Obsoletes: Chinput

%description
Chinput is an X Input Method allowing to type in chinese in X applications
that follow the XIM input method standard.

%prep
%setup -q
%patch0 -p1 -b .rxvt
%patch4 -p1 -b .spaces
%patch5 -p1 -b .zh_locales
%patch6 -p0

%patch7 -p1 -b .fix_gcc_3_4_compile
%patch8 -p0
%patch9 -p0

%build
%configure2_5x
make CC="gcc %ldflags"
make data

%install
rm -fr %buildroot
make prefix=$RPM_BUILD_ROOT/usr install
make prefix=$RPM_BUILD_ROOT/usr data-install

install -d %buildroot/%_iconsdir
install -m644 src/icons/chinput.xpm %buildroot/%_iconsdir

install -d %buildroot/%_sysconfdir/chinese
ln -s /usr/lib/Chinput/Chinput.ad %buildroot/%_sysconfdir/chinese/Chinput.ad
rm -fr %buildroot/%_docdir/%name-%version

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



%changelog
* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 0.1.9-7mdv2011.0
+ Revision: 636131
- fix link and build with gcc 4.5
- bunzip patches

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 0.1.9-4mdv2008.1
+ Revision: 133079
- fix installing
- kill re-definition of %%buildroot on Pixel's request
- buildrequires X11-devel instead of XFree86-devel
- use %%mkrel
- import miniChinput


* Wed Aug 04 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-4mdk
- remove man pages and makefiles from %%doc
- fix previous changelog

* Fri Jun  4 2004 Laurent Montel <lmontel@mandrakesoft.com> 0.1.9-3mdk
- Rebuild
- Fix compile

* Thu Sep 04 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.1.9-2mdk
- fixed BuildRequires

* Fri Aug 29 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.1.9-1mdk
- updated to 0.1.9

* Wed Mar 13 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.0.3-2mdk
- adapted to mdk, merged with Chinput changes and config

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Yu Shao <yshao@redhat.com> 35, 36
- Added memory leak patch from James Su, i18n@xfree86.org
- Added doc to binary RPM

* Thu Jan 7 2003 Yu Shao <yshao@redhat.com> 34
- fixing dependency problem #80964

* Mon Dec 2 2002 Yu Shao <yshao@redhat.com> 32
- /usr/lib/Chinput ownership fix #73957
- minichinput-0.0.3-compile.patch

* Thu Nov 14 2002 Yu Shao <yshao@redhat.com>
- CVS build

* Fri Oct 4 2002 Yu Shao <yshao@redhat.com>
- IA64 build bug fix

* Fri Sep 13 2002 Yu Shao <yshao@redhat.com>
- add hotkey Shift-F3 to switch input style,
- to avoid the conflict with GNOME's Alt-Space

* Wed Aug 28 2002 Yu Shao <yshao@redhat.com>
- rebuilt and cleanup

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- rebuilt with new imlib

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com>
- build using gcc-3.2-0.1

* Mon  Jul 8 2002 Yu Shao <yshao@redhat.com>
- make big5 locale work

* Mon  Jul 8 2002 Yu Shao <yshao@redhat.com>
- xft port enhancement, buildrequires

* Mon  Jun 3 2002 Yu Shao <yshao@redhat.com>
- xft porting

* Tue  May 28 2002 Yu Shao <yshao@redhat.com>
- fix gcc3 compiling errors

* Fri  May 10 2002 Yu Shao <yshao@redhat.com>
- fix bugzilla #64688

* Wed  Apr 03 2002 Yu Shao <yshao@redhat.com>
- use zhongyi font in Chinput.ad

* Thu  Mar  14 2002 Yu Shao <yshao@redhat.com>
- recheck license

* Wed  Feb  20 2002 Yu Shao <yshao@redhat.com>
- update miniChinput-0.0.3-iconv.patch

* Thu  Feb  14 2002 Yu Shao <yshao@redhat.com>
- add locale patch to make it more locale robust

* Thu  Jan  31 2002 Yu Shao <yshao@redhat.com>
- add filter to filter unassigned unicode codepoints

* Fri  Jan  26 2002 Yu Shao <yshao@redhat.com>
- New gcc and ia64 patch

* Wed  Dec  5 2001 Yu Shao <yshao@redhat.com>
- Fix no big5 font problem

* Fri  Nov  9 2001 Yu Shao <yshao@redhat.com>
- Add gb18030 stuff and internal code input module

* Fri  Nov  9 2001 Yu Shao <yshao@redhat.com>
- Update to 0.0.3 

* Tue Jul 17 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update to 0.0.2 to fix tab2txt bugs.

* Sun Jul  8 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add ia64 fix

* Tue Jul  3 2001 Yukihiro Nakai <ynakai@redhat.com>
- Exclude ia64 and alpha

* Wed Jun 27 2001 Yukihiro Nakai <ynakai@redhat.com>
- Initial release.

