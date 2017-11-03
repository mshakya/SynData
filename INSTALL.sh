#!/usr/bin/env bash

set -e # Exit as soon as any line in the bash script fails

ROOTDIR=$( cd $(dirname $0) ; pwd -P ) # path to main PhaME directory

echo
exec &> >(tee -a  install.log)
exec 2>&1 # copies stderr onto stdout

# create a directory where all dependencies will be installed
cd $ROOTDIR
mkdir -p thirdParty
cd thirdParty
mkdir -p $ROOTDIR/bin
export "PATH=$PATH:$ROOTDIR/bin/"
# Minimum Required versions of dependencies
art_illumina_version=2.3.7


################################################################################
done_message () {
   if [ $? == 0 ]; then
      if [ "x$1" != "x" ]; then
          echo $1;
      else
          echo "done.";
      fi
   else
      echo "Installation failed." $2
      exit 1;
   fi
}

download_ext () {
   if [ -e $2 ]; then
      echo "$2 existed. Skiping downloading $1."
      return;
   fi;

   if hash curl 2>/dev/null; then
    if [[ -n ${HTTP_PROXY} ]]; then
          echo "Using proxy";
          echo "curl --proxy $HTTP_PROXY -L $1 -o $2";
          which curl
          curl --proxy $HTTP_PROXY -L $1  -o $2;
        else
      echo "curl -L \$1 -o \$2";
      #echo "Not using proxy";
      curl -L $1 -o $2;
    fi;
   else
      wget -O $2 $1;
   fi;

   if [ ! -r $2 ]; then
      echo "ERROR: $1 download failed."
   fi;
}

################################################################################
install_miniconda()
{
echo "--------------------------------------------------------------------------
                           downloading miniconda
--------------------------------------------------------------------------------
"

if [[ "$OSTYPE" == "darwin"* ]]
then
{

  curl -o miniconda.sh https://repo.continuum.io/miniconda/Miniconda2-4.2.12-MacOSX-x86_64.sh
  chmod +x miniconda.sh
  ./miniconda.sh -b -p $ROOTDIR/thirdParty/miniconda -f
  ln -sf $ROOTDIR/thirdParty/miniconda/bin/conda $ROOTDIR/bin/conda
  ln -sf $ROOTDIR/thirdParty/miniconda/bin/pip $ROOTDIR/bin/pip
  export PATH=$ROOTDIR/bin:$PATH
}
else
{  

  wget https://repo.continuum.io/miniconda/Miniconda2-4.2.12-Linux-x86_64.sh -O miniconda.sh
  chmod +x miniconda.sh
  ./miniconda.sh -b -p $ROOTDIR/thirdParty/miniconda -f
  ln -sf $ROOTDIR/thirdParty/miniconda/bin/conda $ROOTDIR/bin/conda
  ln -sf $ROOTDIR/thirdParty/miniconda/bin/pip $ROOTDIR/bin/pip
  export PATH=$ROOTDIR/bin:$PATH

}
fi
}

################################################################################
checkSystemInstallation()
{
    IFS=:
    for d in $PATH; do
      if test -x "$d/$1"; then return 0; fi
    done
    return 1
}


checkLocalInstallation()
{
    IFS=:
    for d in $ROOTDIR/thirdParty/miniconda/bin; do
      if test -x "$d/$1"; then return 0; fi
    done
    return 1
}

################################################################################




install_art_illumina()
{
echo "--------------------------------------------------------------------------
                           installing art_illumina
--------------------------------------------------------------------------------
"

conda install -c bioconda art 
ln -sf $ROOTDIR/thirdParty/miniconda/bin/art_illumina $ROOTDIR/bin/art_illumina
echo "--------------------------------------------------------------------------
                           installed cpanm v2.00
--------------------------------------------------------------------------------
"

}

################################################################################
if ( checkSystemInstallation conda )
then
  echo "conda is found"
  if [ -d "$ROOTDIR/thirdParty/miniconda" ]; then
    echo "conda is installed and pointed to right environment"  
  else
    echo "Creating a separate conda enviroment ..."
    conda create --yes -p $ROOTDIR/thirdParty/miniconda
  fi
else
  echo "conda was not found"
  install_miniconda
fi
################################################################################
if ( checkSystemInstallation art_illumina )
then
  art_illumina_installed_version=`art_illumina -h 2>&1 | grep 'Version' | perl -nle 'print $& if m{\d+\.\d+\.\d+}'`;
  if  ( echo $art_illumina_installed_version $art_illumina_version | awk '{if($2>=$3) exit 0; else exit 1}' )
  then 
    echo " - found ART $art_illumina_installed_version"
  else
  echo "Required version of ART was not found"
  install_art_illumina
  fi
else 
  echo "ART was not found"
  install_art_illumina
fi

echo "
================================================================================
                 syndata installed successfully.
================================================================================

Quick start:
    Read README.md for detail
Check our github site for update:
    https://github.com/LANL-Bioinformatics/PhaME
";
