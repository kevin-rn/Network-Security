# Network Security: Modular Intrusion Prevention System
This system is modular intrusion prevention system and consists of three main components separated into their own folder. 
- The 'core' which handles and parses the log files, where failed authentication is stored, of each service that is used by the system. 
- The 'server' which stores these parsed failed authentication in a database, a database observer that checks whether to ban or not and components that observe the database and then ban IP’s exceed the configured thresholds. 
- The 'webapp' which provides a web interface that gives the user control over the system such as seeing which IP's are currently banned and can be unbanned and changing threshold configurations.

# Dependencies
- SQLAlchemy is used to store (IP, Timestamp, Service) records.
- Nftables is used for banning/unbanning IP addresses.
- Vue.js is used for showing the web interface.

# Backend & Core


## Prerequisites:
- Install python3-nftables like ```sudo apt install python3-nftables```. 
Warning: Don't install nft from pip as it is unrelated to nftables.
- Download and install Python 3.8

## Getting started:
1. Create a virtual environment:  
   `python -m venv venv`
2. For enabling virtual environment on Windows:  
   `source venv/Scripts/activate.bat`
   For enabling the virtual environment on Linux:  
   `source venv/bin/activate`
3. Run ```pip install -r requirements.txt```.  



## Running the system:
1. One can now run app.py to start the server
2. For seeing the web interface follow the instructions below 'The Front-end'

## Experiments
The folder scripts contains code used for running some experiments on the system.

# The Front-end
## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
