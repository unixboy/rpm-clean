#!/usr/bin/env python

# Simple script to cleanup old packages from an RPM repository. Will scan the
# current directory and ensure only the most recent version of each package
# is present in the folder (optionally keeping a number of old ones).
#
# License: WTFPL

import argparse
import os
import rpm
import rpmUtils.miscutils

def comparePackages(a, b):
	return rpmUtils.miscutils.compareEVR(a['version'], b['version'])

parser = argparse.ArgumentParser(description = 'Cleans up old files in an RPM repo')
parser.add_argument('-N', metavar = 'N', type = int, dest='n_old_versions', default = 0,
                    help = 'Number of old versions to keep in the repository for a given package (default 0)')
parser.add_argument('-n', dest = 'dry_run', default = False, action = 'store_const', const = True,
                    help = 'Don\'t actually delete files (dry run)')

args = parser.parse_args()

# Maps package names to a list of EVRs (epoch, version, release)
packages = {}

ts = rpm.TransactionSet()

# Turn off all RPM checks (we are only interested in versions)
ts.setVSFlags(-1)

print 'Reading information from the packages...'
for f in os.listdir('.'):
	if not f.endswith('.rpm'):
		continue

	hdr = rpmUtils.miscutils.hdrFromPackage(ts, f)

	name = hdr['name']

	if name not in packages:
		packages[name] = []

	packages[name].append({'filename': f, 'version': (hdr['epoch'], hdr['version'], hdr['release'])})

files_to_delete = []

for p in packages:
	# cmp is removed in Python 3 - see https://wiki.python.org/moin/HowTo/Sorting
	versions = sorted(packages[p], cmp = comparePackages, reverse = True)[args.n_old_versions + 1:]

	for v in versions:
		if args.dry_run:
			print 'would delete %s' % v['filename']
		else:
			os.remove(v['filename'])
