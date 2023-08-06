#!/usr/bin/env python3
# Copyright(c) 2020, Intel Corporation
#
# Redistribution  and  use  in source  and  binary  forms,  with  or  without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of  source code  must retain the  above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name  of Intel Corporation  nor the names of its contributors
#   may be used to  endorse or promote  products derived  from this  software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,  BUT NOT LIMITED TO,  THE
# IMPLIED WARRANTIES OF  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT  SHALL THE COPYRIGHT OWNER  OR CONTRIBUTORS BE
# LIABLE  FOR  ANY  DIRECT,  INDIRECT,  INCIDENTAL,  SPECIAL,  EXEMPLARY,  OR
# CONSEQUENTIAL  DAMAGES  (INCLUDING,  BUT  NOT LIMITED  TO,  PROCUREMENT  OF
# SUBSTITUTE GOODS OR SERVICES;  LOSS OF USE,  DATA, OR PROFITS;  OR BUSINESS
# INTERRUPTION)  HOWEVER CAUSED  AND ON ANY THEORY  OF LIABILITY,  WHETHER IN
# CONTRACT,  STRICT LIABILITY,  OR TORT  (INCLUDING NEGLIGENCE  OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,  EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
sub-command module of information operation
"""

import json
from pyopae import fpga
from pacutils import common


class SubCmd(common.PACCmd):
    """
    definition of sub-command
    """
    name = 'information'

    def def_args(self):
        super().def_args()
        self.parser.add_argument('--flex', action='store_true', default=False,
                                 help='PCI information of FPGA in PAC')
        self.parser.add_argument('--fix', action='store_true', default=False,
                                 help='PCI information of non-FPGA in PAC')
        self.parser.add_argument('--phy', action='store_true', default=False,
                                 help='PHY information in PAC')

    @staticmethod
    def flex_info(pf0_bdf):
        """
        get PCI information of PAC FPGA
        """
        info = {}
        fpga_bdfs = [pf0_bdf]
        pf1_bdfs = fpga.get_pf1(pf0_bdf)
        if pf1_bdfs is not None:
            fpga_bdfs.extend(pf1_bdfs)
        for bdf in fpga_bdfs:
            prop = fpga.get_property(bdf, common.PAC_PROP_PCI)
            info[bdf] = prop
        return info

    @staticmethod
    def fix_info(bdfs):
        """
        get PCI information of PAC ASIC
        """
        info = {}
        if bdfs is not None and len(bdfs) == 4:
            for dev in [bdfs[0], bdfs[2]]:
                child = fpga.get_child(dev)
                if child is not None:
                    for bdf in child:
                        prop = fpga.get_property(bdf, common.PAC_PROP_PCI)
                        info[bdf] = prop
        return info

    @staticmethod
    def phy_info(pf0_bdf, eal_param):
        """
        get PHY information in PAC
        """
        common.probe_pac(pf0_bdf, eal_param)
        info = fpga.get_phy_info(pf0_bdf)
        fpga.cleanup_eal()
        return info

    @staticmethod
    def run(args):
        common.PACCmd.run(args)
        common.check_pac(args.bdf)

        pac_bdfs = {}
        dsp = fpga.get_parent(args.bdf)
        usp = fpga.get_parent(dsp)
        dsps = fpga.get_child(usp)
        if dsps is not None and len(dsps) == 4:
            pac_dev = {}
            for bdf in dsps:
                child = fpga.get_child(bdf)
                if child is None:
                    pac_dev[bdf] = []
                else:
                    pac_dev[bdf] = child
            pac_bdfs[usp] = pac_dev

        pac_info = {}
        if args.flex:
            pac_info.update(SubCmd.flex_info(args.bdf))

        if args.fix:
            pac_info.update(SubCmd.fix_info(dsps))

        if args.phy:
            pac_info.update(SubCmd.phy_info(args.bdf, args.eal_parameter))

        if args.flex or args.fix or args.phy:
            print(json.dumps(pac_info, indent=args.json_indent))
        else:
            print(json.dumps(pac_bdfs, indent=args.json_indent))
