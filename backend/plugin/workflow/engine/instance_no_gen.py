from backend.core.conf import settings
from backend.utils.timezone import timezone


class WorkflowInstanceNoGenerator:
    @staticmethod
    def generate() -> str:
        prefix = getattr(settings, 'WORKFLOW_INSTANCE_NO_PREFIX', 'WF')
        return f"{prefix}{timezone.now().strftime('%Y%m%d%H%M%S%f')[:-3]}"


instance_no_generator = WorkflowInstanceNoGenerator()
