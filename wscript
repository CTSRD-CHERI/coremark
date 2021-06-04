#-                                                                                                                                                                                                                                                                                                                [218/1103]# SPDX-License-Identifier: BSD-2-Clause
#
# Copyright (c) 2021 Hesham Almatary
#
# This software was developed by SRI International and the University of
# Cambridge Computer Laboratory (Department of Computer Science and
# Technology) under DARPA contract HR0011-18-C-0016 ("ECATS"), as part of the
# DARPA SSITH research programme.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


def configure(ctx):
    print("Configuring CoreMark Demo @", ctx.path.abspath())

    ctx.env.append_value(
        'INCLUDES',
        [
            ctx.path.abspath() + "/",
            ctx.path.abspath() + "/freertos/",
        ])

    ctx.env.append_value('DEFINES', [
        'configPROG_ENTRY     = main',
        'ITERATIONS           = 8000',
        'POINTER_SPACE        = 16',
    ])

    ctx.env.LIBDL_PROG_START_FILE = "core_main.c"

def build(bld):
    name = "coremark"
    print("Building CoreMark Benchmarking Demo")

    cflags = ['-static', '-std=gnu99', '-ffast-math', '-fno-common']

    if bld.env.COMPARTMENTALIZE:
        cflags += ['-cheri-cap-table-abi=gprel']

    bld.stlib(
        features=['c'],
        cflags=bld.env.CFLAGS + cflags,
        defines=['FLAGS_STR="'+' '.join([str(flag) for flag in bld.env.CFLAGS + cflags])+'"'],
        source=[
            'freertos/core_portme.c',
            'core_main.c',
            'core_list_join.c',
            'core_matrix.c',
            'core_state.c',
            'core_util.c'
        ],
        use=[
            "freertos_core_headers", "freertos_bsp_headers",
        ],
        target=name)
