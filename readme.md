<div align=center>
  <h1>http_bench_static</h1>
</div>

How do different web servers handle concurrent requests with the same static load.

## Task
Receive a JSON payload concurrently, wait for multiple different "workloads" to run, and return a JSON response.
e.g. a workload of 2s, 1s and 0.5s; since the workloads are parallel they should total the max time under clean conditions, however the added tasks will increase the overhead.

Optional timeout of e.g. 5s for the whole request

## Results
1 worker, 10 threads

Framework | lang | 20 connections (95th %, req/s) | 100 connections (95th %, req/s)
---|---|---|---
Flask & Gunicorn | python | 4657.61ms, 4.67 | 20780.28ms, 4.67
axum | rust | 2012.50ms, 9.33 | 2032.59ms, 46.66


To do:
- Tide (rust)
- warp (rust)
- actix-web (rust)

## Tools
[rewrk](https://github.com/lnx-search/rewrk)
```
./send_rewrk
```

[hyperfine](https://github.com/sharkdp/hyperfine)
```
hyperfine ./send_curl
```

