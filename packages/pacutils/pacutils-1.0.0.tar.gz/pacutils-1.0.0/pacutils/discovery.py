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
sub-command module of discovery operation
"""

import json
from pyopae import fpga
from pacutils import common


class SubCmd(common.PACCmd):
    """
    definition of sub-command
    """
    name = 'discovery'

    def def_args(self):
        super().def_args()
        self.parser.add_argument('--vendor-id', type=common.hex_arg,
                                 metavar='HEX', default=0xffff,
                                 help='vendor ID of PCI device')
        self.parser.add_argument('--device-id', type=common.hex_arg,
                                 metavar='HEX', default=0xffff,
                                 help='device ID of PCI device')
        self.parser.add_argument('--class-id', type=common.hex_arg,
                                 metavar='HEX', default=0xffffffff,
                                 help='class ID of PCI device')
        self.parser.add_argument('--sub-vendor-id', type=common.hex_arg,
                                 metavar='HEX', default=0xffff,
                                 help='subsystem vendor ID of PCI device')
        self.parser.add_argument('--sub-device-id', type=common.hex_arg,
                                 metavar='HEX', default=0xffff,
                                 help='subsystem device ID of PCI device')
        self.parser.add_argument('--afu-id', metavar='UUID',
                                 help='AFU ID of PAC FPGA')

    @staticmethod
    def run(args):
        common.PACCmd.run(args)
        fpga_list = fpga.enumerate(vid=args.vendor_id, did=args.device_id,
                                   cid=args.class_id,
                                   sub_vid=args.sub_vendor_id,
                                   sub_did=args.sub_device_id)
        if fpga_list is None:
            fpga_list = []

        if args.afu_id is not None:
            for bdf in fpga_list[::]:
                afu_id = common.read_afu_id(bdf)
                if afu_id is None:
                    fpga_list.remove(bdf)
                    continue
                afu_id = common.bytes_to_uuid(afu_id)
                if afu_id != args.afu_id:
                    fpga_list.remove(bdf)

        print(json.dumps(fpga_list, indent=args.json_indent))
