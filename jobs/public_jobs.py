import requests
from typing import List, Dict, Optional
from datetime import datetime

class PublicJobSearch:
    """Safe public job search provider that doesn't use web scraping."""
    
    @staticmethod
    def search_remotive(query: str, limit: int = 10) -> List[Dict]:
        """Search jobs using the free Remotive API (mostly remote tech jobs)"""
        url = f"https://remotive.com/api/remote-jobs?search={query}&limit={limit}"
        jobs = []
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for job in data.get('jobs', [])[:limit]:
                    # Normalize to required fields
                    jobs.append({
                        "id": str(job.get("id")),
                        "company": job.get("company_name"),
                        "title": job.get("title"),
                        "location": job.get("candidate_required_location") or "Remote",
                        "work_mode": "Remote",
                        "employment_type": job.get("job_type", "").replace("_", " ").title() if job.get("job_type") else None,
                        "salary": job.get("salary"),
                        "source": "Remotive",
                        "source_url": job.get("url"),
                        "apply_url": job.get("url"),
                        "posted_date": job.get("publication_date"),
                        "description": job.get("description")
                    })
        except Exception as e:
            print(f"Remotive API error: {e}")
        return jobs

    @staticmethod
    def search_jobs(query: str, location: str = "") -> List[Dict]:
        """
        Search for jobs across safe public APIs.
        Returns properly normalized job data.
        Clearly labeled as SOURCE ONLY (not verified active).
        """
        all_jobs = []
        
        # 1. Remotive (Remote Jobs)
        remotive_query = query
        if location and location.lower() != "india" and location.lower() != "remote":
            remotive_query = f"{query} {location}"
            
        remotive_jobs = PublicJobSearch.search_remotive(remotive_query)
        all_jobs.extend(remotive_jobs)
        
        return all_jobs
