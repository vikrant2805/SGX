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

  *Required Properties are BARBICAN_ENCLAVE_PATH, IAS_URL, IAS_CRT_PATH, IAS_SPID, IAS_ENABLED for Barbican in different lines*
```
  Example:
         BARBICAN_ENCLAVE_PATH=/opt/BarbiE/lib
         IAS_URL=https://test-as.sgx.trustedservices.intel.com:443/attestation/sgx/v1/report
         IAS_CRT_PATH=/root/client.pem
         IAS_SPID=76508EJNCLBLB8DS19AC35I5U7XDV828
         IAS_ENABLED=True/False
```
**IAS_ENABLED for server to call IAS or not for quote verification.**

**IAS_URL, IAS_CRT_PATH, IAS_SPID are required for quote validation other wise Attestation will Fail.**

### Barbican start/stop/restart
```
/opt/BarbiE/startup.sh start/stop/restart
```

## Testing Barbican SGX Integration

Go under /opt/BarbiE/test_scripts/
```
sudo python sgx.py
```

## Sample Commands

###  Provision Master key in Barbican
```
sudo python sgx_client_wo_hw.py -ip [<IP>] -p <proj_id> [--admin] -s [<SPID>] -crt [<IAS_CRT>] [--server_verify_ias] [--client_verify_ias]
```
    IP      : IPv4 address of the server. Default :- localhost
    proj_id : Project ID
    client_verify_ias : Client will call IAS for quote verification.
    server_verify_ias : Server will call IAS for quote verification.
    SPID    : SPID provided by IAS in hexstring format. Required only when we are providing '--verify_ias'
    IAS_CRT : Absolute path of certificate for IAS server. Required only when we are providing '--verify_ias'
