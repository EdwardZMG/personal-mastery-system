from app.schemas.common import (
    PaginationParams,
    PaginatedResponse,
    SuccessResponse,
    ErrorResponse,
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserProfileUpdate,
    UserProfileResponse,
)
from app.schemas.knowledge import (
    InsightCapture,
    InsightResponse,
    InsightListResponse,
    StructureRequest,
    KnowledgeResponse,
)
from app.schemas.learning import (
    LearningRecordCreate,
    LearningRecordResponse,
    ContentResponse,
)
from app.schemas.review import (
    ReviewTrigger,
    ReviewRespond,
    ReviewResponse,
)
from app.schemas.speech import (
    SpeechGenerate,
    SpeechResponse,
    SpeechMaterialCreate,
)
from app.schemas.goal import (
    GoalCreate,
    GoalUpdate,
    GoalResponse,
)
from app.schemas.habit import (
    HabitCreate,
    HabitLogCreate,
    HabitResponse,
    HabitLogResponse,
)
from app.schemas.classics import (
    ClassicsProgressResponse,
    ClassicsProgressUpdate,
)
