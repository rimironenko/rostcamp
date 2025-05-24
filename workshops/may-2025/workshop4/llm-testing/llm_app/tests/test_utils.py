from app.utils import logger

def test_logger_prints(caplog):
    with caplog.at_level("INFO", logger="llm_app"):
        logger.info("Test log message")
    assert any("Test log message" in message for message in caplog.messages) 