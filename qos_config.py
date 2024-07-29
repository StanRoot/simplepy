import yaml
import ipaddress

with open('files/alabuga-abonents.yaml') as rate_yaml:
    abonents_rate_list = yaml.safe_load(rate_yaml)

def calculate_network_param(net):
    net_ip_v4 = ipaddress.IPv4Network(net)
    net_adress = net_ip_v4.network_address.exploded
    net_wildcard = net_ip_v4.hostmask.exploded
    return net_adress, net_wildcard

def calculate_ratelimit_param(rate_value):
    cir_value = int(rate_value) * 1024
    pir_value = int(cir_value * 1.2)
    return cir_value, pir_value, rate_value

def generate_template(**kwargs):
    config_template = '''
    traffic behavior CIR{behaviorname}Mbps
     permit
     car cir {cir} pir {pir}
    #
    acl name {abonentname}_IN
     rule 10 permit ip destination {network} {wildcard}
    acl name {abonentname}_OUT
     rule 10 permit ip source {network} {wildcard}
    #
    #
    traffic classifier {abonentname}_IN
     if-match acl {abonentname}_IN
    #
    traffic classifier {abonentname}_OUT
     if-match acl {abonentname}_OUT
    #
    #
    traffic policy RATELIMIT_FROM_RESIDENTS match-order config
     classifier {abonentname}_OUT behavior CIR{behaviorname}Mbps
    #
    traffic policy RATELIMIT_TO_RESIDENTS match-order config
     classifier {abonentname}_IN behavior CIR{behaviorname}Mbps
    '''

    kwargs.setdefault('network', '10.1.1.0')
    kwargs.setdefault('wildcard', '0.0.0.0')
    kwargs.setdefault('cir', '100')
    kwargs.setdefault('pir', '100')

    return config_template.format(**kwargs)

for abonent_dict in abonents_rate_list:
    
    nework_ipv4_address, network_ipv4_wildcard = calculate_network_param(abonent_dict['ip'])
    cir, pir, rate = calculate_ratelimit_param(abonent_dict['rate'])
    abonent_name = abonent_dict['abonent'].upper()


    config = generate_template(behaviorname=rate,
                               abonentname=abonent_name,
                               cir=cir,
                               pir=pir,
                               network=nework_ipv4_address,
                               wildcard=network_ipv4_wildcard
                               )
    print(config)