from app.models.factory import get_model


class MedGemmaClinicalTextModel:
    """Named role for medical synthesis; provider/model remains configurable."""
    @staticmethod
    def client():
        return get_model("synthesis")


class MedGemmaClinicalExtractor:
    @staticmethod
    def client():
        return get_model("extractor")


class MedGemmaClinicalVision:
    @staticmethod
    def client():
        return get_model("vision")
