"""
Test script to verify rate limit handling works correctly
"""

def test_rate_limit_detection():
    """Test that rate limit errors are detected correctly"""
    
    test_errors = [
        "Rate limit reached for model llama-3.3-70b-versatile",
        "Limit 100000, Used 99997, Requested 125",
        '{"error":{"message":"Rate limit reached","type":"tokens","code":"ratelimitexceeded"}}',
        "429 Too Many Requests",
        "quota exceeded",
        "tokens per day (TPD): Limit 100000"
    ]
    
    keywords = [
        'rate', 'limit', 'quota', 'exceeded', 'ratelimit', 
        'tokens per day', 'tpd', '429'
    ]
    
    print("Testing Rate Limit Detection:")
    print("=" * 60)
    
    for error in test_errors:
        error_lower = error.lower()
        is_rate_limit = any(keyword in error_lower for keyword in keywords)
        
        status = "✅ DETECTED" if is_rate_limit else "❌ MISSED"
        print(f"{status}: {error[:50]}...")
    
    print("\n" + "=" * 60)
    print("All rate limit patterns should be detected!")

if __name__ == "__main__":
    test_rate_limit_detection()
