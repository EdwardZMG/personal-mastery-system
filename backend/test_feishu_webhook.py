"""
Test script for Feishu webhook functionality.

This script simulates various user messages to test intent recognition
and response generation without needing actual Feishu integration.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uuid import UUID
from app.api.routes.feishu_bot import recognize_intent, process_intent
from app.database import SessionLocal


def test_intent_recognition():
    """Test intent recognition with various sample messages."""
    
    test_cases = [
        # (message, expected_intent, expected_params)
        ("冥想15分钟", "meditation", {"duration": 15}),
        ("今天打坐30分钟，心情很好", "meditation", {"duration": 30, "mood": "good"}),
        ("正念练习20分钟", "meditation", {"duration": 20}),
        ("跑步30分钟", "workout", {"duration": 30, "type": "running"}),
        ("瑜伽45分钟", "workout", {"duration": 45, "type": "yoga"}),
        ("健身1小时", "workout", {"duration": 60, "type": "gym"}),
        ("读了《道德经》50页", "reading", {"book_title": "道德经", "pages": 50}),
        ("看书30分钟", "reading", {"duration": 30}),
        ("今日进度", "progress", {}),
        ("今天状态", "progress", {}),
        ("打卡", "checkin", {}),
        ("签到", "checkin", {}),
        ("帮助", "help", {}),
        ("怎么用", "help", {}),
    ]
    
    print("=" * 80)
    print("Testing Intent Recognition")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for message, expected_intent, expected_params in test_cases:
        result = recognize_intent(message)
        
        intent_match = result.intent_type == expected_intent
        params_match = all(result.parameters.get(k) == v for k, v in expected_params.items())
        
        status = " PASS" if (intent_match and params_match) else " FAIL"
        
        if intent_match and params_match:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status} | Message: {message}")
        print(f"       Expected: {expected_intent}, Got: {result.intent_type} (confidence: {result.confidence:.2f})")
        print(f"       Params: {result.parameters}")
        
        if not intent_match:
            print(f"       MISMATCH: Expected '{expected_intent}' but got '{result.intent_type}'")
        if not params_match:
            for k, v in expected_params.items():
                if result.parameters.get(k) != v:
                    print(f"       PARAM MISMATCH: {k}={v} vs {result.parameters.get(k)}")
    
    print("\n" + "=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    return failed == 0


def test_response_generation():
    """Test response generation for different intents."""
    
    db = SessionLocal()
    edward_user_id = UUID("00000000-0000-0000-0000-000000000001")
    
    test_intents = [
        "meditation",
        "workout", 
        "reading",
        "progress",
        "checkin",
        "help",
        "unknown"
    ]
    
    print("\n" + "=" * 80)
    print("Testing Response Generation")
    print("=" * 80)
    
    for intent_type in test_intents:
        print(f"\n--- Intent: {intent_type} ---")
        
        # Create a mock intent
        from app.api.routes.feishu_bot import IntentResult
        intent = IntentResult(
            intent_type=intent_type,
            confidence=0.9,
            parameters={"duration": 30} if intent_type in ["meditation", "workout"] else {},
            raw_text=f"test {intent_type}"
        )
        
        try:
            response = process_intent(intent, edward_user_id, db)
            print(response[:200] + "..." if len(response) > 200 else response)
        except Exception as e:
            print(f"ERROR: {e}")
    
    db.close()
    print("\n" + "=" * 80)


def main():
    """Run all tests."""
    print("\nFeishu Webhook Test Suite\n")
    
    # Test 1: Intent Recognition
    intent_tests_passed = test_intent_recognition()
    
    # Test 2: Response Generation  
    test_response_generation()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Intent Recognition: {'PASS' if intent_tests_passed else 'FAIL'}")
    print("=" * 80)
    
    if intent_tests_passed:
        print("\nAll tests passed! Ready to configure Feishu webhook.")
        return 0
    else:
        print("\nSome tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit(main())
