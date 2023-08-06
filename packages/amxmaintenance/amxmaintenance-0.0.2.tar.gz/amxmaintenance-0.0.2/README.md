# amxmaintenance
pulls together telnet info, log checking, firmware checks, etc.
run() returns the full object for inspection, but what you'll most likely end up working with is instance.campus, which is a list of AMX system dicts.


## FullScan():
#### telnet_output_dir: (default: amx telnet responses/)
#### error_log_dir: (default: error log/)
#### camera_log_dir: (default: camera log/)
#### master_fw_dir: (default: firmware lists/)
#### device_fw_dir: (default: firmware lists/)

### set_systems(systems):
#### list of dicts where each dict is an AMX system
#### minimum key requirements:
##### 'full_name' (string)
##### 'master_ip' (string)

### config_excel():
uses the amxtoexcel and exceltoamx packages
#### <b>source_xlsx_path</b>: default 'campus_rooms.xlsx'. This is the excel file that everything else depends on. Each AMX system row will be turned into a dictionary, and then they'll all be put into a list.
#### bare minimum requirements for each system:
##### 'full_name'
##### 'master_ip'
##### 'master_model' in the format NI-700, NX-2200, etc.
#### export_xlsx: default True. Do you want to export the results to an excel file?
#### xlsx_output_path: default 'campus_complete.xlsx'. If export_xlsx is true, the results are written to this location.

### config_telnet():
Uses the amxtelnet pkg. To send specific commands, use the amxtelnet pkg directly. Also checkout the amxbroadcast pkg (coming soon) if replies don't matter.

#### telnet_user_name: user name for logging into AMX masters.
#### telnet_password: password to use with telnet_user_name.
#### telnet_alt_username: default: 'administrator',
#### telnet_alt_password: default: 'password',
#### scan_telnet: default: True. 
#### export_telnet_txt: default: True.

### def config_logs():
Uses the amxlogs pkg. To check for other types of log files, use the amxlogs pkg directly.

#### check_error_log: default: True.
#### clear_error_logs: default: False.
#### error_log_type: default: 'error_log'.
#### check_camera_log: default: True.
#### clear_camera_logs: default: False.
#### camera_log_type: default: 'camera_log'.

### def config_firmware():
#### ni_700_current: default: '4.1.419'.
#### ni_x100_current: default: '4.1.419'.
#### nx_current: default: '1.6.179'.

### run():
#### Performs telnet scan of systems defined in set_systems, checks their firmware against the versions provided in config_firmware, checks for logs defined in config_logs, and exports the results to excel.
#### Returns everything to the instance for inspection, but the part you will be working with is instance.campus, which is a list of dicts, with each dict being an AMX master controller.
