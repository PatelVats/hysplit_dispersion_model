#!/bin/sh

#----------------------------------------------------------------
# Last Revised: 23 Jan 2013 - file properties set to executable
#               25 Jan 2013 - version command option for update
#               09 May 2013 - revised directory location
#               14 Oct 2016 - Mac OS correction
#               17 Mar 2020 - updated.
#----------------------------------------------------------------

echo "For non-tagged versions, this script should be run before compiling to 
      create the version message given at the beginning of a HYSPLIT run."
echo " "
echo "Enter username (guest)"
read username

if [ "$username" == "guest" ]; then
   user="--username guest --password 23864"
   echo "NOTICE: guest access is limited to exporting from tags directory."
   echo ""
else
   user="--username "$username
fi

echo "Enter command (update, export, checkout, log, version, vnumber):"
echo "  update:   executes 'svn update' command which updates working copy"
echo "  log:      executes svn log command with output directed to logfile.txt"
echo "  export:   creates a local copy which cannot be updated"
echo "  checkout: creates a working copy. Not available to guest."
echo "  version:  exports specified version from repository"
echo "  vnumber:  only updates version.inc1 and version.inc2 files"
read cmd

#----------------------------------------------
# UPDATE, LOG and VNUMBER commands
if [ "$cmd" == "update" ]; then
   svn update
elif [ "$cmd" == "log" ]; then
   #svn ${user} log -v $repo >logfile.txt
   svn log -v  >logfile.txt
   exit
elif [ "$cmd" == "vnumber" ]; then
   echo ""
else
   # REMOVE repository location option for simplicity.
   # To restore uncomment. 
   #echo "Repository location (local, server):"
   #read cmd2
   #if [ "$cmd2" == "local" ]; then
   #   tdir="file:///opt/csvn/data/repositories/hysplit/"
   #else
   #    tdir="https://svn.arl.noaa.gov:8443/svn/hysplit/"
   #fi
   tdir="https://svn.arl.noaa.gov:8443/svn/hysplit/"
   echo "Pick one: (tags, trunk, dev):"
   read cmd2
   if [ "$cmd2" == "tags" ]; then
      repo1=${tdir}'tags/'
      echo "pick tagged version (e.g. v4.2.0)"
      echo "available versions listed below:"
      svn ${user} list $repo1
      read tv
      repo=${repo1}'/hysplit.'${tv}
   elif [ "$cmd2" == "trunk" ]; then
      repo=${tdir}'trunk/'
   elif [ "$cmd2" == "dev" ]; then
      repo=${tdir}'branches/dev/'
   fi

   ROOT=`pwd`
   if [ "$cmd" == "export" ]; then
      cd ..
      svn ${user} --force export $repo
   elif [ "$cmd" == "checkout" ]; then
      cd ..
      svn ${user} checkout $repo
   elif [ "$cmd" == "version" ]; then
      cd ..
      echo "Enter version number"
      read cmd3
      svn ${user} --force export $repo -r$cmd3
      newdir=`basename $repo`
      cd ${newdir}
      pwd
   fi

fi

#----------------------------------------------
# WRITING THE version.inc files.

if [ "$cmd2" != "tags" ]; then
   echo "Updating version.inc1 and version.inc2"
   if [[ "$OSTYPE" == "darwin"* ]]; then
   svn ${user} info $repo | tail -n3 >version.txt
   else
   if [ "$cmd" == "export" ]; then
       svn ${user} info $repo | tail -n3 - >version.txt
   elif [ "$cmd" == "checkout" ]; then
       svn info | tail -n3 - >version.txt
   elif [ "$cmd" == "version" ]; then
       aaa=`date`
       echo "Exported Rev: "${cmd3} > version.txt     
       echo "Exported date: " $aaa >> version.txt     
   else
       svn info | tail -n3 - >version.txt
   fi
   fi
   rm -f version1.inc version2.inc
   cat version.txt | while read line; do
       echo "WRITE(KF21,*)'"${line}"'"  >>version1.inc
       echo    "WRITE(*,*)'"${line}"'"  >>version2.inc
   done
    #mv version1.inc trunk/source
    #mv version2.inc trunk/source
   mv version1.inc ./source
   mv version2.inc ./source
fi
