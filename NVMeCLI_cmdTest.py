#!/bin/python3

import subprocess
import os


def get_cmd_output(cmd):
    proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, )
    output=proc.communicate()[0]
    return output






o = get_cmd_output('sudo nvme list | grep "/dev/" | cut -d" " -f1')
namespaces = o.decode('UTF-8').strip().split('\n')
if(len(namespaces) == 0):
    print("No NVMe Devices Found. Exitting.")
    exit(1)
characters = [ns[:-2] for ns in namespaces]

cmds = [ # {cmd, [devs], [opts]}
    ["list", None, None],
    ["list-subsys", None, None],
    [ "id-ctrl", namespaces, None],
    [ "id-ns", namespaces, None],
    [ "id-ns-granularity", namespaces, None],
    [ "id-ns-lba-format", namespaces, None],
    [ "list-ns", namespaces, None],
    [ "list-ctrl", namespaces, None],
    [ "nvm-id-ctrl", namespaces, None],
    [ "nvm-id-ns", namespaces, None],
    [ "nvm-id-ns-lba-format", namespaces, None],
    [ "primary-ctrl-caps", namespaces, None],
    [ "cmdset-ind-id-ns", namespaces, None],
    [ "ns-descs", namespaces, None],
    [ "id-nvmset", namespaces, None],
    [ "id-uuid", namespaces, None],
    [ "id-iocs", namespaces, None],
    [ "id-domain", namespaces, None],
    [ "list-endgrp", namespaces, None],
    [ "create-ns", namespaces, "-f 0 --nvmset-id=1023"],
    [ "detach-ns", characters, "--namespace-id=1023"],
    [ "attach-ns", namespaces, "--namespace-id=1023"],
    [ "delete-ns", namespaces, None],
    [ "get-ns-id", namespaces, None],
    [ "get-log", characters, "--log-id=2 --log-len=512"],
    [ "telemetry-log", namespaces, None],
    [ "fw-log", namespaces, None],
    [ "changed-ns-list-log", characters, None],
    [ "smart-log", namespaces, None],
    [ "ana-log", namespaces, None],
    [ "error-log", namespaces, None],
    [ "effects-log", namespaces, None],
    [ "endurance-log", namespaces, None],
    [ "predictable-lat-log", namespaces, None],
    [ "red-lat-event-agg-log", namespaces, None],
    [ "persistent-event-log", namespaces, None],
    [ "endurance-event-agg-log", namespaces, None],
    [ "lba-status-log", namespaces, None],
    [ "resv-notif-log", namespaces, None],
    [ "boot-part-log", namespaces, "-f /dev/null"],
    [ "phy-rx-eom-log", namespaces, None],
    [ "get-feature", namespaces, None],
    [ "device-self-test", namespaces, None],
    [ "self-test-log", namespaces, None],
    [ "supported-log-pages", characters, None],
    [ "fid-supported-effects-log", namespaces, None],
    [ "mi-cmd-support-effects-log", namespaces, None],
    [ "media-unit-stat-log", namespaces, None],
    [ "supported-cap-config-log", namespaces, None],
    [ "mgmt-addr-list-log", namespaces, None],
    [ "rotational-media-info-log", namespaces, None],
    [ "changed-alloc-ns-list-log", namespaces, None],
    [ "dispersed-ns-participating-nss-log", namespaces, None],
    [ "reachability-groups-log", namespaces, None],
    [ "reachability-associations-log", namespaces, None],
    [ "host-discovery-log", namespaces, None],
    [ "ave-discovery-log", namespaces, None],
    [ "pull-model-ddc-req-log", namespaces, None],
    [ "set-feature", characters, "-f 2 -V 0x1"],
    [ "get-property", namespaces, "-O 0"],
    [ "set-property", namespaces, None],
    [ "format", None, None], #force this to break, you don't want format to run
    [ "fw-commit", characters, "--slot=1 --action=2"],
    [ "fw-download", namespaces, None],
    [ "admin-passthru", characters, "-O 06 -l 4096 --cdw=1 -r"],
    [ "io-passthru", namespaces, "--opcode=2 --namespace-id=1 --data-len=4096 --read --cdw10=0 --cdw11=0 --cdw12=0x70000 --raw-binary"],
    [ "security-send", None, None], #Force this to break; no reason to mess with security settings
    [ "security-recv", None, None], 
    [ "get-lba-status", namespaces, "-a 10h"],
    [ "capacity-mgmt", None, None],
    [ "resv-aquire", None, None],
    [ "resv-register", None, None],
    [ "resv-release", None, None],
    [ "resv-report", None, None],
    [ "dsm", None, None],
    [ "copy", None, None],
    [ "flush", None, None],
    [ "compare", None, None],
    [ "read", None, None],
    [ "write", None, None],
    [ "write-zeroes", None, None],
    [ "write-uncor", None, None],
    [ "verify", None, None],
    [ "sanitize", None, None],
    [ "sanitize-log", None, None],
    [ "reset", None, None],
    [ "subsystem-reset", None, None],
    [ "ns-rescan", None, None],
    [ "show-regs", None, None],
    [ "set-reg", None, None],
    [ "get-reg", None, None],
    [ "discover", None, None],
    [ "connect-all", None, None],
    [ "connect", None, None],
    [ "disconnect", None, None],
    [ "disconnect-all", None, None],
    [ "config", None, None],
    [ "gen-hostnqn", None, None],
    [ "show-hostnqn", None, None],
    [ "gen-dhchap-key", None, None],
    [ "check-dhchap-key", None, None],
    [ "gen-tls-key", None, None],
    [ "check-tls-key", None, None],
    [ "tls-key", None, None],
    [ "dir-receive", None, None],
    [ "dir-send", None, None],
    [ "virt-mgmt", None, None],
    [ "rpmb", None, None],
    [ "lockdown", None, None],
    [ "dim", None, None],
    [ "show-topology", None, None],
    [ "io-mgmt-recv", None, None],
    [ "io-mgmt-send", None, None],
    [ "nvme-mi-recv", None, None],
    [ "nvme-mi-send", None, None],
    [ "version", None, None],
    [ "help", None, None]
]

