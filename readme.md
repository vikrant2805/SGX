# Project Title

SGX aware Barbican

## Create BarbiE Installer

Go to intel-sgx/source/SGX-Barbican/

Run 
```
   ./makeself_installer.sh
```

It will create **BarbiE.bz2.run**

## BarbiE Installation

Execute "BarbiE.bz2.run" script as root user with IP address as parameter
```
    sudo ./BarbiE.bz2.run <ip_v4_address>
```
This will prompt for details during SSL certification generation.
Once done the Barbican will be started after installation is complete.
