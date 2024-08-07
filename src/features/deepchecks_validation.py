from deepchecks.vision import classification_dataset_from_directory
from deepchecks.vision.suites import train_test_validation

from src.config import PROCESSED_DATA_DIR, REPORTS_DIR

train_ds, test_ds = classification_dataset_from_directory(
    PROCESSED_DATA_DIR / 'euroSAT', object_type="VisionData", image_extension="jpg"
)
suite = train_test_validation()
result = suite.run(train_ds, test_ds)

result.save_as_html(str(REPORTS_DIR / "deepchecks_validation.html"))
