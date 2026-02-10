pip install -r requirements.txt
cd ..
pytest Cinescope_exam/tests/api/test_movies_api.py -v -s

негативные тесты
pytest Cinescope_exam/tests/api/negative_movies_api_test.py -v -s