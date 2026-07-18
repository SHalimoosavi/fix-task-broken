There is an Apache-style access log at /app/access.log. Parse it and write a JSON
summary report to /app/report.json.

The report must be a JSON object with exactly these three keys:
- total_requests: the total number of log lines (requests) in the file
- unique_ips: the number of distinct client IP addresses (the first field of each line)
- top_path: the request path (e.g. "/index.html") that appears most often across all
  requests; if there is a tie, use whichever tied path appears first in the log

Success criteria:
1. /app/report.json exists and contains valid JSON.
2. total_requests equals the number of non-empty lines in /app/access.log.
3. unique_ips equals the count of distinct IP addresses appearing as the first field
   of any log line.
4. top_path equals the most frequently requested path, using the tie-break rule above.
