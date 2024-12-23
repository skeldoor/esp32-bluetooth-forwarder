import requests

def push_metrics(job_name, instance, metric_name, metric_value, pushgateway_url="http://localhost:9091"):
    """
    Pushes metrics to Prometheus Pushgateway.

    Parameters:
        job_name (str): The job name (e.g., "example_job").
        instance (str): The instance label (e.g., "example_instance").
        metric_name (str): The name of the metric (e.g., "example_metric").
        metric_value (float): The value of the metric.
        pushgateway_url (str): The URL of the Pushgateway (default is "http://localhost:9091").
    """
    # Create the data in Prometheus format
    metrics_data = f"{metric_name} {metric_value}\n"

    # Construct the Pushgateway URL
    url = f"{pushgateway_url}/metrics/job/{job_name}/instance/{instance}"

    # Send data to Pushgateway
    try:
        response = requests.post(url, data=metrics_data)
        response.raise_for_status()
        print(f"Metrics pushed successfully: {metric_name}={metric_value}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to push metrics: {e}")

# Example usage
if __name__ == "__main__":
    job_name = "example_job"
    instance = "example_instance"
    metric_name = "example_metric"
    metric_value = 42.0
    push_metrics(job_name, instance, metric_name, metric_value)
