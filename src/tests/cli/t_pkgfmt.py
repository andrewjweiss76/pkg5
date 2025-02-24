#!/usr/bin/python3
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
#
# Copyright (c) 2009, 2020, Oracle and/or its affiliates. All rights reserved.
#

from . import testutils
if __name__ == "__main__":
        testutils.setup_environment("../../../proto")
import pkg5unittest

import errno
import os
import pkg.portable as portable
import shutil
import stat
import sys
import tempfile
import unittest

import pkg.portable

class TestPkgFmt(pkg5unittest.CliTestCase):
        pkgcontents = \
            """
#Begin Comment
set name=pkg.fmri value=pkg:/system/kernel@$(PKGVERS)
set name=pkg.description value="core kernel software for a specific instruction-set architecture"
set name=pkg.summary value="Core Solaris Kernel"
set name=info.classification value=org.opensolaris.category.2008:System/Core
set name=variant.arch value=$(ARCH)
set name=variant.opensolaris.zone value=global value=nonglobal
dir path=boot group=sys
$(i386_ONLY)dir path=boot/acpi group=sys
$(i386_ONLY)dir path=boot/acpi/tables group=sys
dir path=boot/solaris group=sys
dir path=boot/solaris/bin group=sys
dir path=etc group=sys
dir path=etc/crypto group=sys
dir path=kernel group=sys
$(i386_ONLY)dir path=kernel/$(ARCH64) group=sys
dir path=kernel/crypto group=sys
dir path=kernel/crypto/$(ARCH64) group=sys
dir path=kernel/dacf group=sys
dir path=kernel/dacf/$(ARCH64) group=sys
dir path=kernel/drv group=sys
dir path=kernel/drv/$(ARCH64) group=sys
dir path=kernel/exec group=sys
dir path=kernel/exec/$(ARCH64) group=sys
dir path=kernel/fs group=sys
dir path=kernel/fs/$(ARCH64) group=sys
dir path=kernel/ipp group=sys
dir path=kernel/ipp/$(ARCH64) group=sys
dir path=kernel/kiconv group=sys
dir path=kernel/kiconv/$(ARCH64) group=sys
dir path=kernel/mac group=sys
dir path=kernel/mac/$(ARCH64) group=sys
dir path=kernel/misc group=sys
dir path=kernel/misc/$(ARCH64) group=sys
dir path=kernel/misc/scsi_vhci group=sys
dir path=kernel/misc/scsi_vhci/$(ARCH64) group=sys
dir path=kernel/sched group=sys
dir path=kernel/sched/$(ARCH64) group=sys
dir path=kernel/socketmod group=sys
dir path=kernel/socketmod/$(ARCH64) group=sys
dir path=kernel/strmod group=sys
dir path=kernel/strmod/$(ARCH64) group=sys
dir path=kernel/sys group=sys
dir path=kernel/sys/$(ARCH64) group=sys
dir path=lib
dir path=lib/svc
dir path=lib/svc/method
dir path=lib/svc/manifest group=sys
dir path=lib/svc/manifest/system group=sys
#Middle Comment
$(i386_ONLY)driver name=acpi_drv perms="* 0666 root sys"
driver name=aggr perms="* 0666 root sys"
driver name=arp perms="arp 0666 root sys"
driver name=bl perms="* 0666 root sys"
driver name=bridge clone_perms="bridge 0666 root sys" policy="read_priv_set=net_rawaccess write_priv_set=net_rawaccess"
$(sparc_ONLY)driver name=bscbus alias=SUNW,bscbus
$(i386_ONLY)driver name=bscbus alias=SVI0101
$(sparc_ONLY)driver name=bscv alias=SUNW,bscv perms="* 0644 root sys"
$(i386_ONLY)driver name=bscv
driver name=clone
driver name=cn perms="* 0620 root tty"
driver name=conskbd perms="kbd 0666 root sys"
driver name=consms perms="mouse 0666 root sys"
driver name=cpuid perms="self 0644 root sys"
$(i386_ONLY)driver name=cpunex alias=cpus
driver name=crypto perms="crypto 0666 root sys"
driver name=cryptoadm perms="cryptoadm 0644 root sys"
$(sparc_ONLY)driver name=dad alias=ide-disk perms="* 0640 root sys"
driver name=devinfo perms="devinfo 0640 root sys" perms="devinfo,ro 0444 root sys"
driver name=dld perms="* 0666 root sys"
driver name=dlpistub perms="* 0666 root sys"
$(sparc_ONLY)driver name=i8042 alias=8042
$(i386_ONLY)driver name=i8042
driver name=icmp perms="icmp 0666 root sys" policy="read_priv_set=net_icmpaccess write_priv_set=net_icmpaccess"
driver name=icmp6 perms="icmp6 0666 root sys" policy="read_priv_set=net_icmpaccess write_priv_set=net_icmpaccess"
$(i386_ONLY)driver name=intel_nb5000 \\
    alias=pci8086,25c0 \\
    alias=pci8086,25d0 \\
    alias=pci8086,25d4 \\
    alias=pci8086,25d8 \\
    alias=pci8086,3600 \\
    alias=pci8086,4000 \\
    alias=pci8086,4001 \\
    alias=pci8086,4003 \\
    alias=pci8086,65c0
$(i386_ONLY)driver name=intel_nhm \\
    alias=pci8086,3423 \\
    alias=pci8086,372a
$(i386_ONLY)driver name=intel_nhmex alias=pci8086,3422
driver name=ip perms="ip 0666 root sys" \\
    policy="read_priv_set=net_rawaccess write_priv_set=net_rawaccess"
driver name=ip6 perms="ip6 0666 root sys" \\
    policy="read_priv_set=net_rawaccess write_priv_set=net_rawaccess"
driver name=ipnet perms="lo0 0666 root sys" \\
    policy="read_priv_set=net_observability write_priv_set=net_observability"
driver name=ippctl
driver name=ipsecah perms="ipsecah 0666 root sys" \\
    policy="read_priv_set=sys_ip_config write_priv_set=sys_ip_config"
driver name=ipsecesp perms="ipsecesp 0666 root sys" \\
    policy="read_priv_set=sys_ip_config write_priv_set=sys_ip_config"
driver name=iptun
driver name=iwscn
driver name=kb8042 alias=pnpPNP,303
driver name=keysock perms="keysock 0666 root sys" \\
    policy="read_priv_set=sys_ip_config write_priv_set=sys_ip_config"
driver name=kmdb
driver name=kssl perms="* 0666 root sys"
driver name=llc1 clone_perms="llc1 0666 root sys"
driver name=lofi perms="* 0600 root sys" perms="ctl 0644 root sys"
driver name=log perms="conslog 0666 root sys" perms="log 0640 root sys"
$(i386_ONLY)driver name=mc-amd \\
    alias=pci1022,1100 \\
    alias=pci1022,1101 \\
    alias=pci1022,1102
driver name=mm perms="allkmem 0600 root sys" perms="kmem 0640 root sys" \\
    perms="mem 0640 root sys" perms="null 0666 root sys" \\
    perms="zero 0666 root sys" \\
    policy="allkmem read_priv_set=all write_priv_set=all" \\
    policy="kmem read_priv_set=none write_priv_set=all" \\
    policy="mem read_priv_set=none write_priv_set=all"
driver name=mouse8042 alias=pnpPNP,f03
$(i386_ONLY)driver name=mpt class=scsi \\
    alias=pci1000,30 \\
    alias=pci1000,50 \\
    alias=pci1000,54 \\
    alias=pci1000,56 \\
    alias=pci1000,58 \\
    alias=pci1000,62 \\
    alias=pciex1000,56 \\
    alias=pciex1000,58 \\
    alias=pciex1000,62
driver name=nulldriver \\
    alias=scsa,nodev \\
    alias=scsa,probe
driver name=openeepr perms="openprom 0640 root sys" policy=write_priv_set=all
driver name=options
$(sparc_ONLY)driver name=pci_pci class=pci \\
    alias=pci1011,1 \\
    alias=pci1011,21 \\
    alias=pci1011,24 \\
    alias=pci1011,25 \\
    alias=pci1011,26 \\
    alias=pci1014,22 \\
    alias=pciclass,060400
$(i386_ONLY)driver name=pci_pci class=pci \\
    alias=pci1011,1 \\
    alias=pci1011,21 \\
    alias=pci1014,22 \\
    alias=pciclass,060400 \\
    alias=pciclass,060401
$(sparc_ONLY)driver name=pcieb \\
    alias=pciex108e,9010 \\
    alias=pciex108e,9020 \\
    alias=pciex10b5,8114 \\
    alias=pciex10b5,8516 \\
    alias=pciex10b5,8517 \\
    alias=pciex10b5,8518 \\
    alias=pciex10b5,8532 \\
    alias=pciex10b5,8533 \\
    alias=pciex10b5,8548 \\
    alias=pciexclass,060400
$(i386_ONLY)driver name=pcieb \\
    alias=pciexclass,060400 \\
    alias=pciexclass,060401
$(sparc_ONLY)driver name=pcieb_bcm alias=pciex1166,103
driver name=physmem perms="* 0600 root sys"
driver name=poll perms="* 0666 root sys"
$(sparc_ONLY)driver name=power alias=ali1535d+-power
$(i386_ONLY)driver name=power
driver name=pseudo alias=zconsnex
driver name=ptc perms="* 0666 root sys"
driver name=ptsl perms="* 0666 root sys"
$(sparc_ONLY)driver name=ramdisk alias=SUNW,ramdisk perms="* 0600 root sys" \\
    perms="ctl 0644 root sys"
$(i386_ONLY)driver name=ramdisk perms="* 0600 root sys" \\
    perms="ctl 0644 root sys"
driver name=random perms="* 0644 root sys" policy=write_priv_set=sys_devices
driver name=rts perms="rts 0666 root sys"
driver name=sad perms="admin 0666 root sys" perms="user 0666 root sys"
driver name=scsi_vhci class=scsi-self-identifying perms="* 0666 root sys" \\
    policy="devctl write_priv_set=sys_devices"
$(sparc_ONLY)driver name=sd perms="* 0640 root sys" \\
    alias=ide-cdrom \\
    alias=scsiclass,00 \\
    alias=scsiclass,05
$(i386_ONLY)driver name=sd perms="* 0640 root sys" \\
    alias=scsiclass,00 \\
    alias=scsiclass,05
driver name=sgen perms="* 0600 root sys" \\
    alias=scsa,08.bfcp \\
    alias=scsa,08.bvhci
driver name=simnet clone_perms="simnet 0666 root sys" perms="* 0666 root sys"
$(i386_ONLY)driver name=smbios perms="smbios 0444 root sys"
driver name=softmac
driver name=spdsock perms="spdsock 0666 root sys" \\
    policy="read_priv_set=sys_ip_config write_priv_set=sys_ip_config"
driver name=st alias=scsiclass,01 perms="* 0666 root sys"
driver name=sy perms="tty 0666 root tty"
driver name=sysevent perms="* 0600 root sys"
driver name=sysmsg perms="msglog 0600 root sys" perms="sysmsg 0600 root sys"
driver name=tcp perms="tcp 0666 root sys"
driver name=tcp6 perms="tcp6 0666 root sys"
driver name=tl perms="* 0666 root sys" clone_perms="ticlts 0666 root sys" \\
    clone_perms="ticots 0666 root sys" clone_perms="ticotsord 0666 root sys"
$(sparc_ONLY)driver name=ttymux alias=multiplexer
$(i386_ONLY)driver name=tzmon
$(sparc_ONLY)driver name=uata \\
    alias=pci1095,646 \\
    alias=pci1095,649 \\
    alias=pci1095,680 \\
    alias=pci10b9,5229 \\
    alias=pci10b9,5288 class=dada class=scsi
$(i386_ONLY)driver name=ucode perms="* 0644 root sys"
driver name=udp perms="udp 0666 root sys"
driver name=udp6 perms="udp6 0666 root sys"
$(i386_ONLY)driver name=vgatext \\
    alias=pciclass,000100 \\
    alias=pciclass,030000 \\
    alias=pciclass,030001 \\
    alias=pnpPNP,900
driver name=vnic clone_perms="vnic 0666 root sys" perms="* 0666 root sys"
driver name=wc perms="* 0600 root sys"
$(i386_ONLY)file path=boot/solaris/bin/create_diskmap group=sys mode=0555
file path=boot/solaris/bin/create_ramdisk group=sys mode=0555
file path=boot/solaris/bin/extract_boot_filelist group=sys mode=0555
$(i386_ONLY)file path=boot/solaris/bin/mbr group=sys mode=0555
$(i386_ONLY)file path=boot/solaris/bin/symdef group=sys mode=0555
$(i386_ONLY)file path=boot/solaris/bin/update_grub group=sys mode=0555
file path=boot/solaris/filelist.ramdisk group=sys
file path=boot/solaris/filelist.safe group=sys
file path=etc/crypto/kcf.conf group=sys \\
    original_name=SUNWckr:etc/crypto/kcf.conf preserve=true
file path=etc/name_to_sysnum group=sys original_name=SUNWckr:etc/name_to_sysnum \\
    preserve=renameold
file path=etc/sys= group=sys hash=tmp/sys=
file path=etc/sys=123 group=sys hash=tmp/sys=123
file path="etc/sys white space" group=sys hash='tmp/sys white space'
file path='etc/sys \" bs' group=sys hash='tmp/sys \" bs'
file path='etc/sys"' group=sys hash='tmp/sys"'
file path=etc/system group=sys original_name=SUNWckr:etc/system preserve=true
$(i386_ONLY)file path=kernel/$(ARCH64)/genunix group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/crypto/$(ARCH64)/aes group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/arcfour group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/blowfish group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/crypto/$(ARCH64)/des group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/ecc group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/md4 group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/md5 group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/rsa group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/sha1 group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/sha2 group=sys mode=0755 reboot-needed=true
file path=kernel/crypto/$(ARCH64)/swrand group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/aes group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/arcfour group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/blowfish group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/des group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/ecc group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/md4 group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/md5 group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/rsa group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/sha1 group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/sha2 group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/crypto/swrand group=sys mode=0755 \\
    reboot-needed=true
$(sparc_ONLY)file path=kernel/dacf/$(ARCH64)/consconfig_dacf group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/dacf/$(ARCH64)/net_dacf group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/dacf/net_dacf group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/acpi_drv group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/acpi_toshiba group=sys
file path=kernel/drv/$(ARCH64)/aggr group=sys
file path=kernel/drv/$(ARCH64)/arp group=sys
file path=kernel/drv/$(ARCH64)/bl group=sys
file path=kernel/drv/$(ARCH64)/bridge group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/bscbus group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/bscv group=sys
file path=kernel/drv/$(ARCH64)/clone group=sys
file path=kernel/drv/$(ARCH64)/cn group=sys
file path=kernel/drv/$(ARCH64)/conskbd group=sys
file path=kernel/drv/$(ARCH64)/consms group=sys
file path=kernel/drv/$(ARCH64)/cpuid group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/cpunex group=sys
file path=kernel/drv/$(ARCH64)/crypto group=sys
file path=kernel/drv/$(ARCH64)/cryptoadm group=sys
$(sparc_ONLY)file path=kernel/drv/$(ARCH64)/dad group=sys
file path=kernel/drv/$(ARCH64)/devinfo group=sys
file path=kernel/drv/$(ARCH64)/dld group=sys
file path=kernel/drv/$(ARCH64)/dlpistub group=sys
file path=kernel/drv/$(ARCH64)/i8042 group=sys
file path=kernel/drv/$(ARCH64)/icmp group=sys
file path=kernel/drv/$(ARCH64)/icmp6 group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/intel_nb5000 group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/intel_nhm group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/intel_nhmex group=sys
file path=kernel/drv/$(ARCH64)/ip group=sys
file path=kernel/drv/$(ARCH64)/ip6 group=sys
file path=kernel/drv/$(ARCH64)/ipnet group=sys
file path=kernel/drv/$(ARCH64)/ippctl group=sys
file path=kernel/drv/$(ARCH64)/ipsecah group=sys
file path=kernel/drv/$(ARCH64)/ipsecesp group=sys
file path=kernel/drv/$(ARCH64)/iptun group=sys
file path=kernel/drv/$(ARCH64)/iwscn group=sys
file path=kernel/drv/$(ARCH64)/kb8042 group=sys
file path=kernel/drv/$(ARCH64)/keysock group=sys
file path=kernel/drv/$(ARCH64)/kmdb group=sys
file path=kernel/drv/$(ARCH64)/kssl group=sys
file path=kernel/drv/$(ARCH64)/llc1 group=sys
file path=kernel/drv/$(ARCH64)/lofi group=sys
file path=kernel/drv/$(ARCH64)/log group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/mc-amd group=sys
file path=kernel/drv/$(ARCH64)/mm group=sys
file path=kernel/drv/$(ARCH64)/mouse8042 group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/mpt group=sys
file path=kernel/drv/$(ARCH64)/nulldriver group=sys
file path=kernel/drv/$(ARCH64)/openeepr group=sys
file path=kernel/drv/$(ARCH64)/options group=sys
file path=kernel/drv/$(ARCH64)/pci_pci group=sys
file path=kernel/drv/$(ARCH64)/pcieb group=sys
$(sparc_ONLY)file path=kernel/drv/$(ARCH64)/pcieb_bcm group=sys
file path=kernel/drv/$(ARCH64)/physmem group=sys
file path=kernel/drv/$(ARCH64)/poll group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/power group=sys
file path=kernel/drv/$(ARCH64)/pseudo group=sys
file path=kernel/drv/$(ARCH64)/ptc group=sys
file path=kernel/drv/$(ARCH64)/ptsl group=sys
file path=kernel/drv/$(ARCH64)/ramdisk group=sys
file path=kernel/drv/$(ARCH64)/random group=sys
file path=kernel/drv/$(ARCH64)/rts group=sys
file path=kernel/drv/$(ARCH64)/sad group=sys
file path=kernel/drv/$(ARCH64)/scsi_vhci group=sys
file path=kernel/drv/$(ARCH64)/sd group=sys
file path=kernel/drv/$(ARCH64)/sgen group=sys
file path=kernel/drv/$(ARCH64)/simnet group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/smbios group=sys
file path=kernel/drv/$(ARCH64)/softmac group=sys
file path=kernel/drv/$(ARCH64)/spdsock group=sys
file path=kernel/drv/$(ARCH64)/st group=sys
file path=kernel/drv/$(ARCH64)/sy group=sys
file path=kernel/drv/$(ARCH64)/sysevent group=sys
file path=kernel/drv/$(ARCH64)/sysmsg group=sys
file path=kernel/drv/$(ARCH64)/tcp group=sys
file path=kernel/drv/$(ARCH64)/tcp6 group=sys
file path=kernel/drv/$(ARCH64)/tl group=sys
$(sparc_ONLY)file path=kernel/drv/$(ARCH64)/ttymux group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/tzmon group=sys
$(sparc_ONLY)file path=kernel/drv/$(ARCH64)/uata group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/ucode group=sys
file path=kernel/drv/$(ARCH64)/udp group=sys
file path=kernel/drv/$(ARCH64)/udp6 group=sys
$(i386_ONLY)file path=kernel/drv/$(ARCH64)/vgatext group=sys
file path=kernel/drv/$(ARCH64)/vnic group=sys
file path=kernel/drv/$(ARCH64)/wc group=sys
$(i386_ONLY)file path=kernel/drv/acpi_drv group=sys
$(i386_ONLY)file path=kernel/drv/acpi_drv.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/acpi_toshiba group=sys
$(i386_ONLY)file path=kernel/drv/aggr group=sys
file path=kernel/drv/aggr.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/arp group=sys
file path=kernel/drv/arp.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/bl group=sys
file path=kernel/drv/bl.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/bridge group=sys
file path=kernel/drv/bridge.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/bscbus group=sys
$(i386_ONLY)file path=kernel/drv/bscbus.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/bscv group=sys
$(i386_ONLY)file path=kernel/drv/bscv.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/clone group=sys
file path=kernel/drv/clone.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/cn group=sys
file path=kernel/drv/cn.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/conskbd group=sys
file path=kernel/drv/conskbd.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/consms group=sys
file path=kernel/drv/consms.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/cpuid group=sys
file path=kernel/drv/cpuid.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/cpunex group=sys
$(i386_ONLY)file path=kernel/drv/crypto group=sys
file path=kernel/drv/crypto.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/cryptoadm group=sys
file path=kernel/drv/cryptoadm.conf group=sys reboot-needed=false
$(sparc_ONLY)file path=kernel/drv/dad.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/devinfo group=sys
file path=kernel/drv/devinfo.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/dld group=sys
file path=kernel/drv/dld.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/dlpistub group=sys
file path=kernel/drv/dlpistub.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/i8042 group=sys
$(i386_ONLY)file path=kernel/drv/icmp group=sys
file path=kernel/drv/icmp.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/icmp6 group=sys
file path=kernel/drv/icmp6.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/intel_nb5000 group=sys
$(i386_ONLY)file path=kernel/drv/intel_nb5000.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/intel_nhm group=sys
$(i386_ONLY)file path=kernel/drv/intel_nhm.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/intel_nhmex group=sys
$(i386_ONLY)file path=kernel/drv/intel_nhmex.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ip group=sys
file path=kernel/drv/ip.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ip6 group=sys
file path=kernel/drv/ip6.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ipnet group=sys
file path=kernel/drv/ipnet.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ippctl group=sys
file path=kernel/drv/ippctl.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ipsecah group=sys
file path=kernel/drv/ipsecah.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ipsecesp group=sys
file path=kernel/drv/ipsecesp.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/iptun group=sys
file path=kernel/drv/iptun.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/iwscn group=sys
file path=kernel/drv/iwscn.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/kb8042 group=sys
$(i386_ONLY)file path=kernel/drv/keysock group=sys
file path=kernel/drv/keysock.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/kmdb group=sys
file path=kernel/drv/kmdb.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/kssl group=sys
file path=kernel/drv/kssl.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/llc1 group=sys
file path=kernel/drv/llc1.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/lofi group=sys
file path=kernel/drv/lofi.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/log group=sys
file path=kernel/drv/log.conf group=sys \\
    original_name=SUNWckr:kernel/drv/log.conf preserve=true reboot-needed=false
$(i386_ONLY)file path=kernel/drv/mc-amd group=sys
$(i386_ONLY)file path=kernel/drv/mc-amd.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/mm group=sys
file path=kernel/drv/mm.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/mouse8042 group=sys
$(i386_ONLY)file path=kernel/drv/mpt group=sys
$(i386_ONLY)file path=kernel/drv/mpt.conf group=sys \\
    original_name=SUNWckr:kernel/drv/mpt.conf preserve=true reboot-needed=false
$(i386_ONLY)file path=kernel/drv/nulldriver group=sys
$(i386_ONLY)file path=kernel/drv/openeepr group=sys
file path=kernel/drv/openeepr.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/options group=sys
file path=kernel/drv/options.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/pci_pci group=sys
$(i386_ONLY)file path=kernel/drv/pcieb group=sys
file path=kernel/drv/pcieb.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/physmem group=sys
file path=kernel/drv/physmem.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/poll group=sys
file path=kernel/drv/poll.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/power group=sys
$(i386_ONLY)file path=kernel/drv/power.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/pseudo group=sys
file path=kernel/drv/pseudo.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ptc group=sys
file path=kernel/drv/ptc.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ptsl group=sys
file path=kernel/drv/ptsl.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ramdisk group=sys
file path=kernel/drv/ramdisk.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/random group=sys
file path=kernel/drv/random.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/rts group=sys
file path=kernel/drv/rts.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/sad group=sys
file path=kernel/drv/sad.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/scsi_vhci group=sys
file path=kernel/drv/scsi_vhci.conf group=sys \\
    original_name=SUNWckr:kernel/drv/scsi_vhci.conf preserve=true \\
    reboot-needed=false
$(sparc_ONLY)file path=kernel/drv/sd.conf group=sys \\
    original_name=SUNWckr:kernel/drv/sd.conf preserve=true reboot-needed=false
$(i386_ONLY)file path=kernel/drv/sgen group=sys
file path=kernel/drv/sgen.conf group=sys \\
    original_name=SUNWckr:kernel/drv/sgen.conf preserve=true \\
    reboot-needed=false
$(i386_ONLY)file path=kernel/drv/simnet group=sys
file path=kernel/drv/simnet.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/smbios group=sys
$(i386_ONLY)file path=kernel/drv/smbios.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/softmac group=sys
file path=kernel/drv/softmac.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/spdsock group=sys
file path=kernel/drv/spdsock.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/st group=sys
file path=kernel/drv/st.conf group=sys original_name=SUNWckr:kernel/drv/st.conf \\
    preserve=true reboot-needed=false
$(i386_ONLY)file path=kernel/drv/sy group=sys
file path=kernel/drv/sy.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/sysevent group=sys
file path=kernel/drv/sysevent.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/sysmsg group=sys
file path=kernel/drv/sysmsg.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/tcp group=sys
file path=kernel/drv/tcp.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/tcp6 group=sys
file path=kernel/drv/tcp6.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/tl group=sys
file path=kernel/drv/tl.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/tzmon group=sys
$(i386_ONLY)file path=kernel/drv/tzmon.conf group=sys reboot-needed=false
$(sparc_ONLY)file path=kernel/drv/uata.conf group=sys \\
    original_name=SUNWckr:kernel/drv/uata.conf preserve=true \\
    reboot-needed=false
$(i386_ONLY)file path=kernel/drv/ucode group=sys
$(i386_ONLY)file path=kernel/drv/ucode.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/udp group=sys
file path=kernel/drv/udp.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/udp6 group=sys
file path=kernel/drv/udp6.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/vgatext group=sys
$(i386_ONLY)file path=kernel/drv/vnic group=sys
file path=kernel/drv/vnic.conf group=sys reboot-needed=false
$(i386_ONLY)file path=kernel/drv/wc group=sys
file path=kernel/drv/wc.conf group=sys reboot-needed=false
$(sparc_ONLY)file path=kernel/exec/$(ARCH64)/aoutexec group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/exec/$(ARCH64)/elfexec group=sys mode=0755 reboot-needed=true
file path=kernel/exec/$(ARCH64)/intpexec group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/exec/elfexec group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/exec/intpexec group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/fs/$(ARCH64)/autofs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/cachefs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/ctfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/dcfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/dev group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/devfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/fifofs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/hsfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/lofs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/mntfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/namefs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/objfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/procfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/sharefs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/sockfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/specfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/tmpfs group=sys mode=0755 reboot-needed=true
file path=kernel/fs/$(ARCH64)/ufs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/autofs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/cachefs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/ctfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/dcfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/dev group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/devfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/fifofs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/hsfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/lofs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/mntfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/namefs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/objfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/procfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/sharefs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/sockfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/specfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/tmpfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/fs/ufs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/genunix group=sys mode=0755 reboot-needed=true
file path=kernel/ipp/$(ARCH64)/ipgpc group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/ipp/ipgpc group=sys mode=0755 reboot-needed=true
file path=kernel/kiconv/$(ARCH64)/kiconv_emea group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/kiconv/$(ARCH64)/kiconv_ja group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/kiconv/$(ARCH64)/kiconv_ko group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/kiconv/$(ARCH64)/kiconv_sc group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/kiconv/$(ARCH64)/kiconv_tc group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/kiconv/kiconv_emea group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/kiconv/kiconv_ja group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/kiconv/kiconv_ko group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/kiconv/kiconv_sc group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/kiconv/kiconv_tc group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/mac/$(ARCH64)/mac_6to4 group=sys mode=0755 reboot-needed=true
file path=kernel/mac/$(ARCH64)/mac_ether group=sys mode=0755 reboot-needed=true
file path=kernel/mac/$(ARCH64)/mac_ib group=sys mode=0755 reboot-needed=true
file path=kernel/mac/$(ARCH64)/mac_ipv4 group=sys mode=0755 reboot-needed=true
file path=kernel/mac/$(ARCH64)/mac_ipv6 group=sys mode=0755 reboot-needed=true
file path=kernel/mac/$(ARCH64)/mac_wifi group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/mac/mac_6to4 group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/mac/mac_ether group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/mac/mac_ib group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/mac/mac_ipv4 group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/mac/mac_ipv6 group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/mac/mac_wifi group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/acpica group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/agpmaster group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/bignum group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/bootdev group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/busra group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/cardbus group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/cmlb group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/consconfig group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/ctf group=sys mode=0755 reboot-needed=true
$(sparc_ONLY)file path=kernel/misc/$(ARCH64)/dada group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/dls group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/fssnap_if group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/gld group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/hook group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/hpcsvc group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/idmap group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/iommulib group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/ipc group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/kbtrans group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/kcf group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/kmdbmod group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/ksocket group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/mac group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/mii group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/net80211 group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/neti group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/pci_autoconfig group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/pcicfg group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/pcie group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/pcihp group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/pcmcia group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/rpcsec group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/$(ARCH64)/sata group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/scsi group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/strplumb group=sys mode=0755 reboot-needed=true
$(sparc_ONLY)file path=kernel/misc/$(ARCH64)/swapgeneric group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/$(ARCH64)/tem group=sys mode=0755 reboot-needed=true
file path=kernel/misc/$(ARCH64)/tlimod group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/acpica group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/agpmaster group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/bignum group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/bootdev group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/busra group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/cardbus group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/cmlb group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/consconfig group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/ctf group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/dls group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/fssnap_if group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/gld group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/hook group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/hpcsvc group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/idmap group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/iommulib group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/ipc group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/kbtrans group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/kcf group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/kmdbmod group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/ksocket group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/mac group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/mii group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/net80211 group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/neti group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/pci_autoconfig group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/pcicfg group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/pcie group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/pcihp group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/pcmcia group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/rpcsec group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/sata group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi group=sys mode=0755 reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_asym_emc group=sys \\
    mode=0755 reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_asym_lsi group=sys \\
    mode=0755 reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_asym_sun group=sys \\
    mode=0755 reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_sym group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_sym_emc group=sys \\
    mode=0755 reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_sym_hds group=sys \\
    mode=0755 reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_tape group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_tpgs group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/misc/scsi_vhci/$(ARCH64)/scsi_vhci_f_tpgs_tape group=sys \\
    mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_asym_emc group=sys \\
    mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_asym_lsi group=sys \\
    mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_asym_sun group=sys \\
    mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_sym group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_sym_emc group=sys \\
    mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_sym_hds group=sys \\
    mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_tape group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_tpgs group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/scsi_vhci/scsi_vhci_f_tpgs_tape group=sys \\
    mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/strplumb group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/misc/tem group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/misc/tlimod group=sys mode=0755 reboot-needed=true
file path=kernel/sched/$(ARCH64)/SDC group=sys mode=0755 reboot-needed=true
file path=kernel/sched/$(ARCH64)/TS group=sys mode=0755 reboot-needed=true
file path=kernel/sched/$(ARCH64)/TS_DPTBL group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sched/SDC group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sched/TS group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sched/TS_DPTBL group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/socketmod/$(ARCH64)/socksctp group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/socketmod/$(ARCH64)/trill group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/socketmod/socksctp group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/socketmod/trill group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/strmod/$(ARCH64)/bufmod group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/connld group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/dedump group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/drcompat group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/strmod/$(ARCH64)/ldterm group=sys mode=0755 reboot-needed=true
$(sparc_ONLY)file path=kernel/strmod/$(ARCH64)/ms group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/strmod/$(ARCH64)/pckt group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/pfmod group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/pipemod group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/ptem group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/redirmod group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/strmod/$(ARCH64)/rpcmod group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/timod group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/tirdwr group=sys mode=0755 reboot-needed=true
file path=kernel/strmod/$(ARCH64)/ttcompat group=sys mode=0755 \\
    reboot-needed=true
$(sparc_ONLY)file path=kernel/strmod/$(ARCH64)/vuid3ps2 group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/bufmod group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/connld group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/dedump group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/drcompat group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/ldterm group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/pckt group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/pfmod group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/pipemod group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/ptem group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/redirmod group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/rpcmod group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/timod group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/tirdwr group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/strmod/ttcompat group=sys mode=0755 \\
    reboot-needed=true
file path=kernel/sys/$(ARCH64)/c2audit group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/doorfs group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/inst_sync group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/kaio group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/msgsys group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/pipe group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/portfs group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/pset group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/semsys group=sys mode=0755 reboot-needed=true
file path=kernel/sys/$(ARCH64)/shmsys group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/c2audit group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/doorfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/inst_sync group=sys mode=0755 \\
    reboot-needed=true
$(i386_ONLY)file path=kernel/sys/kaio group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/msgsys group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/pipe group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/portfs group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/pset group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/semsys group=sys mode=0755 reboot-needed=true
$(i386_ONLY)file path=kernel/sys/shmsys group=sys mode=0755 reboot-needed=true
file path=lib/svc/method/svc-dumpadm mode=0555
file path=lib/svc/method/svc-intrd mode=0555
file path=lib/svc/method/svc-scheduler mode=0555
file path=lib/svc/manifest/system/dumpadm.xml group=sys mode=0444
file path=lib/svc/manifest/system/fmd.xml group=sys mode=0444
file path=lib/svc/manifest/system/intrd.xml group=sys mode=0444
file path=lib/svc/manifest/system/scheduler.xml group=sys mode=0444
hardlink path=kernel/misc/$(ARCH64)/md5 \\
    target=../../../kernel/crypto/$(ARCH64)/md5
hardlink path=kernel/misc/$(ARCH64)/sha1 \\
    target=../../../kernel/crypto/$(ARCH64)/sha1
hardlink path=kernel/misc/$(ARCH64)/sha2 \\
    target=../../../kernel/crypto/$(ARCH64)/sha2
$(i386_ONLY)hardlink path=kernel/misc/md5 target=../../kernel/crypto/md5
$(i386_ONLY)hardlink path=kernel/misc/sha1 target=../../kernel/crypto/sha1
$(i386_ONLY)hardlink path=kernel/misc/sha2 target=../../kernel/crypto/sha2
hardlink path=kernel/socketmod/$(ARCH64)/icmp \\
    target=../../../kernel/drv/$(ARCH64)/icmp
hardlink path=kernel/socketmod/$(ARCH64)/rts \\
    target=../../../kernel/drv/$(ARCH64)/rts
hardlink path=kernel/socketmod/$(ARCH64)/tcp \\
    target=../../../kernel/drv/$(ARCH64)/tcp
hardlink path=kernel/socketmod/$(ARCH64)/udp \\
    target=../../../kernel/drv/$(ARCH64)/udp
$(i386_ONLY)hardlink path=kernel/socketmod/icmp target=../../kernel/drv/icmp
$(i386_ONLY)hardlink path=kernel/socketmod/rts target=../../kernel/drv/rts
$(i386_ONLY)hardlink path=kernel/socketmod/tcp target=../../kernel/drv/tcp
$(i386_ONLY)hardlink path=kernel/socketmod/udp target=../../kernel/drv/udp
hardlink path=kernel/strmod/$(ARCH64)/arp \\
    target=../../../kernel/drv/$(ARCH64)/arp
hardlink path=kernel/strmod/$(ARCH64)/icmp \\
    target=../../../kernel/drv/$(ARCH64)/icmp
hardlink path=kernel/strmod/$(ARCH64)/ip target=../../../kernel/drv/$(ARCH64)/ip
hardlink path=kernel/strmod/$(ARCH64)/ipsecah \\
    target=../../../kernel/drv/$(ARCH64)/ipsecah
hardlink path=kernel/strmod/$(ARCH64)/ipsecesp \\
    target=../../../kernel/drv/$(ARCH64)/ipsecesp
hardlink path=kernel/strmod/$(ARCH64)/keysock \\
    target=../../../kernel/drv/$(ARCH64)/keysock
hardlink path=kernel/strmod/$(ARCH64)/tcp \\
    target=../../../kernel/drv/$(ARCH64)/tcp
hardlink path=kernel/strmod/$(ARCH64)/udp \\
    target=../../../kernel/drv/$(ARCH64)/udp
$(i386_ONLY)hardlink path=kernel/strmod/arp target=../../kernel/drv/arp
$(i386_ONLY)hardlink path=kernel/strmod/icmp target=../../kernel/drv/icmp
$(i386_ONLY)hardlink path=kernel/strmod/ip target=../../kernel/drv/ip
$(i386_ONLY)hardlink path=kernel/strmod/ipsecah target=../../kernel/drv/ipsecah
$(i386_ONLY)hardlink path=kernel/strmod/ipsecesp \\
    target=../../kernel/drv/ipsecesp
$(i386_ONLY)hardlink path=kernel/strmod/keysock target=../../kernel/drv/keysock
$(i386_ONLY)hardlink path=kernel/strmod/tcp target=../../kernel/drv/tcp
$(i386_ONLY)hardlink path=kernel/strmod/udp target=../../kernel/drv/udp
hardlink path=kernel/sys/$(ARCH64)/autofs \\
    target=../../../kernel/fs/$(ARCH64)/autofs
hardlink path=kernel/sys/$(ARCH64)/rpcmod \\
    target=../../../kernel/strmod/$(ARCH64)/rpcmod
$(i386_ONLY)hardlink path=kernel/sys/autofs target=../../kernel/fs/autofs
$(i386_ONLY)hardlink path=kernel/sys/rpcmod target=../../kernel/strmod/rpcmod
legacy pkg=SUNWckr arch=$(ARCH) category=system \\
    desc="core kernel software for a specific instruction-set architecture" \\
    hotline="Please contact your local service provider" \\
    name="Core Solaris Kernel (Root)" vendor="Sun Microsystems, Inc." \\
    version=11.11,REV=2009.11.11
license common/crypto/THIRDPARTYLICENSE.cryptogams \\
    license=common/crypto/THIRDPARTYLICENSE.cryptogams
license common/crypto/aes/amd64/THIRDPARTYLICENSE.gladman \\
    license=common/crypto/aes/amd64/THIRDPARTYLICENSE.gladman
license common/crypto/aes/amd64/THIRDPARTYLICENSE.openssl \\
    license=common/crypto/aes/amd64/THIRDPARTYLICENSE.openssl
license common/crypto/ecc/THIRDPARTYLICENSE \\
    license=common/crypto/ecc/THIRDPARTYLICENSE
license common/crypto/md5/amd64/THIRDPARTYLICENSE \\
    license=common/crypto/md5/amd64/THIRDPARTYLICENSE
license common/mpi/THIRDPARTYLICENSE license=common/mpi/THIRDPARTYLICENSE
license cr_Sun license=cr_Sun
license lic_CDDL license=lic_CDDL
license uts/common/inet/ip/THIRDPARTYLICENSE.rts \\
    license=uts/common/inet/ip/THIRDPARTYLICENSE.rts
license uts/common/inet/tcp/THIRDPARTYLICENSE \\
    license=uts/common/inet/tcp/THIRDPARTYLICENSE
license uts/common/io/THIRDPARTYLICENSE.etheraddr \\
    license=uts/common/io/THIRDPARTYLICENSE.etheraddr
license uts/common/sys/THIRDPARTYLICENSE.icu \\
    license=uts/common/sys/THIRDPARTYLICENSE.icu
license uts/common/sys/THIRDPARTYLICENSE.unicode \\
    license=uts/common/sys/THIRDPARTYLICENSE.unicode
license uts/intel/io/acpica/THIRDPARTYLICENSE \\
    license=uts/intel/io/acpica/THIRDPARTYLICENSE
$(i386_ONLY)link path=boot/solaris/bin/root_archive \\
    target=../../../usr/sbin/root_archive
link path=dev/dld target=../devices/pseudo/dld@0:ctl
link path=kernel/misc/$(ARCH64)/des target=../../../kernel/crypto/$(ARCH64)/des
$(i386_ONLY)link path=kernel/misc/des target=../../kernel/crypto/des
$(USE_INTERNAL_CRYPTO)depend fmri=driver/crypto/dprov type=require
#End Comment
"""

        needs_formatting = """\
# This comment was the first line in the file.
# The depend actions here should have their type attribute first, followed by
# fmri, other attributes, facets, and then variants.  In addition, they should
# be sorted by type and then fmri.

depend fmri=zoo fmri=apple fmri=barge type=require-any
depend fmri=baz type=require
depend fmri=zorch@2.0 type=optional
depend type=require fmri=bar
# This action should be line wrapped after each pkg.debug attribute.
depend fmri=__TBD pkg.debug.depend.file=libGL.so.1 pkg.debug.depend.path=lib pkg.debug.depend.path=usr/lib pkg.debug.depend.reason=usr/bin/xdriinfo pkg.debug.depend.type=elf type=require

# These lines through the depend action are to test for comment duplication, bug
# 18858.
$(MAN_INCLUDE)<include network-ftp.man.p5m>
# keep ping on system during upgrade from earlier releases
depend fmri=network/ping

# legacy and license actions should appear after group actions, which should
# appear before depend actions.
license a8c4507c0abeaa04fa24adda980a2558890c0249 chash=4636ad2345de0ab201674162c134796f8f1ecb72 license=cr_Oracle pkg.csize=88 pkg.size=71
legacy arch=i386 category=system desc="The Image Packaging System (IPS), or pkg(7), is the software delivery system used on OpenSolaris systems.  This package contains the core command-line components and depot server." hotline="Please contact your local service provider" name="Image Packaging System" pkg=SUNWipkg variant.arch=i386 vendor="Sun Microsystems, Inc." version=0.0.0,REV=2011.04.08.15.41.42

# This transform is the first; wrapping should be maintained although leading
# spaces should be trimmed.
<transform pkg variant.mumble=set-default -> \\
        emit set name=variant.mumble \\
        value=$(ARCH)>
# These filesystem action attributes should be re-ordered as path, owner, group,
# mode, other attributes, facet, variant.  In addition, the actions should be
# sorted by path.
link path=etc facet.devel=true target=opt/oldetc
file mode=0755 path=etc/example variant.arch=i386 \\
    group=root facet.devel=true owner=root

# These actions contain path and hash attributes with whitespace, quotes, and
# equal characters and should retain them when formatted (including hash
# attributes).
file path=etc/sys= hash=tmp/sys=
file path=etc/sys=123 hash=tmp/sys=123
file path="etc/sys white space" hash='tmp/sys white space'
file path='etc/sys \" bs' hash='tmp/sys \" bs'
file path='etc/sys"' hash='tmp/sys"'

# This action contains a hash attribute which doesn't need special handling, so
# should be transformed to the standard position.
file path=etc/foo hash=etc/foo

# This action has exactly 80 characters, so shouldn't be wrapped.
dir mode=0755 path=etc variant.arch=i386 group=root facet.devel=false owner=root
# This action has one attribute past 80 characters, so only variant should be
# wrapped after the attributes are reordered.
dir mode=0755 path=opt/etc variant.arch=i386 group=root facet.devel=false owner=root
hardlink path=etc/example facet.devel=true target=opt/etc/example
# This action has only one attribute past 80 characters, so should be unwrapped.
file \\
    path=usr/share/software/example/of/really/long/path/that/really/should/be/shorter

# This transform is the second; wrapping should be maintained.
<transform pkg variant.arch=set-default -> \\
    emit set name=variant.arch value=$(ZARCH)>

# This action should be line wrapped after each alias attribute.
driver name=intel_nb5000 alias=pci8086,25c0 alias=pci8086,25d0 alias=pci8086,25d4 alias=pci8086,25d8 alias=pci8086,3600 alias=pci8086,4000 alias=pci8086,4001 alias=pci8086,4003 alias=pci8086,65c0

# This driver action's aliases should be sorted by their alias prefix first, and
# then numerically for each component that can be parsed as hexadecimal, not
# alphabetically or asciibetically.
driver alias=usb1044,800a alias=usb13b1,20 alias=usb148f,2573 alias=usb15a9,4 alias=usb7d1,3c03 alias=usb7d1,3c04 alias=usbb05,1723 clone_perms="rum 0666 root sys" name=rum perms="* 0666 root sys" variant.arch=i386

# Ensure the correct sorting for an alias that does not fit with the main
# searching aliases meaning it falls to an alphabetical sort.
driver name=usbser_edge perms="* 0666 root sys" alias=usbif1608,1.config1.0 alias=usbif1608,1.100.config1.0 alias=usbif1608,3.config1.0 alias=usbif1608,4.config1.0 alias=usbif1608,5.config1.0 alias=usbif1608,6.config1.0

# Ensure the correct sorting for an alias that does not fit with the main
# searching aliases meaning it falls to an alphabetical sort.
driver name=usbvc perms="* 0666 root sys" alias=usbia46d,8c1.config1.0 alias=usbia46d,8c5.config1.0 alias=usbia46d,8c2.config1.0 alias=usbia,classe alias=usbia46d,8c3.config1.0

# This driver's attributes should appear in the order: name, perms, clone_perms,
# privs, policy, devlink, alias.
driver name=driver alias="bobcat" clone_perms="driver 0666 root sys" devlink=type=ddi_pseudo;name=sv\\t\\D perms="driver 0666 root sys" policy="write_priv_set=net_rawaccess" privs=sys_config

# This comment was for set name=foo; its attributes should be reordered and
# wrapped.
set name=foo value=bar variant.arch=i386 variant.arch=sparc variant.opensolaris.zone=global variant.opensolaris.zone=nonglobal

set name=pkg.summary value="No dir was harmed in the making of this summary."

# This comment was for set name=pkg.description; its value should remain quoted
# and on a single, separate line.
set name=pkg.description \\
    value='PolicyKit provides an authorization API intended to be used by privileged programs ("mechanisms") offering service to unprivileged programs ("clients") through some form of IPC mechanism such as D-Bus or Unix pipes.'

# This transform is the third; it should remain unwrapped.
<transform pkg variant.arch=set-default -> emit set name=variant.arch value=$(ARCH)>

# This comment was for pkg.fmri; it should be the first set action and the comment should
# not be unwrapped even though its first line is > 80 characters.
set name=pkg.fmri value=pkg://solaris/package/pkg@0.5.11,5.11-0.163:20110410T074945Z

# This comment was the last line of the manifest."""

        v1_fmt = """\
# This comment was the first line in the file.
# The depend actions here should have their type attribute first, followed by
# fmri, other attributes, facets, and then variants.  In addition, they should
# be sorted by type and then fmri.


# These lines through the depend action are to test for comment duplication, bug
# 18858.
$(MAN_INCLUDE)<include network-ftp.man.p5m>
# keep ping on system during upgrade from earlier releases
depend fmri=network/ping

# This transform is the first; wrapping should be maintained although leading
# spaces should be trimmed.
<transform pkg variant.mumble=set-default -> emit set name=variant.mumble value=$(ARCH)>

# This transform is the second; wrapping should be maintained.
<transform pkg variant.arch=set-default -> emit set name=variant.arch value=$(ZARCH)>

# This transform is the third; it should remain unwrapped.
<transform pkg variant.arch=set-default -> emit set name=variant.arch value=$(ARCH)>

# This comment was for pkg.fmri; it should be the first set action and the comment should
# not be unwrapped even though its first line is > 80 characters.
set name=pkg.fmri \\
    value=pkg://solaris/package/pkg@0.5.11,5.11-0.163:20110410T074945Z

# This comment was for set name=pkg.description; its value should remain quoted
# and on a single, separate line.
set name=pkg.description \\
    value='PolicyKit provides an authorization API intended to be used by privileged programs ("mechanisms") offering service to unprivileged programs ("clients") through some form of IPC mechanism such as D-Bus or Unix pipes.'
set name=pkg.summary value="No dir was harmed in the making of this summary."

# This comment was for set name=foo; its attributes should be reordered and
# wrapped.
set name=foo value=bar variant.arch=i386 variant.arch=sparc \\
    variant.opensolaris.zone=global variant.opensolaris.zone=nonglobal

# This action has exactly 80 characters, so shouldn't be wrapped.
dir path=etc group=root mode=0755 owner=root facet.devel=false \\
    variant.arch=i386
# This action has one attribute past 80 characters, so only variant should be
# wrapped after the attributes are reordered.
dir path=opt/etc group=root mode=0755 owner=root facet.devel=false \\
    variant.arch=i386

# This driver's attributes should appear in the order: name, perms, clone_perms,
# privs, policy, devlink, alias.
driver name=driver alias=bobcat clone_perms="driver 0666 root sys" \\
    devlink=type=ddi_pseudo;name=sv\\t\\D perms="driver 0666 root sys" \\
    policy=write_priv_set=net_rawaccess privs=sys_config

# This action should be line wrapped after each alias attribute.
driver name=intel_nb5000 \\
    alias=pci8086,25c0 \\
    alias=pci8086,25d0 \\
    alias=pci8086,25d4 \\
    alias=pci8086,25d8 \\
    alias=pci8086,3600 \\
    alias=pci8086,4000 \\
    alias=pci8086,4001 \\
    alias=pci8086,4003 \\
    alias=pci8086,65c0

# This driver action's aliases should be sorted by their alias prefix first, and
# then numerically for each component that can be parsed as hexadecimal, not
# alphabetically or asciibetically.
driver name=rum clone_perms="rum 0666 root sys" perms="* 0666 root sys" \\
    alias=usb1044,800a \\
    alias=usb13b1,20 \\
    alias=usb148f,2573 \\
    alias=usb15a9,4 \\
    alias=usb7d1,3c03 \\
    alias=usb7d1,3c04 \\
    alias=usbb05,1723 variant.arch=i386

# Ensure the correct sorting for an alias that does not fit with the main
# searching aliases meaning it falls to an alphabetical sort.
driver name=usbser_edge perms="* 0666 root sys" \\
    alias=usbif1608,1.100.config1.0 \\
    alias=usbif1608,1.config1.0 \\
    alias=usbif1608,3.config1.0 \\
    alias=usbif1608,4.config1.0 \\
    alias=usbif1608,5.config1.0 \\
    alias=usbif1608,6.config1.0

# Ensure the correct sorting for an alias that does not fit with the main
# searching aliases meaning it falls to an alphabetical sort.
driver name=usbvc perms="* 0666 root sys" \\
    alias=usbia,classe \\
    alias=usbia46d,8c1.config1.0 \\
    alias=usbia46d,8c2.config1.0 \\
    alias=usbia46d,8c3.config1.0 \\
    alias=usbia46d,8c5.config1.0
file path=etc/example group=root mode=0755 owner=root facet.devel=true \\
    variant.arch=i386

# This action contains a hash attribute which doesn't need special handling, so
# should be transformed to the standard position.
file etc/foo path=etc/foo
file path='etc/sys " bs' hash='tmp/sys " bs'
file path="etc/sys white space" hash="tmp/sys white space"
file path='etc/sys"' hash='tmp/sys"'

# These actions contain path and hash attributes with whitespace, quotes, and
# equal characters and should retain them when formatted (including hash
# attributes).
file path=etc/sys= hash=tmp/sys=
file path=etc/sys=123 hash=tmp/sys=123
# This action has only one attribute past 80 characters, so should be unwrapped.
file \\
    path=usr/share/software/example/of/really/long/path/that/really/should/be/shorter
hardlink path=etc/example target=opt/etc/example facet.devel=true
legacy pkg=SUNWipkg arch=i386 category=system \\
    desc="The Image Packaging System (IPS), or pkg(7), is the software delivery system used on OpenSolaris systems.  This package contains the core command-line components and depot server." \\
    hotline="Please contact your local service provider" \\
    name="Image Packaging System" vendor="Sun Microsystems, Inc." \\
    version=0.0.0,REV=2011.04.08.15.41.42 variant.arch=i386

# legacy and license actions should appear after group actions, which should
# appear before depend actions.
license a8c4507c0abeaa04fa24adda980a2558890c0249 license=cr_Oracle \\
    chash=4636ad2345de0ab201674162c134796f8f1ecb72 pkg.csize=88 pkg.size=71
# These filesystem action attributes should be re-ordered as path, owner, group,
# mode, other attributes, facet, variant.  In addition, the actions should be
# sorted by path.
link path=etc target=opt/oldetc facet.devel=true
depend type=require-any fmri=apple fmri=barge fmri=zoo
# This action should be line wrapped after each pkg.debug attribute.
depend fmri=__TBD pkg.debug.depend.file=libGL.so.1 \\
    pkg.debug.depend.reason=usr/bin/xdriinfo pkg.debug.depend.type=elf \\
    type=require pkg.debug.depend.path=lib pkg.debug.depend.path=usr/lib
depend fmri=bar type=require
depend fmri=baz type=require
depend fmri=zorch@2.0 type=optional

# This comment was the last line of the manifest.
"""

        v2_fmt = """\
# This comment was the first line in the file.
# The depend actions here should have their type attribute first, followed by
# fmri, other attributes, facets, and then variants.  In addition, they should
# be sorted by type and then fmri.


# These lines through the depend action are to test for comment duplication, bug
# 18858.
$(MAN_INCLUDE)<include network-ftp.man.p5m>
# keep ping on system during upgrade from earlier releases
depend fmri=network/ping

# This transform is the first; wrapping should be maintained although leading
# spaces should be trimmed.
<transform pkg variant.mumble=set-default -> \\
    emit set name=variant.mumble \\
    value=$(ARCH)>

# This transform is the second; wrapping should be maintained.
<transform pkg variant.arch=set-default -> \\
    emit set name=variant.arch value=$(ZARCH)>

# This transform is the third; it should remain unwrapped.
<transform pkg variant.arch=set-default -> emit set name=variant.arch value=$(ARCH)>

# This comment was for pkg.fmri; it should be the first set action and the comment should
# not be unwrapped even though its first line is > 80 characters.
set name=pkg.fmri \\
    value=pkg://solaris/package/pkg@0.5.11,5.11-0.163:20110410T074945Z
set name=pkg.summary value="No dir was harmed in the making of this summary."

# This comment was for set name=pkg.description; its value should remain quoted
# and on a single, separate line.
set name=pkg.description \\
    value='PolicyKit provides an authorization API intended to be used by privileged programs ("mechanisms") offering service to unprivileged programs ("clients") through some form of IPC mechanism such as D-Bus or Unix pipes.'

# This comment was for set name=foo; its attributes should be reordered and
# wrapped.
set name=foo value=bar variant.arch=i386 variant.arch=sparc \\
    variant.opensolaris.zone=global variant.opensolaris.zone=nonglobal

# This action has exactly 80 characters, so shouldn't be wrapped.
dir  path=etc owner=root group=root mode=0755 facet.devel=false variant.arch=i386
# These filesystem action attributes should be re-ordered as path, owner, group,
# mode, other attributes, facet, variant.  In addition, the actions should be
# sorted by path.
link path=etc target=opt/oldetc facet.devel=true
file path=etc/example owner=root group=root mode=0755 facet.devel=true \\
    variant.arch=i386
hardlink path=etc/example target=opt/etc/example facet.devel=true

# This action contains a hash attribute which doesn't need special handling, so
# should be transformed to the standard position.
file etc/foo path=etc/foo
file path='etc/sys " bs' hash='tmp/sys " bs'
file path="etc/sys white space" hash="tmp/sys white space"
file path='etc/sys"' hash='tmp/sys"'

# These actions contain path and hash attributes with whitespace, quotes, and
# equal characters and should retain them when formatted (including hash
# attributes).
file path=etc/sys= hash=tmp/sys=
file path=etc/sys=123 hash=tmp/sys=123
# This action has one attribute past 80 characters, so only variant should be
# wrapped after the attributes are reordered.
dir  path=opt/etc owner=root group=root mode=0755 facet.devel=false \\
    variant.arch=i386
# This action has only one attribute past 80 characters, so should be unwrapped.
file path=usr/share/software/example/of/really/long/path/that/really/should/be/shorter

# This driver's attributes should appear in the order: name, perms, clone_perms,
# privs, policy, devlink, alias.
driver name=driver perms="driver 0666 root sys" \\
    clone_perms="driver 0666 root sys" privs=sys_config \\
    policy=write_priv_set=net_rawaccess devlink=type=ddi_pseudo;name=sv\\t\\D \\
    alias=bobcat

# This action should be line wrapped after each alias attribute.
driver name=intel_nb5000 \\
    alias=pci8086,25c0 \\
    alias=pci8086,25d0 \\
    alias=pci8086,25d4 \\
    alias=pci8086,25d8 \\
    alias=pci8086,3600 \\
    alias=pci8086,4000 \\
    alias=pci8086,4001 \\
    alias=pci8086,4003 \\
    alias=pci8086,65c0

# This driver action's aliases should be sorted by their alias prefix first, and
# then numerically for each component that can be parsed as hexadecimal, not
# alphabetically or asciibetically.
driver name=rum perms="* 0666 root sys" clone_perms="rum 0666 root sys" \\
    alias=usb7d1,3c03 \\
    alias=usb7d1,3c04 \\
    alias=usbb05,1723 \\
    alias=usb1044,800a \\
    alias=usb13b1,20 \\
    alias=usb148f,2573 \\
    alias=usb15a9,4 variant.arch=i386

# Ensure the correct sorting for an alias that does not fit with the main
# searching aliases meaning it falls to an alphabetical sort.
driver name=usbser_edge perms="* 0666 root sys" \\
    alias=usbif1608,1.100.config1.0 \\
    alias=usbif1608,1.config1.0 \\
    alias=usbif1608,3.config1.0 \\
    alias=usbif1608,4.config1.0 \\
    alias=usbif1608,5.config1.0 \\
    alias=usbif1608,6.config1.0

# Ensure the correct sorting for an alias that does not fit with the main
# searching aliases meaning it falls to an alphabetical sort.
driver name=usbvc perms="* 0666 root sys" \\
    alias=usbia46d,8c1.config1.0 \\
    alias=usbia46d,8c2.config1.0 \\
    alias=usbia46d,8c3.config1.0 \\
    alias=usbia46d,8c5.config1.0 \\
    alias=usbia,classe
legacy pkg=SUNWipkg arch=i386 category=system \\
    desc="The Image Packaging System (IPS), or pkg(7), is the software delivery system used on OpenSolaris systems.  This package contains the core command-line components and depot server." \\
    hotline="Please contact your local service provider" \\
    name="Image Packaging System" vendor="Sun Microsystems, Inc." \\
    version=0.0.0,REV=2011.04.08.15.41.42 variant.arch=i386

# legacy and license actions should appear after group actions, which should
# appear before depend actions.
license a8c4507c0abeaa04fa24adda980a2558890c0249 license=cr_Oracle \\
    chash=4636ad2345de0ab201674162c134796f8f1ecb72 pkg.csize=88 pkg.size=71
depend type=optional fmri=zorch@2.0
# This action should be line wrapped after each pkg.debug attribute.
depend type=require fmri=__TBD pkg.debug.depend.file=libGL.so.1 \\
    pkg.debug.depend.reason=usr/bin/xdriinfo pkg.debug.depend.type=elf \\
    pkg.debug.depend.path=lib \\
    pkg.debug.depend.path=usr/lib
depend type=require fmri=bar
depend type=require fmri=baz
depend type=require-any fmri=apple fmri=barge fmri=zoo

# This comment was the last line of the manifest.
"""

        def setUp(self):
                pkg5unittest.CliTestCase.setUp(self)

                with open(os.path.join(self.test_root, "source_file"),
                    "w") as f:
                        f.write(self.pkgcontents)

                with open(os.path.join(self.test_root, "needs_fmt_file"),
                    "w") as f:
                        f.write(self.needs_formatting)

        def test_0_checkfmt(self):
                """Verify that pkgfmt -c format checking works as expected."""

                man = os.path.join(self.test_root, "man.p5m")
                original = os.path.join(self.test_root, "needs_fmt_file")
                portable.copyfile(original, man)

                # Copy man to man2 before executing tests.
                man2 = os.path.join(self.test_root, "man2.p5m")
                pkg.portable.copyfile(man, man2)

                # Verify pkgfmt exits 1 when checking format for manifest that
                # needs formatting (both from a file and from stdin).
                self.pkgfmt("-c {0}".format(man), exit=1)
                # Ensure "error:" is in output (for the benefit of ON nightly).
                self.assertTrue("pkgfmt: error:" in self.errout)
                self.pkgfmt("-c < {0}".format(man), exit=1)

                # Verify pkgfmt exits 1 when checking format for multiple
                # manifests that need formatting.
                self.pkgfmt("-c {0} {1}".format(man, man2), exit=1)

                # Verify formatted manifest is identical to expected.
                for pfmt, mfmt in (("v1", self.v1_fmt), ("v2", self.v2_fmt)):
                        portable.copyfile(original, man)
                        self.pkgfmt("-f {0} {1}".format(pfmt, man))
                        with open(man, "r") as f:
                                actual = f.read()
                                self.assertEqualDiff(mfmt, actual,
                                    msg="{0} format".format(pfmt))

                        # Test using environment variable.
                        portable.copyfile(original, man)
                        os.environ["PKGFMT_OUTPUT"] = pfmt
                        self.pkgfmt(man)
                        with open(man, "r") as f:
                                actual = f.read()
                                self.assertEqualDiff(mfmt, actual,
                                    msg="{0} format".format(pfmt))
                os.environ["PKGFMT_OUTPUT"] = ""

                # Verify pkgfmt exits 1 when any of the manifests named need
                # formatting.  (Ordering matters here, the good one must be
                # specified last.)
                self.pkgfmt("-c {0} {1}".format(man2, man), exit=1)

                # Verify pkgfmt exits 0 when a manifest doesn't need formatting.
                self.pkgfmt("-c {0}".format(man))

                # Format the second manifest.
                self.pkgfmt(man2)

                # Verify pkgfmt exits 0 when none of the manifests named need
                # formatting.
                self.pkgfmt("-c {0} {1}".format(man, man2))

                # Verify pkgfmt -c accepts a manifest in v1 or v2 format, and
                # that the output for each version matches expected.
                for contents in (self.v1_fmt, self.v2_fmt):
                        with open(man, "w") as f:
                                f.write(contents)
                        self.pkgfmt("-c {0}".format(man))

                # Verify pkgfmt -c accepts both a v1 and v2 format manifest
                # at the same time.
                with open(man, "w") as f:
                        f.write(self.v1_fmt)
                with open(man2, "w") as f:
                        f.write(self.v2_fmt)
                self.pkgfmt("-c {0} {1}".format(man, man2))

        def test_1_difference(self):
                """display that pkgfmt makes no diff in manifest"""
                source_file = os.path.join(self.test_root, "source_file")
                mod_file = os.path.join(self.test_root, "mod_file")
                # Remove comments from source file; they don't sort
                # since pkgfmt tries to maintain comment position in
                # file.
                self.cmdline_run("sed '/^#/d' < {0} > {1}; mv {2} {3}".format(
                                source_file,
                                mod_file,
                                mod_file,
                                source_file))
                # remove backslashes in place
                self.pkgfmt("-u < {0} > {1}".format(source_file, mod_file))
                # sort into alternate order and format
                self.cmdline_run("/usr/bin/sort -o {0} {1}".format(
                    mod_file, mod_file), coverage=False)
                self.pkgfmt("{0}".format(mod_file))
                self.pkgfmt("{0}".format(source_file))
                self.cmdline_run("/usr/bin/diff {0} {1}".format(
                    source_file, mod_file), coverage=False)

        def test_2_unprivileged(self):
                """Verify pkgfmt handles unprivileged user gracefully."""

                source_file = os.path.join(self.test_root, "source_file")
                # Should fail since manifest needs formatting and user can't
                # replace file.
                self.pkgfmt("{0}".format(source_file), su_wrap=True, exit=1)

                # Now reformat the file.
                self.pkgfmt("{0}".format(source_file))

                # Should not fail even though user is unprivileged.
                self.pkgfmt("-c {0}".format(source_file), su_wrap=True)

        def test_3_handle_comments(self):
                """Verify pkgfmt handles comments, does stdin"""
                source_file = os.path.join(self.test_root, "source_file")
                self.pkgfmt("< {0}".format(source_file))
                assert "Begin Comment" in self.output
                assert "Bobcat" not in self.output
                assert "Middle Comment" in self.output
                assert "End Comment" in self.output

# Vim hints
# vim:ts=8:sw=8:et:fdm=marker
