"""
Test script for Edward Growth System API endpoints
Run with: python test_api.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint"""
    print("\n🧪 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ Health check passed")
    return response.json()


def test_root_endpoint():
    """Test root endpoint"""
    print("\n🧪 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    print(f"✅ API Version: {data['version']}")
    print(f"✅ Modules: {', '.join(data['modules'])}")
    return data


def test_capture_insight():
    """Test knowledge insight capture"""
    print("\n🧪 Testing knowledge capture...")
    
    payload = {
        "content": "AI代理是能够自主执行复杂任务的智能系统，它们可以感知环境、做出决策并采取行动。",
        "domain": "AI",
        "source": "manual",
        "language": "zh"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/insights/capture",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201
    data = response.json()
    print(f"✅ Insight captured: {data['id']}")
    print(f"   Domain: {data['domain']}")
    print(f"   Intent: {data['intent']}")
    return data


def test_structure_knowledge(insight_id):
    """Test converting insight to structured knowledge"""
    print("\n🧪 Testing knowledge structuring...")
    
    payload = {
        "insight_id": insight_id,
        "title": "AI代理的核心能力",
        "core_concept": "自主决策与行动",
        "explanation": "AI代理通过感知-决策-行动的循环，能够自主完成复杂任务，无需人类持续干预。",
        "examples": [
            "自动驾驶汽车根据路况做出实时决策",
            "智能客服自动处理客户咨询并解决问题"
        ],
        "applications": [
            "客户服务自动化",
            "数据分析与洞察生成",
            "流程自动化优化"
        ],
        "difficulty": 3,
        "importance": 4
    }
    
    response = requests.post(
        f"{BASE_URL}/api/insights/structure",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201
    data = response.json()
    print(f"✅ Knowledge structured: {data['id']}")
    print(f"   Mastery level: {data['mastery_level']}")
    return data


def test_trigger_review():
    """Test triggering a daily review session"""
    print("\n🧪 Triggering daily review...")
    
    payload = {
        "review_type": "daily",
        "scheduled_time": None
    }
    
    response = requests.post(
        f"{BASE_URL}/api/review/trigger",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201
    data = response.json()
    print(f"✅ Review session created: {data['id']}")
    print(f"   Type: {data['review_type']}")
    print(f"   Status: {data['status']}")
    return data


def test_submit_review_response(review_id):
    """Test submitting review responses"""
    print("\n🧪 Submitting review responses...")
    
    payload = {
        "responses": """今天学习了AI代理的相关知识，理解了其核心能力和应用场景。
在营销工作中可以考虑使用AI代理来自动化客户分析和个人化推荐。
需要进一步探索如何将国学智慧与现代管理结合。""",
        "new_insights": {
            "key_learning": "AI代理可以应用于营销自动化",
            "action_item": "研究AI营销工具"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/review/{review_id}/respond",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200
    data = response.json()
    print(f"✅ Review responses submitted")
    print(f"   Status: {data['status']}")
    return data


def test_generate_speech():
    """Test generating a speech draft"""
    print("\n🧪 Generating TED Talk speech...")
    
    payload = {
        "topic": "AI时代的学习革命",
        "template_type": "ted_talk",
        "key_points": [
            "传统教育模式的局限性",
            "AI如何个性化学习路径",
            "终身学习的重要性",
            "未来教育的愿景"
        ],
        "target_duration": 18,
        "audience": "教育工作者和学习者",
        "tone": "inspirational"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/speech/generate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201
    data = response.json()
    print(f"✅ Speech draft generated: {data['id']}")
    print(f"   Template: {data['template_type']}")
    print(f"   Duration: ~{data['estimated_duration']} minutes")
    return data


def test_log_application(knowledge_id):
    """Test logging a knowledge application"""
    print("\n🧪 Logging knowledge application...")
    
    payload = {
        "knowledge_id": knowledge_id,
        "scenario": "在公司战略会议中应用AI代理概念，设计智能客户分析系统架构",
        "outcome": "团队认可方案，决定在下季度试点项目中采用",
        "lessons_learned": "将抽象的AI概念转化为具体的业务场景需要清晰的沟通和实例展示",
        "effectiveness": 4.5,
        "confidence_level": 0.8,
        "context_tags": ["战略规划", "AI应用", "团队沟通"],
        "stakeholders": ["CTO", "产品总监", "技术团队"],
        "follow_up_needed": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/application/log",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201
    data = response.json()
    print(f"✅ Application logged: {data['id']}")
    print(f"   Effectiveness: {data['effectiveness']}/5")
    return data


def test_get_application_stats():
    """Test getting application statistics"""
    print("\n🧪 Getting application statistics...")
    
    response = requests.get(f"{BASE_URL}/api/application/stats")
    
    assert response.status_code == 200
    data = response.json()
    print(f"✅ Statistics retrieved")
    print(f"   Total applications: {data['total_applications']}")
    print(f"   Success rate: {data['success_rate']:.1%}")
    print(f"   Avg effectiveness: {data['avg_effectiveness']:.2f}/5")
    return data


def run_all_tests():
    """Run all API tests"""
    print("=" * 60)
    print("Edward Growth System API - Integration Tests")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        test_health_check()
        test_root_endpoint()
        
        # Test knowledge workflow
        insight = test_capture_insight()
        knowledge = test_structure_knowledge(insight['id'])
        
        # Test review workflow
        review = test_trigger_review()
        test_submit_review_response(review['id'])
        
        # Test speech generation
        speech = test_generate_speech()
        
        # Test application tracking
        test_log_application(knowledge['id'])
        test_get_application_stats()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error: Is the API server running?")
        print("   Start with: cd backend && uvicorn app.main:app --reload")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    run_all_tests()