longest_cmd_name=0
line_len=0


for c in cmds:
    if(len(c[0]) > longest_cmd_name):
        longest_cmd_name = len(c[0])

line_len+=longest_cmd_name+4
for n in namespaces:
    line_len+=len(n)+3

def get_header():
    header=""
    for i in range(line_len):
        header+='-'
    header+='\n| Commands'
    for i in range(longest_cmd_name-len("Commands")):
        header+=' '
    header+=" |"
    for n in namespaces:
        header+=' '+n+' |'
    header+='\n'
    for i in range(line_len):
        header+='-'
    return header


def status_message(result, ns_id):
    ret = " " + result
    for i in range(len(namespaces[ns_id])+1-len(result)):
        ret += ' '
    ret += "\033[0m|"
    return ret

def make_commands(cmd):
    ret = []
    if(not cmd[1]):
        c = f"sudo nvme {cmd[0]} "
        if(cmd[2]):
            c += cmd[2]
        c += " > /dev/null 2>&1"
        ret.append(c)
        return ret

    for device in cmd[1]:
        c = f"sudo nvme {cmd[0]} {device} "
        if(cmd[2]):
            c += cmd[2]
        c += " > /dev/null 2>&1"
        ret.append(c)

    return ret


def check_commands(arr):
    i = 0
    for a in arr:
        status = os.system(a)
        if(status==0):
            print("\033[42m", end='')
            print(status_message("Good ", i), end='')
            print("\033[0m", end='')
        else:
            print(status_message("Bad", i), end='')
        i+=1

    print()


def print_command_availability():
    # Heading
    print(get_header())

    for c in cmds:
        print("|", c[0], end='')
        for i in range(longest_cmd_name-len(c[0])):
            print(" ", end='')
        print(" |", end='')

        check_commands(make_commands(c))

    # Bottom Line
    for i in range(line_len):
        print('-', end='')
    print()


print_command_availability()





#def get_cmd_status(cmd):
#    cmd = cmd + " > /dev/null 2>&1"
#    return os.system(cmd)

