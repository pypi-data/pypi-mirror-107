#!/bin/bash
. ./n.sh
mactools
VERSION=$(cat version)
increment_version $VERSION > version
VERSION=$(cat version)
configChiaProduction
deploy_pack_gz
