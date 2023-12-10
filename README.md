# Unfinished Project

This project is currently in an unfinished state. The primary goal is to make it compatible with Docker images, but the current version is designed for local machine use only.

## Usage Instructions

Follow these steps to use the project:

1. **Set Total in Makefile:**
   - Open the `Makefile` and set the value of `TOTAL` to specify the desired total goods for comparison.

2. **Configure `config.json`:**
   - Navigate to the `config` directory and edit the `config.json` file. Update the settings for main sites and the site for comparison.

3. **Install Dependencies:**
   - Install all the required packages listed in `requirements.txt` by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Script Locally:**
   - Execute the script using the following command:
     ```bash
     make run_local
     ```

5. **View Results:**
   - Check the `output` folder for the results, which will be in JSON format.

Please note that the project is a work in progress, and future updates may include Docker image compatibility.
