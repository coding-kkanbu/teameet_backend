# Change Log

## Unreleased

### Environment

- set python version 3.8-bullseye

### Github

- set ISSUE_TEMPLATE & PULL_REQUEST_TEMPLATE

### Docs

- README: docker를 이용한 초기 세팅 방법 추가

### Docker

- local.yml: fix docs external port from 7000 to 7777

### CI

- add cache-dependency-path to 'set up python' in linter [cookiecutter-django update](https://github.com/cookiecutter/cookiecutter-django/pull/3520/files)
- change applied branch to 'dev' from 'master'

### THIRD_PARTY_APPS

- dj-rest_auth
  - 사용자 관리를 위한 REST API 패키지 추가
  - 사용자가 소셜 로그인할 수 있도록 구글, 카카오 로그인 rest api로 구현
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)
  - OpenAPI 3.0 문서 생산을 위한 패키지 추가
- django-taggit
  - Tag 기능을 위한 app 추가
  - TaggableManager / TaggitSerializer로 tag 생성 및 삭제 가능

### Default Security Settings

- Authentication
  - CustomjwtCookieAuthentication
    - accounts/authentication.py 참고
  - api/v1/accounts 앱에 한해서만 BasicAuthentication(모두허용)
- Permission
  - IsAuthenticated

### Board

- models : Post, Category, Comment, SogaetingOption
- serializer:
  - SogaetingOptionSerializer
  - UserSerializer
  - PostListSerializer
  - PostSerializer
  - PitAPatSerializer
  - CategorySerializer
  - CommentSerializer
  - CommentListSerializer
- views
  - AbstractPostViewSet
  - TopicViewSet
  - PitAPatViewSet
  - CategoryViewSet
  - CommentViewSet
- permissions
  - IsOwnerOrReadOnly
- pagination
  - PostLimitOffsetPagination
  - PostPageNumberPagination
  - CategoryPageNumberPagination
- filter_backends
  - SearchFilter, OrderingFilter (DRF built-in)
  - TagFilter (Customize)

### Operation

- models: PostBlame, CommentBlame, PostLike, CommentLike
- views:
  - PostBlameViewSet
  - CommentBlameViewSet
  - PostLikeViewset
  - CommentLikeViewset

### Notification

- models: Notification
- views
  - NotificationViewset
- signals
  - notifiy
- pagination
  - NotiPageNumberPagination
- filter_backends
  - OrderingFilter (DRF built-in)

### User

- models: User
- views
  - UserViewset
- pagination
  - PageNumberPagination(default)

### Accounts

- views
  - VerifyNeisEmail
  - VerifyNeisEmailConfirm
