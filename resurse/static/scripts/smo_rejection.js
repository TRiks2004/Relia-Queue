async function refusalSolve() {
    const intensityInput = document.getElementById('intensityInput').value;
    const serviceTimeInput = document.getElementById('serviceTimeInput').value;
    const simulationDurationInput = document.getElementById('simulationDurationInput').value;
    const channelCountInput = document.getElementById('channelCountInput').value;
    const simulationCountInput = document.getElementById('simulationCountInput').value;
  
    const formData = {
      T: parseFloat(simulationDurationInput),
      num_channels: parseInt(channelCountInput),
      service_time: parseFloat(serviceTimeInput),
      num_iterations: parseInt(simulationCountInput),
      alfa: parseFloat(intensityInput),
    };
  
    try {
      const response = await fetch('/cfr-refusal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
  
      if (response.ok) {
        const responseData = await response.json();
        console.log('Simulation Results:', responseData);
        // Здесь вы можете обработать полученные результаты на сайте
      } else {
        console.error('Failed to run simulation', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }