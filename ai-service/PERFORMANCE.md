# Performance Benchmark

## Endpoint: /categorise

- p50: 2055 ms  
- p95: 2307 ms  
- p99: 2415 ms  

## Observations

- Initial response time is high due to AI model processing
- Subsequent responses improve when cache is used
- Redis caching reduces repeated request latency

## Conclusion

- API is functional and stable
- Performance acceptable for AI-based processing
- Cache layer helps optimize repeated queries