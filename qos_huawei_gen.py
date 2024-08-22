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
    pir_value = int(cir_value * 1)
    return cir_value, pir_value, rate_value

def generate_template(**kwargs):
    config_template = '''
    traffic behavior CIR{behaviorname}M
     permit
     car cir {cir} pir {pir}
    #
    acl name TO_{abonentname} advance
     rule 10 permit ip destination {network} {wildcard}
    acl name FROM_{abonentname} advance
     rule 10 permit ip source {network} {wildcard}
    #
    #
    traffic classifier TO_{abonentname}
     if-match acl TO_{abonentname}
    #
    traffic classifier FROM_{abonentname}
     if-match acl FROM_{abonentname}
    #
    #
    traffic policy RATELIMIT_TO_RESIDENTS match-order config
     classifier TO_{abonentname} behavior CIR{behaviorname}M
    #
    traffic policy RATELIMIT_FROM_RESIDENTS match-order config
     classifier FROM_{abonentname} behavior CIR{behaviorname}M
    '''

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