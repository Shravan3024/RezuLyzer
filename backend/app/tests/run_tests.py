import sys
import asyncio
import traceback
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.tests import test_resumeiq
from app.tests.test_async_api import run_api_tests

def run_all_tests():
    unit_tests = [
        ("test_document_parser_pdf", test_resumeiq.test_document_parser_pdf),
        ("test_document_parser_docx", test_resumeiq.test_document_parser_docx),
        ("test_document_parser_invalid_file", test_resumeiq.test_document_parser_invalid_file),
        ("test_text_preprocessor_preserves_tech_terms", test_resumeiq.test_text_preprocessor_preserves_tech_terms),
        ("test_skill_extractor_canonical_and_aliases", test_resumeiq.test_skill_extractor_canonical_and_aliases),
        ("test_job_analyzer_templates", test_resumeiq.test_job_analyzer_templates),
        ("test_job_analyzer_custom_text", test_resumeiq.test_job_analyzer_custom_text),
        ("test_experience_evaluation", test_resumeiq.test_experience_evaluation),
        ("test_education_evaluation", test_resumeiq.test_education_evaluation),
        ("test_ats_scorer_calculation", test_resumeiq.test_ats_scorer_calculation),
        ("test_recommendation_engine", test_resumeiq.test_recommendation_engine),
    ]

    passed = 0
    failed = 0
    print("=" * 70)
    print("RESULYZER AUTOMATED TEST SUITE: UNIT & NLP ENGINE TESTS")
    print("=" * 70)

    for name, func in unit_tests:
        try:
            func()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 70)
    print("RESULYZER AUTOMATED TEST SUITE: END-TO-END ASYNC API INTEGRATION TESTS")
    print("=" * 70)

    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(run_api_tests())
        passed += 9  # 9 sub-tests inside run_api_tests
    except Exception as e:
        print(f"[FAIL] run_api_tests: {e}")
        traceback.print_exc()
        failed += 1

    total = len(unit_tests) + 9
    print("\n" + "=" * 70)
    print(f"FINAL TEST SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL: {total})")
    print("=" * 70)
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()

