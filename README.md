# Linux Network Troubleshooting Agent
An AI-powered agent that investigates Linux network configurations using remote inspection tools and provides troubleshooting suggestions.
## Requirements
* Python 3.10+
* VirtualBox
* Three Ubuntu Server virtual machines
* SSH access to each VM
* Ollama or Google AI Studio API access
## Virtual Machine Setup
The project uses three virtual machines:
* **Bridge**: Connects two separate network segments using a Linux bridge named br0.
* **Host A**: Connected to the first network segment (Lab A).
* **Host B**: Connected to the second network segment (Lab B).
VirtualBox Configuration
1.	Create three Ubuntu Server virtual machines.
2.	Configure Host A and the Bridge VM to share the Lab A network.
3.	Configure Host B and the Bridge VM to share the Lab B network.
4.	On the Bridge VM, configure the two network adapters to allow promiscuous mode (Allow All) in VirtualBox.
## Bridge Configuration
On the Bridge VM, create a Linux bridge named br0 and attach the two network interfaces:
* **enp0s9** (Lab A)
* **enp0s10** (Lab B)
The bridge should connect both network segments, allowing Host A and Host B to communicate.
## Verify the configuration:
ip link show
bridge link
bridge fdb show
Make sure SSH is enabled on all three VMs and that the agent can connect to them.
## Installation
Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```
## Create and activate a virtual environment:
python -m venv .venv
Windows:
.venv\Scripts\activate
## Install dependencies:
pip install -r requirements.txt
## Configuration
Configure the SSH connection information for the Bridge, Host A, and Host B.
Configure your LLM provider and model using the project's configuration settings.
If using Google AI Studio, provide your API key through an environment variable. If using Ollama, make sure the Ollama service is running and the selected model is installed.
## Running the Evaluation
python <evaluation-script>.py
The evaluation script runs the evaluation dataset against the selected model and reports the results.

