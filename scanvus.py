import functions_transport_ssh
import functions_linux_inventory
import functions_vuln_detects
import functions_reports
import functions_transport_localhost
import functions_transport_docker


def get_text_block(target):
    text_block = ""
    bash_script_oneliner = functions_linux_inventory.get_bash_script_oneliner(functions_linux_inventory.bash_script)
    if target["assement_type"] == "auto_remote_ssh":
        ssh_client = functions_transport_ssh.get_ssh_client(target)
        command_result = functions_transport_ssh.execute_command(ssh_client, command=bash_script_oneliner)
        functions_transport_ssh.close_ssh_client(ssh_client)
        if command_result['errors'] != "":
            print("Error: SSH command " + command_result['errors'])
            exit()
        else:
            text_block = command_result['output']
    elif target["assement_type"] == "auto_localhost":
        text_block = functions_transport_localhost.execute_command(command=bash_script_oneliner)
    elif target["assement_type"] == "auto_docker_image":
        text_block = functions_transport_docker.execute_command(docker_name=target["docker_image"],
                                                                command=bash_script_oneliner)
    return text_block


# Examples

# target = {
#     "assement_type": "auto_remote_ssh",
#     "host": "IP",
#     "user_name": "name",
#     "key_path": "key",
# }

target = {
    "assement_type": "auto_localhost",
    "host": "localhost"
}

# target = {
#     "assement_type": "auto_docker_image",
#     "docker_image": "ubuntu:latest",
# }

text_block = get_text_block(target)
os_data = dict()
os_data["os_name"] = functions_linux_inventory.get_os_name_from_text_block(text_block)
os_data["os_version"] = functions_linux_inventory.get_os_version_from_text_block(text_block)
os_data['package_list'] = functions_linux_inventory.get_os_packages_from_text_block(text_block)
# os_data['package_list'] = ["apt 1.0.6 amd64","apt-config-icons 0.12.10-2 all"] # DEBUG
vulners_linux_audit_data = functions_vuln_detects.get_vulners_linux_audit_data(os_data)

# vulnerability_report = functions_reports.get_vulnerability_report(target, os_data, vulners_linux_audit_data)
# print(vulnerability_report['report_text'])