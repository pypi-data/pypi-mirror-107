#!/usr/bin/env bash
NVM_DIR=~/.nvm
. ~/.nvm/nvm.sh
boolean_result_false=false
boolean_result_true=true
help() {
  local usage=" Explorer builder autoscript -h\n
	 Please try select any of these cmd - testnet,dx1\n

	 example\n

	 	testnet: sh build.sh testnet\n
	 production: sh build.sh dx1\n

	 skip upload: sh build.sh testnet -test\n
	 skip upload: sh build.sh dx1  -test\n
	 	try to help it out
	 "
  echo $usage
}

configChiaProduction(){
  local file="package.json"
  local icon="versacex"
  rm -rf $TARGET_STATIC
  configStaticIconFile $icon
  configStaticSoundFile "error"
  mod_package_json ".extensions.title" "XCH Watcher v1.X" $file
  mod_package_json ".extensions.desc" "The basic console for watcher" $file
  mod_package_json ".extensions.compile" "src/pages/cover.vue" $file
  mod_package_json ".extensions.production_domain" "http://ipant1.tpddns.cn" $file
  mod_package_json ".extensions.app_icon" "/$icon.ico" $file
  mod_package_json ".extensions.port" "19451" $file
  mod_package_json ".version" $VERSION $file
}

# Accepts a version string and prints it incremented by one.
# Usage: increment_version <version> [<position>] [<leftmost>]
increment_version() {
  declare -a part=(${1//\./ })
  declare new
  declare -i carry=1

  for ((CNTR = ${#part[@]} - 1; CNTR >= 0; CNTR -= 1)); do
    len=${#part[CNTR]}
    new=$((part[CNTR] + carry))
    [ ${#new} -gt $len ] && carry=1 || carry=0
    [ $CNTR -gt 0 ] && part[CNTR]=${new: -len} || part[CNTR]=${new}
  done
  new="${part[*]}"
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${new// /.}"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "${new// /.}"
  elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "not correct system - cygwin detected"
    exit
  fi
}
abort_program() {
  cd $BUILD_DIR
  rm -f $FILE
  exit
}

#1: the full path
#2: the target location in the remote server
upload_file() {
  local file_size_kb=$(du -k "$1" | cut -f1)

  if [[ $file_size_kb -eq 0 ]]; then
    echo "⛔️ file is zero bytes..."
    abort_program
  fi

  scp $1 root@$LOCAL:$2

  if [ $? -eq 0 ]; then
    echo "✅ ==== upload successfully"
  # else
  #echo "⛔️ Error from uploading... $1"
  # abort_program
  fi

}

remotecmd() {
  local remote_cmd=$2
  ssh -t root@$LOCAL "cd $TARGET_LOC; bash; $remote_cmd"
}

directcmd() {
  ssh -t root@$LOCAL "cd $TARGET_LOC; ./build.sh"
}

mod_setting() {
  param_hk="$1 = \"$2\""
  #echo "$param_hk"
  cat $EXPLORER_SETTINGS | jq "$param_hk" -c $EXPLORER_SETTINGS | sponge $EXPLORER_SETTINGS
}
mod_package_json() {
    local NODEPFILE=$3
    param_chan=$(echo "$1 = \"$2\"")
    echo "$param_chan"
    cat $NODEPFILE | jq "$param_chan" $NODEPFILE | sponge $NODEPFILE
}
env_segment() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "mainnet"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac OSX
    echo "testlocal"
  elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "testlocal"
    # POSIX compatibility layer and Linux environment emulation for Windows
  elif [[ "$OSTYPE" == "msys" ]]; then
    # Windows
    echo "testlocal"
  elif [[ "$OSTYPE" == "freebsd"* ]]; then
    # ...
    echo "testlocal"
  fi
}

linuxtools() {
  #https://snapcraft.io/install/solc/centos
  if ! command -v rsync &>/dev/null; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    echo "rsync could not be found"
    sudo yum install rsync
  fi
}

checkssh(){
  # Script for checking if SSH port is open
  # Only checks that port is open. Not that actually SSH connection can occur
  local counter=0
  local result="ssh disabled"
  local remote=$LOCAL

  while [ $counter -lt 20 ]; do
    echo "check ssh port connection for $remote"
    telnet_output=`echo quit | telnet $remote 22 2>/dev/null | grep Connected`
    case "$telnet_output" in
      *Connected*)
        let counter=100
        result="ssh enabled"
        ;;
    esac
    let counter=counter+1
    echo "sleep for 5 seconds"
    sleep 5
  done

  echo "$result on $remote"

  if [[ "$result" =~ "enabled" ]]
  then
    exit 0
  fi
}

mactools() {
  if ! command -v rsync &>/dev/null; then
    echo "rsync could not be found"
    brew install rsync
  fi
  if ! command -v cnpm &>/dev/null; then
    echo "cnpm could not be found"
    npm i -g cnpm
  fi

  #NVM_VERSION=$(echo "$(node -v)" | grep -o -E '[0-9]{2}.')
  local NVM_VERSION=$(echo "$(node -v)" | cut -d. -f1)
  echo "==> 🈯️ all modules needed are completed."


  if [[ ${NVM_VERSION} == "v12" ]]; then
    echo "node version is on the right version : v12"
  else
    echo "please use the below command to switch to the right version of node"
    echo "nvm use 12"
    exit
  fi

}


writeremotetranslations() {
  cat <<EOF >remotetranslate
#!/bin/bash
if [[ ! -f $TARGET_LOC ]]; then
    mkdir -p $TARGET_LOC
fi

cd $TARGET_LOC
node ethcap.js
cd $TARGET_LOC && tar -czf $COMPRESSED_NAME *.json
mv $COMPRESSED_NAME $TARGET_LOC
exit
EOF
}

endline() {
  cat remotetranslate | ssh root@$LOCAL /bin/bash
  echo "==> 🈯️ download file from remote $TARGET_LOC"
  if [[ ! -f $LANGBUILDPATH ]]; then
    mkdir -p $LANGBUILDPATH
  fi
  cd $BUILDPATH
  rsync -avzhe ssh root@$LOCAL:$TARGET_LOC/$COMPRESSED_NAME $BUILDPATH
  rm remotetranslate
  mv $BUILDPATH/$COMPRESSED_NAME $LANGBUILDPATH
  cd $LANGBUILDPATH
  tar -xvf $COMPRESSED_NAME
  rm $COMPRESSED_NAME
  echo "==> 🛃 solc process completed."
}
deploy_pack_gz(){
  rm -rf dist
  rm -rf $DIST_DIR
  if [[ ! -f dist ]]; then
    mkdir -p dist
  fi
  cnpm run build
  if [[ ! -f $DIST_DIR ]]; then
    mkdir -p $DIST_DIR
  fi
  mv dist/* $DIST_DIR
  cd $DIST_DIR
  gzip -r *.* > $BUILD_FINAL/webx.tar.gz
}

translation_py(){
  # declare pytranslate="$HOME/Documents/b95/fastroundscam/controller/translate.py"
  declare localization="$PWD/src/i18n/lang"
  declare sheet=$GOOGLETRANS
  local _c=$(
    cat <<EOF

# !/usr/bin/env python
# coding: utf-8
import os

from googlesheettranslate.main import GoogleTranslationSheet

ROOT = "${localization}"

builder = GoogleTranslationSheet().builderOutputTarget(ROOT).builderMeta("${sheet}")
builder.GetReader().overrideFileFormat("_{}.json", True)
builder.run(True, "CN")
builder.run(True, "EN")
builder.run(True, "ZH")
builder.run(True, "JP")
builder.run(True, "TH")
builder.run(True, "IN")
builder.run(True, "KR")
builder.run(True, "RU")
builder.run(True, "AR")
builder.run(True, "DE")
builder.run(True, "ES")
builder.run(True, "FR")
builder.run(True, "IT")

EOF
  )
  python3 -c "$_c"
}



# how to use cp
# https://riptutorial.com/bash/topic/4030/copying--cp-
TARGET_STATIC="$BUILD_DIR/src/static"
ensureTargetFolder(){
  TARGET_STATIC="$BUILD_DIR/src/static"
  if [[ ! -f $TARGET_STATIC ]]; then
    mkdir -p $TARGET_STATIC
    chmod u+w $TARGET_STATIC
  fi
}

ensureTargetSubFolder(){
  TARGET_STATIC="$BUILD_DIR/src/static"
  local sub_folder=$1
  if [[ ! -f "$TARGET_STATIC/$sub_folder" ]]; then
    mkdir -p "$TARGET_STATIC/$sub_folder"
    chmod u+w "$TARGET_STATIC/$sub_folder"
  fi
}

configStaticIconFile(){
  local iconfolder="$BUILD_DIR/extern/icon"
  local icon_file_name=$1
  ensureTargetFolder
  cp -f "$iconfolder/$icon_file_name.ico" $TARGET_STATIC
}

configStaticSoundFile(){
  local soundfolder="$BUILD_DIR/extern/sound"
  local sound_file=$1
  ensureTargetFolder
  ensureTargetSubFolder "sound"
  #cp "$soundfolder/*.*" "$TARGET_STATIC/sound"
  cp -f "$soundfolder/$sound_file.mp3" "$TARGET_STATIC/sound"
}

GOOGLETRANS=""

BUILD_DIR=$HOME/Documents/ipfs/plotman/v1app
DIST_DIR=$HOME/Documents/ipfs/plotman/dist
BUILD_FINAL=$HOME/Documents/ipfs/plotman/build
