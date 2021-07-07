#!/usr/bin/python3

#-
# SPDX-License-Identifier: BSD-2-Clause
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

import sys
import argparse
import os.path
from os import path
import json
import csv

# Args
parser = argparse.ArgumentParser(description='Process serial output from a CoreMark run.')
parser.add_argument("--input-logfile", help="The file path to read serial output from", default='')
parser.add_argument("--output-csv", help="The file path to write output csv data to", default='output.csv')
parser.add_argument("--output-json", help="The file path to write output json data to", default='output.json')
parser.add_argument("--freq-mhz", help="The frequency in MHz for this run", default=100)
args = parser.parse_args()

if not path.exists(args.input_logfile):
  print('Log file ', args.input_logfile, 'does not exists')
  sys.exit(-1)

hpm_counters = {
  "ITERATIONS/SECOND": 0.0,
  "CoreMark/MHz": 0.0,
  "CYCLE": 0.0,
  "INSTRET": 0.0,
  "REDIRECT": 0.0,
  "BRANCH": 0.0,
  "JAL": 0.0,
  "JALR": 0.0,
  "TRAP": 0.0,
  "LOAD_WAIT": 0.0,
  "CAP_LOAD": 0.0,
  "CAP_STORE": 0.0,
  "ITLB_MISS": 0.0,
  "ICACHE_LOAD": 0.0,
  "ICACHE_LOAD_MISS": 0.0,
  "ICACHE_LOAD_MISS_WAIT": 0.0,
  "DTLB_ACCESS": 0.0,
  "DTLB_MISS": 0.0,
  "DTLB_MISS_WAIT": 0.0,
  "DCACHE_LOAD": 0.0,
  "DCACHE_LOAD_MISS": 0.0,
  "DCACHE_LOAD_MISS_WAIT": 0.0,
  "DCACHE_STORE": 0.0,
  "DCACHE_STORE_MISS": 0.0,
  "LLCACHE_FILL": 0.0,
  "LLCACHE_LLCACHE_FILL_WAIT": 0.0,
  "TAGCACHE_LOAD": 0.0,
  "TAGCACHE_LOAD_MISS": 0.0,
  "TAGCACHE_LLCACHE_EVICT": 0.0,
  "TAGCACHE_STORE_MISS": 0.0,
  "TAGCACHE_EVICT": 0.0
}

hpm_counters["ITERATIONS/SECOND"] = [ float(line.split(':')[1]) for line in open(args.input_logfile) if 'Iterations/Sec' in line][0]
hpm_counters["CoreMark/MHz"] = hpm_counters["ITERATIONS/SECOND"] / float(args.freq_mhz)

with open(args.input_logfile) as logfile:
  for line in logfile:
    for counter in hpm_counters:
      if counter in line:
         hpm_counters[counter] = float(line.split(':')[1])

with open(args.output_csv,'w') as f:
    w = csv.writer(f)
    w.writerows(hpm_counters.items())

with open(args.output_json, 'w') as outfile:
    json.dump(hpm_counters, outfile, indent = 4)

json_object = json.dumps(hpm_counters, indent = 4)
print(json_object)
