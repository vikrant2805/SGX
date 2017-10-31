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

### SGX Aware client without SGX Hardware


ias_enable  | server_verify_ias | client_verify_ias | Expected output |
----------- | ----------------- | ----------------- |---------------- |
True        | True              | True              | Client verify quote |
True        | True              | False             | Server verify quote |
True        | False             | True              | Client verify quote |
True        | False             | False             | Server verify quote |
False       | True              | True              | Client verify quote |
False       | True              | False             | Server not configure to do ias verification |
False       | False             | True              | Client verify quote |
False       | False             | False             | No IAS verification fake report generated  |


**ias_enabled** flag represents if configured to talk with IAS for quote verification

**server_verify_ias** flag is provided by client to let server do the quote verification with IAS

**client_verify_ias** flag is provided by client to let server know that client will verify quote with IAS



* #### Provision Master key in Barbican

```
sudo python sgx_client_wo_hw.py -ip [<IP>] -p <proj_id> [--admin] -s [<SPID>] -crt [<IAS_CRT>] [--server_verify_ias] [--client_verify_ias]
```

    IP      : IPv4 address of the server. Default :- localhost
    proj_id : Project ID
    client_verify_ias : Client will call IAS for quote verification.
    server_verify_ias : Server will call IAS for quote verification.
    SPID    : SPID provided by IAS in hexstring format. Required only when we are providing '--verify_ias'
    IAS_CRT : Absolute path of certificate for IAS server. Required only when we are providing '--verify_ias'


* #### Attestation and Secret management

```
sudo python sgx_client_wo_hw.py -ip [<IP>] -p <proj_id> -s [<SPID>] -crt [<IAS_CRT>] [--server_verify_ias] [--client_verify_ias]
```

    IP      : IPv4 address of the server. Default :- localhost
    proj_id : Project ID
    client_verify_ias : Client will call IAS for quote verification.
    server_verify_ias : Server will call IAS for quote verification.
    SPID    : SPID provided by IAS in hexstring format. Required only when we are providing '--verify_ias'
    IAS_CRT : Absolute path of certificate for IAS server. Required only when we are providing '--verify_ias'


* #### Policy Management

```
sudo python sgx_client_wo_hw.py -ip [<IP>] -p <proj_id> -po [<policy>] -mre [<mr_enclave_list_file_path>] -s [<SPID>] -crt [<IAS_CRT>] [--verify_ias]
```

    IP      : IPv4 address of the server. Default :- localhost
    proj_id : Project ID
    policy  : Project Policy to be set. Along with policy, MR Signer or path of file with list of MR Enclaves that are base64 encoded needs to be provided.
              Accepted values :-
              1 :- Mr Signer of the Client is validated.
              3 :- Mr Enclave of the Client is validated with a list of third party enclaves.
    client_verify_ias : Client will call IAS for quote verification.
    server_verify_ias : Server will call IAS for quote verification.
    SPID    : SPID provided by IAS in hexstring format. Required only when we are providing '--verify_ias'
    IAS_CRT : Absolute path of certificate for IAS server. Required only when we are providing '--verify_ias'



###  SGX Aware client with SGX Hardware

**E1** :- Enclave 1

**E2** :- Enclave 2(BarbiE)

**E1 is initiator of mutual attestation with E2**


ias_enable  | server_verify_ias | client_verify_ias | Expected output |
----------- | ----------------- | ----------------- |---------------- |
True        | True              | True              | E1 & E2 verify quote when acting as client enclave |
True        | True              | False             | E1 & E2 verify quote when acting as server enclave |
True        | False             | True              | E1 & E2 verify quote when acting as client enclave|
True        | False             | False             | E1 & E2 verify quote when acting as server enclave |
False       | True              | True              | Server not configure to do ias verification |
False       | True              | False             | Server not configure to do ias verification |
False       | False             | True              | Server not configure to do ias verification |
False       | False             | False             | E1 verify verify quote when acting as server enclave & E2 generate fake report when acting as server    |


**ias_enabled** flag represents if configured to talk with IAS for quote verification

**server_verify_ias** flag is provided by client to let server do the quote verification with IAS

**client_verify_ias** flag is provided by client to let server know that client will verify quote with IAS


* #### Policy Management

```
  sudo python sgx_client_with_hw.py -ip [<IP>] -p <proj_id> -po [<policy>] -mre [<mr_enclave_list_file_path>] -s [<SPID>] -crt [<IAS_CRT>] [--verify_ias]
```

    IP      : IPv4 address of the server. Default :- localhost
    proj_id : Project ID   
    policy  : Project Policy to be set. Mandatory during first mutual attestation. If provided in
              the subsequent call, client will be validated with existing policy and the project 
              policy will be updated. When policy '3' is provided, path of file with list of MR enclaves
              that are base64 encoded needs to be provided.
              Accepted values :-
              1 :- Mr Signer of the Client is validated.
              2 :- Mr Enclave of the Client is validated.
              3 :- Mr Enclave of the Client is validated with a list of third party enclaves.
    verify_ias : Client will call IAS or server.
    SPID    : SPID provided by IAS in hexstring format
    IAS_CRT : Absolute path of certificate for IAS server


* #### Secret Management

```
sudo python sgx_client_with_hw.py -ip [<IP>] -p <proj_id> -s [<SPID>] -crt [<IAS_CRT>] [--verify_ias]
```

    IP      : IPv4 address of the server. Default :- localhost
    proj_id : Project ID
    verify_ias : Client will call IAS or server.
    SPID    : SPID provided by IAS in hexstring format
    IAS_CRT : Absolute path of certificate for IAS server


**The above test scripts are for standalone use of barbican. If barbican is configured with Keystone, the client scripts wont work.**

