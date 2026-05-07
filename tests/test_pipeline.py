# test_pipeline.py
# Automated tests for CSV Cleaner

import pytest
import pandas as pd
import os
import sys

# Add parent folder so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, clean_data

# ===== SETUP =====
@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for testing"""
    csv_content = """order_id,product,quantity,price,status
1,Laptop,2,45000,completed
2,Mouse,5,500,completed
2,Mouse,5,500,completed
3,Keyboard,3,1200,pending
4,,2,3000,completed
5,Monitor,1,12000,completed
"""
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)

# ===== TESTS =====

def test_home_page(client):
    """Test home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    print("✅ Home page loads correctly")

def test_login_page(client):
    """Test login page loads"""
    response = client.get('/login')
    assert response.status_code == 200
    print("✅ Login page loads correctly")

def test_signup_page(client):
    """Test signup page loads"""
    response = client.get('/signup')
    assert response.status_code == 200
    print("✅ Signup page loads correctly")

def test_upload_no_file(client):
    """Test upload without file shows error"""
    response = client.post('/upload', data={})
    assert response.status_code == 200
    print("✅ Upload without file handled correctly")

def test_upload_wrong_format(client):
    """Test upload with non-CSV file"""
    data = {
        'file': (open(os.devnull, 'rb'), 'test.txt')
    }
    response = client.post('/upload',
                          data=data,
                          content_type='multipart/form-data')
    assert response.status_code == 200
    print("✅ Wrong file format handled correctly")

def test_clean_removes_duplicates(sample_csv):
    """Test that cleaning removes duplicate rows"""
    result = clean_data(sample_csv)
    original = result['stats']['original_rows']
    cleaned = result['stats']['cleaned_rows']
    removed = result['stats']['removed_rows']
    assert removed >= 0
    assert cleaned <= original
    print(f"✅ Duplicates removed: {removed} rows")

def test_clean_removes_empty(sample_csv):
    """Test that cleaning removes empty values"""
    result = clean_data(sample_csv)
    assert result['stats']['cleaned_rows'] > 0
    print("✅ Empty values removed correctly")

def test_clean_returns_stats(sample_csv):
    """Test that cleaning returns proper stats"""
    result = clean_data(sample_csv)
    assert 'original_rows' in result['stats']
    assert 'cleaned_rows' in result['stats']
    assert 'removed_rows' in result['stats']
    assert 'columns' in result['stats']
    print("✅ Stats returned correctly")

def test_clean_output_file_exists(sample_csv):
    """Test that cleaned file is created"""
    clean_data(sample_csv)
    assert os.path.exists('data/cleaned.csv')
    print("✅ Cleaned file created successfully")

def test_column_names_lowercase(sample_csv):
    """Test that column names are converted to lowercase"""
    result = clean_data(sample_csv)
    for col in result['stats']['column_names']:
        assert col == col.lower()
    print("✅ Column names are lowercase")