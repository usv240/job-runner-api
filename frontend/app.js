const apiBase = 'http://localhost:8000';

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById('jobForm');
  const input = document.getElementById('commandInput');
  const jobList = document.getElementById('jobsList');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const command = input.value.trim();
    if (!command) return;

    try {
      await fetch(`${apiBase}/jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
      });
      input.value = '';
      loadJobs();
    } catch (err) {
      console.error('Failed to submit job:', err);
    }
  });

  async function cancelJob(jobId) {
    try {
      await fetch(`${apiBase}/jobs/${jobId}/cancel`, { method: 'POST' });
      loadJobs();
    } catch (err) {
      console.error(`Failed to cancel job ${jobId}:`, err);
    }
  }

  async function getJobStatus(jobId) {
    try {
      const res = await fetch(`${apiBase}/jobs/${jobId}`);
      return await res.json();
    } catch (err) {
      console.error(`Failed to get job status for ${jobId}:`, err);
      return {};
    }
  }

  async function loadJobs() {
    jobList.innerHTML = '';

    try {
      const res = await fetch(`${apiBase}/jobs`);
      const jobs = await res.json();

      for (const job of jobs) {
        const jobItem = document.createElement('li');
        jobItem.className = 'job-item';
        jobItem.style.borderLeft = `4px solid ${getStatusColor(job.status)}`;

        const jobIdSpan = document.createElement('span');
        jobIdSpan.className = 'job-id';
        jobIdSpan.textContent = job.job_id;

        const statusSpan = document.createElement('span');
        statusSpan.className = 'job-status';
        statusSpan.textContent = ` - ${job.status}`;

        const jobDetails = document.createElement('div');
        jobDetails.appendChild(jobIdSpan);
        jobDetails.appendChild(statusSpan);

        jobItem.appendChild(jobDetails);

        // Fetch latest details (like output)
        const latest = await getJobStatus(job.job_id);
        if (latest.output) {
          const outputBox = document.createElement('pre');
          outputBox.className = 'output-box';
          outputBox.textContent = latest.output.trim();
          jobItem.appendChild(outputBox);
        }

        // Show Cancel button only if still running
        if (job.status === 'running') {
          const cancelBtn = document.createElement('button');
          cancelBtn.textContent = 'Cancel';
          cancelBtn.className = 'cancel-btn';
          cancelBtn.onclick = () => cancelJob(job.job_id);
          jobItem.appendChild(cancelBtn);
        }

        jobList.appendChild(jobItem);
      }
    } catch (err) {
      console.error('Failed to load jobs:', err);
    }
  }

  function getStatusColor(status) {
    switch (status) {
      case 'success': return 'green';
      case 'failed': return 'red';
      case 'cancelled': return 'gray';
      case 'running': return 'orange';
      default: return 'lightgray';
    }
  }

  // Initial and auto refresh
  loadJobs();
  setInterval(loadJobs, 5000);
});
