# NVMe-CLI Command Tester

NVMeCLI_cmdTest is a Python script that runs safe versions of all of the commadns listed on the NVMe-CLI Help page to verify which ones are available for use with your particular NVMe device. Since NVMe-CLI is a Linux-only command there will be no instructions for Windows.

## Installation

To install the script all you need to do is clone this repository. Do make sure you have both [Python](https://www.python.org/downloads/) and [`NVMe-CLI`](https://github.com/linux-nvme/nvme-cli) installed as well.

### Installing the Script
```bash
git clone https://github.com/Benjamin-Anderson-II/NVMeCLI_cmdTest/
```

### Installing Python
#### Debian-based
```bash
sudo apt get python3
```
#### Red Hat-based
```bash
sudo dnf install python3
```
#### Arch-based
```
sudo pacman -S python3
```
### Installing NVMe CLI
As made explicit in the NVMe-CLI [Readme](https://github.com/linux-nvme/nvme-cli) there is package manager support for most major distributions. Installation on the most popular of these is listed below

#### Debian-Based
```bash
sudo apt install nvme-cli
```

#### Red Hat-Based
```bash
sudo dnf install nvme-cli
```

#### Arch-Based
```bash
sudo pacman -S nvme-cli
```

## Usage

Running the script is as simple as calling the Python interpreter on the `NVMe_cmdTest.py` file.

```bash
# Navigate to the folder
cd NVMeCLI_cmdTest

# Run the Script
python3 NVMeCLI_cmdTest.py
```

## Reading the Output

The output will have at least two columns. The first of which is the name of the command being tested. To run this command yourself type `nvme <command_name> <[options]>`.

All other columns will have a device name as the header. This is the device on which the command is being run.

Certain commands will not be run on each device (`nvme list` for instance), this is because said commands are not sent to the device. Rather, these commands simply run on the system. These commands will be distinguishable from others only on multi-device systems by way of only outputting in the second column.

For each command there are currently two listed states: "Good" and "Bad." The former of these two indicates that the command is runnable on the device, given the correct parameters. The latter indicates the opposite: the command cannot be run; the device does not support its operation.

![Example Screenshot](Screenshot_20260315_130856.png)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
