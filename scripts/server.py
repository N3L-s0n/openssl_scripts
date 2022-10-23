import socket
import yaml
import ansible_runner

class Request:
  def __init__(self, file_name, priv_passphrase, country_name, state, locality, org_name, org_unit_name, common_name, sub_alt_name_data, crl_dist_points, auth_info_access):
    self.file_name = file_name
    self.priv_passphrase = priv_passphrase
    self.country_name = country_name
    self.state = state
    self.locality = locality
    self.org_name = org_name
    self.org_unit_name = org_unit_name
    self.commom_name = common_name
    self.sub_alt_name_data = sub_alt_name_data
    self.crl_dist_points = crl_dist_points
    self.auth_info_access = auth_info_access

def server_program():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()

    file_name = conn.recv(1024).decode()
    priv_passphrase = conn.recv(1024).decode()
    org_name = conn.recv(1024).decode()
    org_unit_name = conn.recv(1024).decode()
    common_name = conn.recv(1024).decode()
    sub_alt_name_data = conn.recv(1024).decode()

    request = Request(file_name, priv_passphrase, "CR", "San Jose", "San Pedro", org_name, org_unit_name, common_name, sub_alt_name_data, "URI:http://172.16.202.22:80", "OCSP;URI:http://172.16.202.22:8080")

    csr = {
        'priv_passphrase' : getattr(request, "priv_passphrase"),
        'ca_name' : 'vpnemisora',
        'time' : '365',
        'request': {
            'name' : getattr(request, "file_name"),
            'data' : {
                'country_name' : getattr(request, "country_name"),
                'state_or_province_name' : getattr(request, "state"),
                'locality_name' : getattr(request, "locality"),
                'organization_name' : getattr(request, "org_name"),
                'organizational_unit_name' : getattr(request, "org_unit_name"),
                'common_name' : getattr(request, "commom_name"),
                'basic_constraints' : {
                    'data' : [],
                    'critical' : 'yes'
                },
                'key_usage' : {
                    'data' : ['digitalSignature'],
                    'critical' : 'no'
                },
                'subject_alt_name' : {
                    'data' : getattr(request, "sub_alt_name_data").split(","),
                    'critical' : 'yes'
                },
                'crl_distribution_points' : [{
                    'full_name' : getattr(request, "crl_dist_points").split(",")
                }]
            }
        }
    }

    r = ansible_runner.run(private_data_dir='../playbooks/', playbook='sign.yml', extravars=csr)

    print(csr)

    if (r.rc == 0 and r.status == "successful"):
        print("DONE")
    else:
        print("{}: {}".format(r.status, r.rc))

    conn.close()

if __name__ == '__main__':
    server_program()