##def is_cmd_available(cmd, devs, opts):
    

#def is_cmd_available(*args):
#    args=list(args)
#    args.insert(0, 'sudo nvme')
#    status = get_cmd_status(' '.join(args))
#    if(status == 0):
#        print(args[1], "\033[42mGood\033[0m")
#        return True
#    else:
#        print(args[1], "Bad")
#        return False


#def print_availability_for_device(dev):
#    print("--------------Command Availability for", dev, "----------------")
#    print("--------------------------------------")
#    is_cmd_available("id-ctrl", dev)
#    is_cmd_available("id-ns", dev)
#    is_cmd_available("id-ns-granularity", dev)
#    is_cmd_available("id-ns-lba-format", dev)
#    is_cmd_available("list-ns", dev)
#    is_cmd_available("list-ctrl", dev)
#    is_cmd_available("nvm-id-ctrl", dev)
#    is_cmd_available("nvm-id-ns", dev)
#    is_cmd_available("nvm-id-ns-lba-format", dev)
#    is_cmd_available("primary-ctrl-caps", dev)
#    is_cmd_available("list-secondary", dev)
#    is_cmd_available("cmdset-ind-id-ns", dev)
#    is_cmd_available("ns-descs", dev)
#    is_cmd_available("id-nvmset", dev)
#    is_cmd_available("id-uuid", dev)
#    is_cmd_available("id-iocs", dev)
#    is_cmd_available("id-domain", dev)
#    is_cmd_available("list-endgrp", dev)
#    create_ns = is_cmd_available("create-ns", dev, "-f 0 -i 1023")
#    if(create_ns == 0):
#        is_cmd_available("detach-ns", dev, "-n 1023")
#        is_cmd_available("attach-ns", dev[:-2], "-n 1023") # needs a character device, so remove the "n1"
#        is_cmd_available("delete-ns", dev, "-n 1023")
#    is_cmd_available("get-ns-id", dev)
#    is_cmd_available("get-log", dev)
#    is_cmd_available("telemetry-log", dev)
#    is_cmd_available("fw-log", dev)
#    is_cmd_available("changed-ns-list-log", dev[:-2])
#    is_cmd_available("smart-log", dev)
#    is_cmd_available("ana-log", dev[:-2])
#    is_cmd_available("error-log", dev)
#    is_cmd_available("effects-log", dev[:-2])
#    is_cmd_available("endurance-log", dev)
#    is_cmd_available("predictable-lat-log", dev)
#    is_cmd_available("pred-lat-event-agg-log", dev)
#    is_cmd_available("persistent-event-log", dev)
#    is_cmd_available("endurance-event-agg-log", dev)
#    is_cmd_available("lba-status-log", dev)
#    is_cmd_available("resv-notif-log", dev)
#    is_cmd_available("boot-part-log", dev, "-f /dev/null")
#    is_cmd_available("phy-rx-eom-log", dev)
#    is_cmd_available("get-feature", dev)
#    is_cmd_available("device-self-test", dev)
#    is_cmd_available("self-test-log", dev)
#    is_cmd_available("supported-log-pages", dev[:-2])
#    is_cmd_available("fid-supported-effects-log", dev)
#    is_cmd_available("mi-cmd-support-effects-log", dev)
#    is_cmd_available("media-unit-stat-log", dev)
#    is_cmd_available("supported-cap-config-log", dev)
#    is_cmd_available("mgmt-addr-list-log", dev)
#    is_cmd_available("rotational-media-info-log", dev)
#    is_cmd_available("changed-alloc-ns-list-log", dev)
#    is_cmd_available("dispersed-ns-participating-nss-log", dev)
#    is_cmd_available("reachability-groups-log", dev)
#    is_cmd_available("reachability-associations-log", dev)
#    is_cmd_available("host-discovery-log", dev)
#    is_cmd_available("ave-discovery-log", dev)
#    is_cmd_available("pull-model-ddc-req-log", dev)
#    is_cmd_available("set-feature", dev[:-2], "-f 2 -V 0x1")
#    get_prop = is_cmd_available("get-property", dev, "-O 0")
#    if(get_prop == 0):
#        is_cmd_available("set-property", dev) # THIS WILL ALWAYS BREAK, I DON"T KNOW SAFE VALUES FOR IT
#    # is_cmd_available("format", dev) # Wayyyyy too scary. Just assume you have it...
#    print("format \033[42mGood\033[0m")
#    fw_commit = is_cmd_available("fw-commit", dev[:-2], "--slot=1 --action=2")
#    if(fw_commit == 0):
#        print("fw-download", "Good") # Assume that if they can commit, they can download
#    else:
#        is_cmd_available("fw-download", dev)
#    is_cmd_available("admin-passthru", dev[:-2], "-O 06 -l 4096 --cdw10=1 -r")
#    is_cmd_available("io-passthru", dev, "--opcode=2 --namespace-id=1 --data-len=4096 --read --cdw10=0 --cdw11=0 --cdw12=0x70000 --raw-binary")
#    # is_cmd_available("security-send", dev)
#    print("security-send \033[42mGood\033[0m")
#    # is_cmd_available("security-recv", dev)
#    print("security-recv \033[42mGood\033[0m")
#    is_cmd_available("get-lba-status", dev, "-a 10h")

