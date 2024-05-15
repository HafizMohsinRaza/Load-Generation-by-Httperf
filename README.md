# Load Generation by Httperf

This repository contains a simple setup for generating load on a web server using [Httperf](http://www.hpl.hp.com/research/web/httperf/), a tool for measuring web server performance. Httperf can generate various levels of load and can be used to test the performance and scalability of web servers, including Apache, Nginx, and others.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- A Unix-like operating system (Linux, macOS, etc.)
- Httperf installed on your system
- A web server to test (Apache, Nginx, etc.)

## Installation

To install Httperf on a Debian-based system (like Ubuntu), you can use the following command:

```bash
sudo apt-get install httperf
```

For other systems, please refer to the official Httperf documentation or your distribution's package manager.

## Usage

1. Clone this repository:

```bash
git clone https://github.com/HafizMohsinRaza/Load-Generation-by-Httperf.git
cd Load-Generation-by-Httperf
```

2. Edit the `httperf-test.sh` script to set the target server's URL and other parameters according to your needs.

3. Run the script to start the load test:

```bash
bash httperf-test.sh
```

4. Monitor the results and the server's performance.

## Customization

You can customize the load test by modifying the parameters passed to Httperf in the `httperf-test.sh` script. Some of the key parameters you might want to adjust include:

- `--server`: The IP address or hostname of the server to test.
- `--port`: The port number on which the server is running (default is 80).
- `--num-conn`: The total number of connections to make to the server.
- `--rate`: The fixed rate of requests per second.
- `--burst-length`: The length of the bursts when the `--burst-length` option is used.

For a full list of options, refer to the Httperf man page:

```bash
man httperf
```

## Example

Here's an example of how to run a basic load test with Httperf:

```bash
httperf --server=<server-ip> --port=80 --num-conn=5000 --rate=10
```

This command will create a total of 5000 connections to the server at a rate of 10 requests per second.

## Contributing

Contributions are welcome! If you have any improvements or additional features for the load test script, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Httperf tool was developed by David Mosberger and Tai Jin of Hewlett-Packard's High Performance Systems Laboratory.
- This repository is a simple wrapper around Httperf to facilitate load testing for beginners.
