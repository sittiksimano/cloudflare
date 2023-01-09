import os
import subprocess
import shutil
import argparse
import logging

def run_command(command):
    """Run a shell command and return the output.
    If the command fails, raise a CalledProcessError.
    """
    output = subprocess.check_output(command, shell=True)
    return output.decode('utf-8').strip()

def check_command(command):
    """Check if a command is available on the system.
    """
    return shutil.which(command) is not None

def install_package(package):
    """Install a package using apt.
    """
    run_command(f"apt install {package} -y")

def setup_cloudflare(arch, output_dir):
    """Set up Cloudflare for the specified architecture.
    """
    if arch == "aarch64" or arch == "Android":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
    elif arch == "arm64":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
    elif arch == "x86_64":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    else:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386"

    run_command(f"wget {url} -O {output_dir}/cloudflared")
    run_command(f"chmod +x {output_dir}/cloudflared")
    run_command(f"cp {output_dir}/cloudflared $PREFIX/bin/cloudflared")
    run_command("chmod +X $PREFIX/bin/cloudflared")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--arch", type=str, default="", help="target architecture (aarch64, arm64, x86_64, or 386)")
    parser.add_argument("-o", "--output", type=str, default=".", help="output directory")
    args = parser.parse_args()

    arch = args.arch
    output_dir = args.output

     logging.basicConfig(level=logging.INFO)

    # Check if required commands are available
    if not check_command("apt"):
        logging.error("apt is not available on this system.")
        return
    if not check_command("wget"):
        logging.info("wget is not available, installing it...")
        install_package("wget")
    if not check_command("php"):
        logging.info("php is not available, installing it...")
        install_package("php")
    if not check_command("proot"):
        logging.info("proot is not available, installing it...")
        install_package("proot")
    install_package("resolv-conf")

    # Remove the old Cloudflare directory if it exists
    if os.path.exists("cloudflare"):
        shutil.rmtree("cloudflare")

    # Create a new Cloudflare directory
    os.makedirs(output_dir, exist_ok=True)

    # Set up Cloudflare
    setup_cloudflare(arch, output_dir)

    logging.info("Setup done!")
    logging.info("Run 'cloudflared --help' to get started.")

if __name__ == "__main__":
    main()