#    # is_cmd_available("capacity-mgmt", dev)
#    # is_cmd_available("resv-acquire", dev)
#    # is_cmd_available("resv-register", dev)
#    # is_cmd_available("resv-release", dev)
#    # is_cmd_available("resv-report", dev)
#    # is_cmd_available("dsm", dev)
#    # is_cmd_available("copy", dev)
#    # is_cmd_available("flush", dev)
#    # is_cmd_available("compare", dev)
#    # is_cmd_available("read", dev)
#    # is_cmd_available("write", dev)
#    # is_cmd_available("write-zeroes", dev)
#    # is_cmd_available("write-uncor", dev)
#    # is_cmd_available("verify", dev)
#    # is_cmd_available("sanitize", dev)
#    # is_cmd_available("sanitize-log", dev)
#    # is_cmd_available("reset", dev)
#    # is_cmd_available("subsystem-reset", dev)
#    # is_cmd_available("ns-rescan", dev)
#    # is_cmd_available("show-regs", dev)
#    # is_cmd_available("set-reg", dev)
#    # is_cmd_available("get-reg", dev)
#    # is_cmd_available("discover", dev)
#    # is_cmd_available("connect-all", dev)
#    # is_cmd_available("connect", dev)
#    # is_cmd_available("disconnect", dev)
#    # is_cmd_available("disconnect-all", dev)
#    # is_cmd_available("config", dev)
#    # is_cmd_available("gen-hostnqn", dev)
#    # is_cmd_available("show-hostnqn", dev)
#    # is_cmd_available("gen-dhchap-key", dev)
#    # is_cmd_available("gen-tls-key", dev)
#    # is_cmd_available("check-tls-key", dev)
#    # is_cmd_available("tls-key", dev)
#    # is_cmd_available("dir-receive", dev)
#    # is_cmd_available("dir-send", dev)
#    # is_cmd_available("virt-mgmt", dev)
#    # is_cmd_available("rpmb", dev)
#    # is_cmd_available("lockdown", dev)
#    # is_cmd_available("dim", dev)
#    # is_cmd_available("show-topology", dev)
#    # is_cmd_available("io-mgmt-recv", dev)
#    # is_cmd_available("io-mgmt-send", dev)
#    # is_cmd_available("nvme-mi-recv", dev)
#    # is_cmd_available("nvme-mi-send", dev)
#    # is_cmd_available("version", dev)
#    # is_cmd_available("help", dev)

#o = get_cmd_output('sudo nvme list | grep "/dev/" | cut -d" " -f1')
#devices = o.decode('UTF-8').strip().split('\n')
#if(len(devices) == 0):
#    print("No NVMe Devices Found. Exitting.")
#    exit(1)

#print("Commands that don't require devices:")
#is_cmd_available('list')
#is_cmd_available('list-subsys')

#for device in devices:
#    print_availability_for_device(device)
