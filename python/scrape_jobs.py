"""
Job Description Web Scraper

This script scrapes job descriptions from various job boards and saves them
to the data/processed/jobs directory.
"""

import os
import json
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin


class JobScraper:
    """Web scraper for job descriptions from multiple sources"""
    
    def __init__(self, output_dir: str = "data/raw/jobs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_remotive_jobs(self, category: str = "software-dev", limit: int = 10) -> List[Dict]:
        """
        Scrape jobs from Remotive API (free, no auth required)
        Categories: software-dev, customer-support, design, sales, marketing, product, business, data, devops, finance, hr, legal, operations, quality-assurance, teaching
        """
        jobs = []
        try:
            url = f"https://remotive.com/api/remote-jobs?category={category}&limit={limit}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            for job in data.get('jobs', []):
                job_data = {
                    'title': job.get('title', ''),
                    'company': job.get('company_name', ''),
                    'location': job.get('candidate_required_location', 'Remote'),
                    'description': job.get('description', ''),
                    'job_type': job.get('job_type', ''),
                    'category': job.get('category', category),
                    'url': job.get('url', ''),
                    'publication_date': job.get('publication_date', ''),
                    'source': 'remotive'
                }
                jobs.append(job_data)
                print(f"✓ Scraped: {job_data['title']} at {job_data['company']}")
            
            print(f"\nSuccessfully scraped {len(jobs)} jobs from Remotive")
            return jobs
            
        except Exception as e:
            print(f"Error scraping Remotive: {e}")
            return jobs
    
    def scrape_linkedin_jobs(self, search_term: str = "software engineer", location: str = "United States", limit: int = 25) -> List[Dict]:
        """
        Scrape jobs from LinkedIn using their public job search (no auth required)
        Note: This uses LinkedIn's public job board without authentication
        """
        jobs = []
        try:
            # LinkedIn's public job search URL
            base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            
            params = {
                'keywords': search_term,
                'location': location,
                'start': 0,
                'pageNum': 0,
                'f_TP': '1'  # Posted in last 24 hours, remove for all time
            }
            
            # LinkedIn headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            collected = 0
            page = 0
            
            while collected < limit and page < 5:  # Max 5 pages
                params['start'] = page * 25
                
                response = requests.get(base_url, params=params, headers=headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')
                
                if not job_cards:
                    break
                
                for card in job_cards:
                    if collected >= limit:
                        break
                    
                    try:
                        # Extract job details
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        location_elem = card.find('span', class_='job-search-card__location')
                        link_elem = card.find('a', class_='base-card__full-link')
                        
                        if title_elem is not None and company_elem is not None and link_elem is not None:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else location
                            job_url = str(link_elem.get('href', ''))
                        else:
                            continue    
                        
                        # Try to get full job description
                        description = self._get_linkedin_job_description(job_url)
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'description': description,
                            'job_type': 'N/A',
                            'category': search_term,
                            'url': job_url,
                            'publication_date': datetime.now().strftime('%Y-%m-%d'),
                            'source': 'linkedin'
                        }
                        
                        jobs.append(job_data)
                        collected += 1
                        print(f"✓ Scraped: {title} at {company}")
                        
                        # Be respectful with rate limiting
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                
                page += 1
                time.sleep(2)  # Rate limiting between pages
            
            print(f"\nSuccessfully scraped {len(jobs)} jobs from LinkedIn")
            return jobs
            
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
            return jobs
    
    def _get_linkedin_job_description(self, job_url: str) -> str:
        """
        Fetch the full job description from a LinkedIn job posting
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(job_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the job description section
            description_elem = soup.find('div', class_='show-more-less-html__markup')
            
            if description_elem:
                return description_elem.get_text(separator='\n', strip=True)
            else:
                return "Description not available"
                
        except Exception as e:
            return f"Could not fetch full description: {str(e)}"
    
    def scrape_arbeitnow_jobs(self, search_term: str = "software", limit: int = 20) -> List[Dict]:
        """
        Scrape jobs from Arbeitnow API (free, no auth required)
        """
        jobs = []
        try:
            url = "https://www.arbeitnow.com/api/job-board-api"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            all_jobs = data.get('data', [])
            
            # Filter by search term
            filtered_jobs = [
                job for job in all_jobs 
                if search_term.lower() in job.get('title', '').lower() 
                or search_term.lower() in job.get('description', '').lower()
            ][:limit]
            
            for job in filtered_jobs:
                job_data = {
                    'title': job.get('title', ''),
                    'company': job.get('company_name', ''),
                    'location': job.get('location', 'Remote'),
                    'description': job.get('description', ''),
                    'job_type': job.get('job_types', ['N/A'])[0] if job.get('job_types') else 'N/A',
                    'category': ', '.join(job.get('tags', [])),
                    'url': job.get('url', ''),
                    'publication_date': job.get('created_at', ''),
                    'source': 'arbeitnow'
                }
                jobs.append(job_data)
                print(f"✓ Scraped: {job_data['title']} at {job_data['company']}")
            
            print(f"\nSuccessfully scraped {len(jobs)} jobs from Arbeitnow")
            return jobs
            
        except Exception as e:
            print(f"Error scraping Arbeitnow: {e}")
            return jobs
    
    def scrape_github_jobs_api(self, search_term: str = "developer", limit: int = 20) -> List[Dict]:
        """
        Scrape tech jobs from GitHub Jobs alternatives (using Remotive as primary)
        """
        jobs = []
        try:
            # Since GitHub Jobs API is deprecated, using an alternative aggregator
            url = f"https://remotive.com/api/remote-jobs?search={search_term}&limit={limit}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            for job in data.get('jobs', [])[:limit]:
                job_data = {
                    'title': job.get('title', ''),
                    'company': job.get('company_name', ''),
                    'location': job.get('candidate_required_location', 'Remote'),
                    'description': job.get('description', ''),
                    'job_type': job.get('job_type', ''),
                    'category': job.get('category', search_term),
                    'url': job.get('url', ''),
                    'publication_date': job.get('publication_date', ''),
                    'source': 'remotive_search'
                }
                jobs.append(job_data)
                print(f"✓ Scraped: {job_data['title']} at {job_data['company']}")
            
            print(f"\nSuccessfully scraped {len(jobs)} jobs from search")
            return jobs
            
        except Exception as e:
            print(f"Error scraping jobs: {e}")
            return jobs
    
    def save_job_to_file(self, job: Dict, index: int):
        """Save individual job description to a text file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        company_clean = job['company'].replace(' ', '_').replace('/', '_')[:30]
        title_clean = job['title'].replace(' ', '_').replace('/', '_')[:40]
        
        filename = f"{timestamp}_{index:03d}_{company_clean}_{title_clean}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        # Format the job description nicely
        content = f"""JOB TITLE: {job['title']}
COMPANY: {job['company']}
LOCATION: {job['location']}
JOB TYPE: {job.get('job_type', 'N/A')}
CATEGORY: {job.get('category', 'N/A')}
SOURCE: {job.get('source', 'N/A')}
URL: {job.get('url', 'N/A')}
PUBLICATION DATE: {job.get('publication_date', 'N/A')}

{'='*80}
DESCRIPTION:
{'='*80}

{job['description']}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def save_jobs_metadata(self, jobs: List[Dict], filename: str = "jobs_metadata.json"):
        """Save all jobs metadata to a JSON file"""
        filepath = os.path.join(self.output_dir, filename)
        
        metadata = {
            'scrape_timestamp': datetime.now().isoformat(),
            'total_jobs': len(jobs),
            'jobs': jobs
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✓ Saved metadata to {filename}")
    
    def run(self, sources: List[str] = ['remotive', 'linkedin', 'arbeitnow'], 
            categories: List[str] = ['software-dev'], 
            limit_per_source: int = 10):
        """
        Run the scraper across multiple sources
        
        Args:
            sources: List of sources to scrape from ['remotive', 'linkedin', 'arbeitnow', 'github']
            categories: List of job categories/search terms to scrape
            limit_per_source: Maximum number of jobs to scrape per source per category
        """
        all_jobs = []
        
        print(f"\n{'='*80}")
        print(f"Starting Job Scraping")
        print(f"{'='*80}\n")
        
        for category in categories:
            print(f"\n--- Scraping category: {category} ---")
            
            if 'remotive' in sources:
                jobs = self.scrape_remotive_jobs(category=category, limit=limit_per_source)
                all_jobs.extend(jobs)
                time.sleep(1)  # Be respectful with rate limiting
            
            if 'linkedin' in sources:
                jobs = self.scrape_linkedin_jobs(search_term=category, limit=limit_per_source)
                all_jobs.extend(jobs)
                time.sleep(2)  # LinkedIn needs more time
            
            if 'arbeitnow' in sources:
                jobs = self.scrape_arbeitnow_jobs(search_term=category, limit=limit_per_source)
                all_jobs.extend(jobs)
                time.sleep(1)
            
            if 'github' in sources:
                jobs = self.scrape_github_jobs_api(search_term=category, limit=limit_per_source)
                all_jobs.extend(jobs)
                time.sleep(1)

        # Save individual job files
        print(f"\n{'='*80}")
        print(f"Saving job descriptions to files...")
        print(f"{'='*80}\n")
        
        for idx, job in enumerate(all_jobs, 1):
            filename = self.save_job_to_file(job, idx)
            print(f"✓ Saved: {filename}")
        
        # Save metadata
        self.save_jobs_metadata(all_jobs)
        
        print(f"\n{'='*80}")
        print(f"Scraping Complete!")
        print(f"{'='*80}")
        print(f"Total jobs scraped: {len(all_jobs)}")
        print(f"Files saved to: {self.output_dir}")
        print(f"{'='*80}\n")
        
        return all_jobs


def main():
    """Main function to run the scraper"""
    scraper = JobScraper()
    
    # Scrape 25+ jobs from multiple sources
    jobs = scraper.run(
        sources=['remotive', 'linkedin', 'arbeitnow'],  # Multiple sources
        categories=['software engineer', 'data scientist', 'devops engineer'],  # Multiple search terms
        limit_per_source=10  # 10 per source per category = 90 potential jobs
    )
    
    return jobs


if __name__ == "__main__":
    main()
