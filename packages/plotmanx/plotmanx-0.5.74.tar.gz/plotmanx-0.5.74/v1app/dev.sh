#!/bin/bash
. ./n.sh
mactools
VERSION=$(cat version)
increment_version $VERSION > version
VERSION=$(cat version)
configChiaProduction
#translation_py
cnpm run dev
