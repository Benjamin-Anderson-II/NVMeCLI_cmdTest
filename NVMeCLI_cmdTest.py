#!/bin/python3

import subprocess
import os

def get_cmd_output(cmd):
    proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, )
    output=proc.communicate()[0]
    return output


def get_cmd_status(cmd):
    cmd = cmd + " > /dev/null 2>&1"
    return os.system(cmd)


def is_cmd_available(*args):
    args=list(args)
    args.insert(0, 'sudo nvme')
    status = get_cmd_status(' '.join(args))
    if(status == 0):
        print(args[1], "Good")
        return True
    else:
        print(args[1], "Bad")
        return False


def print_availability_for_device(dev):
    print("Command Availability for", dev)
    is_cmd_available("id-ctrl", dev)
    is_cmd_available("id-ns", dev)
    is_cmd_available("id-ns-granularity", dev)
    is_cmd_available("id-ns-lba-format", dev)
    is_cmd_available("list-ns", dev)
    is_cmd_available("list-ctrl", dev)
    is_cmd_available("nvm-id-ctrl", dev)
    is_cmd_available("nvm-id-ns", dev)
    is_cmd_available("nvm-id-ns-lba-format", dev)
    is_cmd_available("primary-ctrl-caps", dev)
    is_cmd_available("list-secondary", dev)
    is_cmd_available("cmdset-ind-id-ns", dev)
    is_cmd_available("ns-descs", dev)
    is_cmd_available("id-nvmset", dev)
    is_cmd_available("id-uuid", dev)
    is_cmd_available("id-iocs", dev)
    is_cmd_available("id-domain", dev)
    is_cmd_available("list-endgrp", dev)
    create_ns = is_cmd_available("create-ns", dev, "-f 0 -i 1023")
    if(create_ns == 0):
        is_cmd_available("detach-ns", dev, "-n 1023")
        is_cmd_available("attach-ns", dev[:-2], "-n 1023") # needs a character device, so remove the "n1"
        is_cmd_available("delete-ns", dev, "-n 1023")
    is_cmd_available("get-ns-id", dev)
    is_cmd_available("get-log", dev)
    is_cmd_available("telemetry-log", dev)
    is_cmd_available("fw-log", dev)
    is_cmd_available("changed-ns-list-log", dev[:-2])
    is_cmd_available("smart-log", dev)
    is_cmd_available("ana-log", dev[:-2])
    is_cmd_available("error-log", dev)
    is_cmd_available("effects-log", dev[:-2])
    is_cmd_available("endurance-log", dev)
    is_cmd_available("predictable-lat-log", dev)
    is_cmd_available("pred-lat-event-agg-log", dev)
    is_cmd_available("persistent-event-log", dev)
    is_cmd_available("endurance-event-agg-log", dev)
    is_cmd_available("lba-status-log", dev)
    is_cmd_available("resv-notif-log", dev)
    is_cmd_available("boot-part-log", dev, "-f /dev/null")
    is_cmd_available("phy-rx-eom-log", dev)
    is_cmd_available("get-feature", dev)
    is_cmd_available("device-self-test", dev)
    is_cmd_available("self-test-log", dev)
    is_cmd_available("supported-log-pages", dev[:-2])
    is_cmd_available("fid-supported-effects-log", dev)
    is_cmd_available("mi-cmd-support-effects-log", dev)
    is_cmd_available("media-unit-stat-log", dev)
    is_cmd_available("supported-cap-config-log", dev)
    is_cmd_available("mgmt-addr-list-log", dev)
    is_cmd_available("rotational-media-info-log", dev)
    is_cmd_available("changed-alloc-ns-list-log", dev)
    is_cmd_available("dispersed-ns-participating-nss-log", dev)
    is_cmd_available("reachability-groups-log", dev)
    is_cmd_available("reachability-associations-log", dev)
    is_cmd_available("host-discovery-log", dev)
    is_cmd_available("ave-discovery-log", dev)
    is_cmd_available("pull-model-ddc-req-log", dev)
    is_cmd_available("set-feature", dev[:-2], "-f 2 -V 0x1")
    get_prop = is_cmd_available("get-property", dev, "-O 0")
    if(get_prop == 0):
        is_cmd_available("set-property", dev) # THIS WILL ALWAYS BREAK, I DON"T KNOW SAFE VALUES FOR IT
    # is_cmd_available("format", dev) # Wayyyyy too scary. Just assume you have it...
    print("format Good")
    fw_commit = is_cmd_available("fw-commit", dev[:-2], "--slot=1 --action=2")
    if(fw_commit == 0):
        print("fw-download", "Good") # Assume that if they can commit, they can download
    else:
        is_cmd_available("fw-download", dev)
    is_cmd_available("admin-passthru", dev[:-2], "-O 06 -l 4096 --cdw10=1 -r")
    is_cmd_available("io-passthru", dev, "-O 2 -n 1 -l 4096 -r --cdw10=0 --cdw11=0 --cde12=0x70000")
    # is_cmd_available("security-send", dev)
    print("security-send Good")
    # is_cmd_available("security-recv", dev)
    print("security-recv Good")
    is_cmd_available("get-lba-status", dev, "-a 10h")

    is_cmd_available("capacity-mgmt", dev)
    is_cmd_available("resv-acquire", dev)
    is_cmd_available("resv-register", dev)
    is_cmd_available("resv-release", dev)
    is_cmd_available("resv-report", dev)
    is_cmd_available("dsm", dev)
    is_cmd_available("copy", dev)
    is_cmd_available("flush", dev)
    is_cmd_available("compare", dev)
    is_cmd_available("read", dev)
    is_cmd_available("write", dev)
    is_cmd_available("write-zeroes", dev)
    is_cmd_available("write-uncor", dev)
    is_cmd_available("verify", dev)
    is_cmd_available("sanitize", dev)
    is_cmd_available("sanitize-log", dev)
    is_cmd_available("reset", dev)
    is_cmd_available("subsystem-reset", dev)
    is_cmd_available("ns-rescan", dev)
    is_cmd_available("show-regs", dev)
    is_cmd_available("set-reg", dev)
    is_cmd_available("get-reg", dev)
    is_cmd_available("discover", dev)
    is_cmd_available("connect-all", dev)
    is_cmd_available("connect", dev)
    is_cmd_available("disconnect", dev)
    is_cmd_available("disconnect-all", dev)
    is_cmd_available("config", dev)
    is_cmd_available("gen-hostnqn", dev)
    is_cmd_available("show-hostnqn", dev)
    is_cmd_available("gen-dhchap-key", dev)
    is_cmd_available("gen-tls-key", dev)
    is_cmd_available("check-tls-key", dev)
    is_cmd_available("tls-key", dev)
    is_cmd_available("dir-receive", dev)
    is_cmd_available("dir-send", dev)
    is_cmd_available("virt-mgmt", dev)
    is_cmd_available("rpmb", dev)
    is_cmd_available("lockdown", dev)
    is_cmd_available("dim", dev)
    is_cmd_available("show-topology", dev)
    is_cmd_available("io-mgmt-recv", dev)
    is_cmd_available("io-mgmt-send", dev)
    is_cmd_available("nvme-mi-recv", dev)
    is_cmd_available("nvme-mi-send", dev)
    is_cmd_available("version", dev)
    is_cmd_available("help", dev)

o = get_cmd_output('sudo nvme list | grep "/dev/" | cut -d" " -f1')
devices = o.decode('UTF-8').strip().split('\n')
if(len(devices) == 0):
    print("No NVMe Devices Found. Exitting.")
    exit(1)

print("Commands that don't require devices:")
is_cmd_available('list')
is_cmd_available('list-subsys')

for device in devices:
    print_availability_for_device(device)
