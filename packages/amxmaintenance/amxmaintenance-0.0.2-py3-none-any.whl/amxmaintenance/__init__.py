import asyncio
from logging import critical, error, warning, info, debug


class FullScan():
    def __init__(
        self,
        telnet_output_dir='systems/amx telnet responses/',
        error_log_dir='systems/error logs/',
        camera_log_dir='systems/camera logs/',
        master_fw_dir='systems/firmware lists/',
        device_fw_dir='systems/firmware lists/',
        ):
        self.telnet_output_dir = telnet_output_dir
        self.error_log_dir = error_log_dir
        self.camera_log_dir = camera_log_dir
        self.master_fw_dir = master_fw_dir
        self.device_fw_dir = device_fw_dir
        

    def set_systems(self, systems):
        self.systems = systems
        info(f"amxmaintenance.py FullScan() added {len(self.systems)} systems")  


    def config_excel(
            self,
            source_xlsx_path='systems/campus_rooms.xlsx',
            export_xlsx=True,
            xlsx_output_path='systems/campus_complete.xlsx',
        ):
        self.source_xlsx_path = source_xlsx_path
        self.export_xlsx = export_xlsx
        self.xlsx_output_path = xlsx_output_path
 

    def config_telnet(
            self,
            telnet_user_name,
            telnet_password,
            telnet_alt_username='administrator',
            telnet_alt_password='password',
            scan_telnet=True,
            export_telnet_txt=True,
        ):
        self.telnet_user_name = telnet_user_name
        self.telnet_password = telnet_password
        self.telnet_alt_username = telnet_alt_username
        self.telnet_alt_password = telnet_alt_password
        self.scan_telnet = scan_telnet
        self.export_telnet_txt = export_telnet_txt
        

    async def _telnet_scan(self):
        from amxtelnet import AMXConnect, ParseAMXResponse
        from exceltoamx import xlsx_to_dict_list

        self.telnet_session = AMXConnect()

        self.telnet_session.config(
            user_name=self.telnet_user_name,
            password=self.telnet_password,
            alt_username=self.telnet_alt_username,
            alt_password=self.telnet_alt_password,
            write_results=self.export_telnet_txt,
            output_path=self.telnet_output_dir,
        )
        self.telnet_session.set_systems(xlsx_to_dict_list(self.source_xlsx_path))

        self.telnet_session.set_requests(
            'show device',  # do this first to get match on master_model )N...
            'get ip',
            'program info',
            'list',
            'ipdd disable',
            'boot status',  # just there as a connection delimiter
        )
        if self.scan_telnet: await self.telnet_session.run()

        self.telnet_results = await ParseAMXResponse(self.telnet_session.output_path).run()

        await self._merge_telnet()

        return self


    async def _merge_telnet(self):
        """
        Builds self.campus while destroying self.telnet_results
        """
        self.campus = []
        
        for system in self.telnet_session.systems:
            match = False
            for i, reponse in enumerate(self.telnet_results):
                if system['full_name'] == reponse['full_name']:
                    # merge dicts. telnet takes precedence
                    match = True
                    # if the tp was offline or it's a new system that hasn't seen telnet
                    if reponse['tp_model'] == 'None' and system['tp_model'] != 'None':
                        reponse['tp_model'] = system['tp_model']
                        #  we lose (G4),(G5), etc. from tp_model, but programs aren't built from this output
                        # if that becomes the plan later, (G4) or (G5) need to be reinstated as applicable.
                    self.campus.append({**system, **reponse})  # right side takes precedence
                    self.telnet_results.pop(i)  # no need to check the same one again
                    break
            # didn't find a match in the telnet communication .txt files
            if match is False: self.campus.append(system)  # keep the telnet data either way

        return self


    def config_logs(
            self,    
            check_error_log=True,
            clear_error_logs=False,
            error_log_type='error_log',
            check_camera_log=True,
            clear_camera_logs=False,
            camera_log_type='camera_log',
        ):
        self.check_error_log = check_error_log
        self.clear_error_logs = clear_error_logs
        self.error_log_type = error_log_type
        self.check_camera_log = check_camera_log
        self.clear_camera_logs = clear_camera_logs
        self.camera_log_type = camera_log_type


    async def _check_logs(self):
        from amxlogs import LogSniffer

        if self.check_error_log:
            self.error_logs = LogSniffer()
            self.error_logs.set_systems(self.campus)
            self.error_logs.config(
                log_type=self.error_log_type,
                output_dir=self.error_log_dir,
                clear_logs=self.clear_error_logs,
            )
            await self.error_logs.run()

        if self.check_camera_log:
            self.camera_logs = LogSniffer()
            self.camera_logs.set_systems(self.campus)
            self.camera_logs.config(
                log_type=self.camera_log_type,
                output_dir=self.camera_log_dir,
                clear_logs=self.clear_camera_logs,
            )
            await self.camera_logs.run()

        return self


    def config_firmware(
        self,
        ni_700_current='4.1.419',
        ni_x100_current='4.1.419',
        nx_current='1.6.179',
        ):
        self.ni_700_current = ni_700_current
        self.ni_x100_current = ni_x100_current
        self.nx_current = nx_current


    def _check_firmware(self):
        from amxfirmware import MasterFirmware, DeviceFirmware

        master_fw = MasterFirmware(self.master_fw_dir)
        master_fw.set_systems(self.campus)
        master_fw.set_versions()
        self.campus = master_fw.run()
        
        device_fw = DeviceFirmware(self.device_fw_dir)
        device_fw.set_systems(self.campus)
        device_fw.set_versions()
        self.campus = device_fw.run()

        return self


    async def run(self):

        await self._telnet_scan()

        self._check_firmware()

        await self._check_logs()

        if self.export_xlsx:
            from amxtoexcel import create_xlsx
            create_xlsx(self.campus, self.xlsx_output_path)

        info(f"amxmaintenance complete\n")

        return self.campus
