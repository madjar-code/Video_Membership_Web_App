from uuid import UUID
from pydantic import (
    HttpUrl,
    BaseModel,
    validator,
    root_validator,
)
from app.users.exceptions import InvalidUserIDException
from .exceptions import (
    InvalidYoutubeVideoURLException,
    VideoAlreadyAddedException,
)
from .extractors import extract_video_id
from .models import Video


class VideoCreateSchema(BaseModel):
    url: HttpUrl
    user_id: UUID

    @validator('url')
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(v)
        if video_id is None:
            raise ValueError(f'{url} is not a valid Youtube URL')
        return url

    @root_validator
    def validate_data(cls, values):
        url = values.get('url')
        if url is None:
            raise ValueError('A valid URL is required')
        user_id = values.get('user_id')
        video_obj: Video | None = None
        try:
            video_obj = Video.add_video(url, user_id)
        except InvalidYoutubeVideoURLException:
            raise ValueError(f"{url} is not a valid YouTube URL")
        except VideoAlreadyAddedException:
            raise ValueError(f"{url} has already been added to your account.")
        except InvalidUserIDException:
            raise ValueError("There's a problem with your account, please try again.")
        except:
            raise ValueError("There's a problem with your account, please try again")
        if video_obj is None or not isinstance(video_obj, Video):
            raise ValueError("There's a problem with your account, please try again")            
        return video_obj.as_data()
