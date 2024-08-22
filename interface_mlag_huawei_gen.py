device_list = ['ALB-PH-VDI09', 'ALB-PH-VDI10', 'ALB-PH-VDI11', 'ALB-PH-VDI12', 'ALB-PH-VDI13', 'ALB-PH-VDI14', 'ALB-PH-VDI15', 'ALB-PH-VDI16', 'ALB-PH-VDI17', 'ALB-PH-VDI18', 'ALB-PH-VDI19', 'ALB-PH-VDI20', 'ALB-PH-VDI21', 'ALB-PH-VDI22', 'ALB-PH-VDI23', 'ALB-PH-VDI24', 'ALB-PH-VDI25', 'ALB-PH-VDI26', 'ALB-PH-VDI27', 'ALB-PH-VDI28', 'ALB-PH-VDI29', 'ALB-PH-VDI30', 'ALB-PH-VDI31', 'ALB-PH-VDI32', 'ALB-PH-VDI33']

config_template = '''
interface Eth-Trunk{ifnum}
 description to_MLAG_to_{devname}
 port link-type trunk
 port trunk allow-pass vlan 2129
 mode lacp-dynamic
 dfs-group 1 m-lag {ifnum}
#
interface 25GE1/0/{ifnum}
 description MLAG_to_{devname}_INT-1
 eth-trunk {ifnum}
#
'''

counter = 1

for device  in device_list:
    cfg = config_template.format(ifnum=counter,  devname=device)
    print(cfg)
    counter += 1

