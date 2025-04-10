from flask import Flask, render_template, request, Response
import requests
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Rendering index.html")
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        logging.info("Received simulation request")

        # Parse input
        try:
            numVMs = int(request.form.get('numVMs', 0))
            numCloudlets = int(request.form.get('numCloudlets', 0))
            numHosts = int(request.form.get('numHosts', 0))

            if numVMs <= 0 or numCloudlets <= 0 or numHosts <= 0:
                logging.warning("Invalid input: VMs, Cloudlets, and Hosts must be greater than zero")
                return "Error: Number of VMs, Cloudlets, and Hosts must be greater than zero."
        except ValueError as e:
            logging.error(f"ValueError: Invalid number input - {e}")
            return f"Error: Invalid input - {e}"

        logging.debug(f"Parsed Input - VMs: {numVMs}, Cloudlets: {numCloudlets}, Hosts: {numHosts}")

        # Host Configuration
        hosts = []
        for i in range(numHosts):
            try:
                pesMips = request.form.get(f'hosts{i}_pesMips', '').strip()
                if not pesMips:
                    logging.error(f"Missing pesMips for host {i}")
                    return f"Error: Missing pesMips for host {i}."
                
                pesMipsList = [int(x) for x in pesMips.split(',')]
                ram = int(request.form.get(f'hosts{i}_ram', 0))
                bw = int(request.form.get(f'hosts{i}_bw', 0))
                storage = int(request.form.get(f'hosts{i}_storage', 0))

                if any(x <= 0 for x in [ram, bw, storage]) or any(x <= 0 for x in pesMipsList):
                    logging.error(f"Invalid configuration for host {i}: RAM, BW, Storage, or PE MIPS is invalid.")
                    return f"Error: Invalid RAM, Bandwidth, Storage, or PE MIPS for host {i}."

                host_data = {"pesMips": pesMipsList, "ram": ram, "bw": bw, "storage": storage}
                hosts.append(host_data)
                logging.debug(f"Host {i} Configuration: {host_data}")

            except ValueError as e:
                logging.error(f"ValueError for host {i}: {e}")
                return f"Error: Invalid input for host {i}. Details: {e}"

        # VM Configuration
        try:
            vmMips = int(request.form['vmMips'])
            vmPes = int(request.form['vmPes'])
            vmRam = int(request.form['vmRam'])
            vmBw = int(request.form['vmBw'])
            vmSize = int(request.form['vmSize'])

            if any(x <= 0 for x in [vmMips, vmPes, vmRam, vmBw, vmSize]):
                logging.error("Invalid VM configuration: Values must be greater than zero.")
                return "Error: Invalid VM configuration. All values must be greater than zero."
        except (ValueError, KeyError) as e:
            logging.error(f"Invalid VM configuration: {e}")
            return f"Error: Invalid VM configuration. {e}"

        logging.debug(f"VM Configuration: MIPS={vmMips}, PEs={vmPes}, RAM={vmRam}, BW={vmBw}, Size={vmSize}")

        # Algorithm Selection
        algorithm = request.form.get('algorithm', '').strip().lower()
        if algorithm not in ['roundrobin', 'fcfs', 'sjf', 'ant', 'genetic']:
            logging.error(f"Invalid algorithm selected: {algorithm}")
            return f"Error: Invalid algorithm '{algorithm}'. Choose from roundrobin, fcfs, sjf, ant, or genetic."
        logging.info(f"Selected Algorithm: {algorithm}")

        # Cloudlet Configuration
        cloudlets = []
        for i in range(numCloudlets):
            try:
                length = int(request.form.get(f'cloudlet{i}_length', 0))
                pes = int(request.form.get(f'cloudlet{i}_pes', 0))
                fileSize = int(request.form.get(f'cloudlet{i}_fileSize', 0))
                outputSize = int(request.form.get(f'cloudlet{i}_outputSize', 0))

                if any(x <= 0 for x in [length, pes, fileSize, outputSize]):
                    logging.error(f"Invalid cloudlet configuration for cloudlet {i}.")
                    return f"Error: Invalid cloudlet configuration for cloudlet {i}."

                cloudlets.append({"length": length, "pes": pes, "fileSize": fileSize, "outputSize": outputSize})
            except ValueError as e:
                logging.error(f"Error in cloudlet {i} input: {e}")
                return f"Error: Invalid input for cloudlet {i}. {e}"

        logging.debug(f"Cloudlet Configuration: {cloudlets}")

        # Build API payload
        data = {
            "numVMs": numVMs,
            "numCloudlets": numCloudlets,
            "numHosts": numHosts,
            "hosts": hosts,
            "vmMips": vmMips,
            "vmPes": vmPes,
            "vmRam": vmRam,
            "vmBw": vmBw,
            "vmSize": vmSize,
            "algorithm": algorithm,
            "cloudlets": cloudlets
        }

        logging.info("Sending request to Spring Boot API")
        response = requests.post('http://13.234.125.14:8080/api/simulation/run', json=data)

        if response.status_code != 200:
            logging.error(f"Spring Boot API Error: {response.status_code} - {response.text}")
            return f"API Error: {response.status_code} - {response.text}"

        response_data = response.json()
        logging.info("Successfully received response from API")

        app.config['latest_result'] = response_data
        return render_template('result.html', result=response_data)

    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)
        return f"Error: {str(e)}"

@app.route('/plot.png')
def plot():
    try:
        logging.info("Generating plot")
        response_data = app.config.get('latest_result', {})
        if not response_data:
            logging.warning("No simulation data available for plotting")
            return "No simulation data available for plotting. Please run a simulation first."

        cloudlet_execution = response_data.get('cloudletExecution', {})
        if not cloudlet_execution:
            logging.warning("No cloudlet execution data available for plotting")
            return "No cloudlet execution data available for plotting."

        # Extract Cloudlet Names and Execution Times
        cloudlets = list(cloudlet_execution.keys())
        execution_times = []
        for value in cloudlet_execution.values():
            try:
                time_ms = int(''.join(filter(str.isdigit, value)))
                execution_times.append(time_ms)
            except ValueError:
                logging.error(f"Invalid execution time format: {value}")
                return f"Error: Invalid execution time format: {value}"

        # Plot Data
        plt.figure(figsize=(8, 6))
        plt.bar(cloudlets, execution_times, color='skyblue')
        plt.xlabel('Cloudlets')
        plt.ylabel('Execution Time (ms)')
        plt.title(f"Cloudlet Execution Time ({response_data.get('algorithm', '').capitalize()})")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        logging.info("Plot successfully generated")
        return Response(img.getvalue(), mimetype='image/png')

    except Exception as e:
        logging.error(f"Error generating plot: {e}", exc_info=True)
        return f"Error generating plot: {str(e)}"

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

