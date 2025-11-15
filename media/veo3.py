"""
VEO3 (Gemini Veo-like) video generation client.

This module provides a generic client implementation for interacting with a
hypothetical VEO3 / Gemini Veo video generation API. The exact API surface
varies by provider; this client implements a flexible pattern:

- Build a video generation request payload from a text prompt + options
- Submit the job to an HTTP endpoint (config.VEO3_API_URL) or via the
  `google.generativeai` SDK when available and configured
- Poll for job completion (exponential backoff)
- Download the generated video artifact when ready and save to disk

Notes:
- This is an implementation scaffold. To make it work in your environment
  you must provide either:
    - `VEO3_API_URL` environment variable pointing to a compatible HTTP
      endpoint that accepts job submissions and returns job IDs / presigned
      URLs, or
    - `GOOGLE_API_KEY` (or other provider SDK) and adjust the SDK call
      pathway below.
- This module is intentionally defensive: it logs actionable errors and
  returns `None` on failure instead of raising network/SDK exceptions.

Usage example:

    from media.veo3 import generate_video_with_veo3
    out = Path("/tmp/out.mp4")
    success = generate_video_with_veo3(prompt, out, api_url=os.getenv('VEO3_API_URL'))

"""
from __future__ import annotations

import time
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any

import requests

import config

logger = logging.getLogger(__name__)

# Config keys:
# - VEO3_API_URL: optional HTTP endpoint to submit video jobs
# - GOOGLE_API_KEY: if you prefer to use a provider SDK instead, set this
VEO3_API_URL = None
if not VEO3_API_URL:
    VEO3_API_URL = getattr(config, 'VEO3_API_URL', None) or None

# Polling defaults
POLL_INTERVAL_SECONDS = 2
POLL_MAX_SECONDS = 60 * 5  # 5 minutes default


class VEO3Client:
    """Simple client for submitting video generation jobs to a VEO3 HTTP API.

    This client expects the API to expose these endpoints (common pattern):
      - POST {api_url}/jobs  => returns {"job_id": "..."}
      - GET  {api_url}/jobs/{job_id} => returns {"status": "pending|running|done|failed", "result_url": "https://..."}

    If your provider differs, adapt `submit_job` and `get_job_status`.
    """

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_url = api_url or VEO3_API_URL
        self.api_key = api_key or config.GOOGLE_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_url or self.api_key)

    def submit_job(self, payload: Dict[str, Any]) -> Optional[str]:
        """Submit a job and return job_id or None on failure."""
        if self.api_url:
            try:
                headers = {"Content-Type": "application/json"}
                if self.api_key:
                    # If the API expects a bearer token header
                    headers["Authorization"] = f"Bearer {self.api_key}"

                resp = requests.post(f"{self.api_url.rstrip('/')}/jobs", json=payload, headers=headers, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                job_id = data.get('job_id') or data.get('id')
                if not job_id:
                    logger.error("VEO3 submit: no job_id in response: %s", resp.text)
                    return None
                return str(job_id)
            except requests.RequestException as e:
                logger.error("VEO3 submit request failed: %s", e)
                return None
            except Exception as e:
                logger.exception("Unexpected error submitting VEO3 job: %s", e)
                return None
        else:
            logger.error("No VEO3 API URL configured (VEO3_API_URL or config.VEO3_API_URL)")
            return None

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status. Expected to return a dict with keys: status, result_url (if done)."""
        if not self.api_url:
            logger.error("VEO3 get_job_status called but api_url not configured")
            return None
        try:
            resp = requests.get(f"{self.api_url.rstrip('/')}/jobs/{job_id}", timeout=20)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error("VEO3 status request failed: %s", e)
            return None
        except Exception as e:
            logger.exception("Unexpected error fetching VEO3 job status: %s", e)
            return None

    def download_result(self, result_url: str, destination: Path) -> bool:
        """Download the result file from a presigned URL or http endpoint."""
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with requests.get(result_url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(destination, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            logger.info("Downloaded VEO3 result to %s", destination)
            return True
        except requests.RequestException as e:
            logger.error("Failed to download VEO3 result: %s", e)
            return False
        except Exception as e:
            logger.exception("Unexpected error downloading result: %s", e)
            return False


def generate_video_with_veo3(
    prompt: str,
    output_path: Path,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    timeout_seconds: int = POLL_MAX_SECONDS,
) -> Optional[Path]:
    """High-level helper to generate video via VEO3-like API and save to `output_path`.

    Returns `output_path` on success, or `None` on failure.

    Options may include desired duration, resolution, voice settings, etc. The
    payload shape depends on your provider; this helper sends a reasonable
    generic payload and logs the full payload for debugging.
    """
    client = VEO3Client(api_url=api_url, api_key=api_key)

    if not client.is_configured():
        logger.error("VEO3 client is not configured. Set VEO3_API_URL or an API key in config.")
        return None

    payload = {
        'prompt': prompt,
        'options': options or {},
        'metadata': {
            'source': 'BIDV-custom-mail',
            'timestamp': int(time.time())
        }
    }

    logger.info("Submitting VEO3 job: payload keys=%s", list(payload.keys()))
    job_id = client.submit_job(payload)
    if not job_id:
        logger.error("Failed to submit VEO3 job")
        return None

    logger.info("VEO3 job submitted: %s; polling for completion...", job_id)

    started = time.time()
    sleep_interval = POLL_INTERVAL_SECONDS
    while True:
        if time.time() - started > timeout_seconds:
            logger.error("VEO3 job %s timed out after %s seconds", job_id, timeout_seconds)
            return None

        status_resp = client.get_job_status(job_id)
        if not status_resp:
            logger.warning("Empty status response for job %s; retrying...", job_id)
            time.sleep(sleep_interval)
            sleep_interval = min(sleep_interval * 1.5, 10)
            continue

        status = status_resp.get('status') or status_resp.get('state')
        logger.info("VEO3 job %s status: %s", job_id, status)

        if status in ('done', 'succeeded', 'completed'):
            result_url = status_resp.get('result_url') or status_resp.get('output_url') or (status_resp.get('result') or {}).get('url')
            if not result_url:
                logger.error("Job %s reported success but no result_url present: %s", job_id, status_resp)
                return None

            # Download
            ok = client.download_result(result_url, output_path)
            return output_path if ok else None

        if status in ('failed', 'error'):
            logger.error("VEO3 job %s failed: %s", job_id, status_resp)
            return None

        # still pending/running -> wait
        time.sleep(sleep_interval)
        sleep_interval = min(sleep_interval * 1.5, 10)


if __name__ == '__main__':
    # Quick local smoke test (will not run unless VEO3_API_URL or key is configured)
    logging.basicConfig(level=logging.INFO)
    sample_prompt = (
        "Short product promo video: show charts, highlight top category, include a friendly CTA."
    )
    out = Path('./media/output/test_veo3_video.mp4')
    res = generate_video_with_veo3(sample_prompt, out)
    print('Result:', res)
