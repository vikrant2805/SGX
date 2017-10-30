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

### Prerequisite

* Provide properties in the /opt/BarbiE/env.properties file

  *Required Properties are BARBICAN_ENCLAVE_PATH, IAS_URL, IAS_CRT_PATH, IAS_SPID for Barbican in different lines*
```
  Example:
         BARBICAN_ENCLAVE_PATH=/opt/BarbiE/lib
         IAS_URL=https://test-as.sgx.trustedservices.intel.com:443/attestation/sgx/v1/report
         IAS_CRT_PATH=/root/client.pem
         IAS_SPID=76508EJNCLBLB8DS19AC35I5U7XDV828
         IAS_ENABLED=True/False
```
**IAS_URL, IAS_CRT_PATH, IAS_SPID are required for quote validation other wise Attestation will Fail**
