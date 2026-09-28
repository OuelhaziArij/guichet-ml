from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_mode_mock():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["mode"] == "mock"


def test_detection_francais():
    r = client.post("/detect-language", json={"text": "Je ne peux plus acceder a mon compte."})
    assert r.status_code == 200
    assert r.json()["language"] == "fr"


def test_detection_arabe():
    r = client.post("/detect-language", json={"text": "لا أستطيع الدخول إلى حسابي"})
    assert r.json()["language"] == "ar"


def test_texte_trop_court_rejete():
    assert client.post("/detect-language", json={"text": "ab"}).status_code == 422
def test_champ_text_absent():
    assert client.post("/detect-language", json={}).status_code == 422


def test_fournisseur_en_panne_503(monkeypatch):
    def panne(text):
        raise RuntimeError("panne simulee")

    monkeypatch.setattr("app.main.provider.detect_language", panne)
    r = client.post("/detect-language", json={"text": "Bonjour tout le monde"})
    assert r.status_code == 503
    assert "panne simulee" not in r.text


def test_requires_review_sous_le_seuil(monkeypatch):
    monkeypatch.setattr("app.main.REVIEW_THRESHOLD", 0.99)
    r = client.post("/detect-language", json={"text": "hello, how are you today"})
    assert r.json()["requires_review"] is True
